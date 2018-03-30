#####
# Part of `SmartCashVoting`
#
#
# Copyright 2018 dustinface
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#####

import os, sys
import time
import json
import threading
import getpass
import requests

from smartcash.rpc import SmartCashRPC

if sys.version_info < (3, 0):
    input = raw_input

URL_SMARTCASH = 'https://vote.smartcash.cc/api/v1'
API_PROPOSAL_LIST = '/voteproposals'
API_CAST_VOTE = '/voteproposals/castvote'

STATE_COLLECT = 0
STATE_WALLETLOCK = 1
STATE_LOAD_PROPOSALS = 2
STATE_ASK_PROPOSAL = 3
STATE_ASK_VOTE_TYPE = 4
STATE_CAST_VOTES = 5
STATE_DONE = 6
STATE_CANCELED = 7

def clear():
    print("\033[H\033[J")

def error(msg):
    print("\n[ERROR] {}\n".format(msg))

def exit(msg = ''):
    return input("{}\n[ENTER to continue{}]: ".format(msg, ' / X + ENTER to Exit' if exit else '')).upper().find('X') != -1

class SmartCashVoting(object):

    def __init__(self, rpcConfig):

        self.rpc = SmartCashRPC(rpcConfig)

        self.state = STATE_COLLECT

        self.password = None
        self.unlockedBefore = False

        self.addresses = None
        self.proposals = None
        self.activeProposal = None

        self.success = 0
        self.failed = 0


    def unlock(self, password):

        unlock = self.rpc.unlockWallet(password)

        if unlock.error:
            clear()
            error("Could not unlock wallet: {}".format(unlock.error.message))

            return False

        else:
            self.password = password
            self.unlockedBefore = False

        return True

    def collectAddresses(self):

        self.addresses = {}

        print("\n** Collect addresses **")

        addressGroupings = self.rpc.getAddressGroupings()

        if addressGroupings.error:
            error("Could not fetch addresses: {}".format(str(addressGroupings.error)))
            print("Please verify that your wallet is running and the rpc server is enabled.")
            print("Look here: https://github.com/xdustinface/SmartCashVoting#configuration-of-your-wallet")
            return False

        for addressGroup in addressGroupings.data:

            for address in addressGroup:
                if float(address[1]) > 0:
                    self.addresses[address[0]] = address[1]

        self.timeout = len(self.addresses) * 30

        if not len(self.addresses):
            error("No address with voting power detected!")
            return False

        print("  => {} addresses with overall {} SMART detected.\n".format(len(self.addresses), sum(self.addresses.values())))

        return True

    def checkWalletLock(self):

        print("\n** Check if the wallet is unlocked already **")

        # First check if the wallet is locked or not.
        unlockCheck = self.rpc.signMessage(list(self.addresses.keys())[0], "LOCKED?")

        if unlockCheck.error:

            print("  => Its locked!\n")
            print("To sign the voting messagges your wallet needs to be unlocked.")
            print("Once the voting is done your wallet will become locked again!!\n")

            print(("If you feel more comforable by unlocking inside of your wallet "
                "you can also cancel this script, run:\n\n"
                "  walletpassphrase \"yourpassword\" 1000\n\nfrom the wallet's debug console"
                "and come back afterwards. If you manually unlock"
                " your wallet this script also wont't trigger the lock at the end.\n"))

            password = getpass.getpass("Enter your wallet password: ")

            if not password:
                clear()
                error("Could not unlock wallet: Make sure you entered a password!")

                return False

            return self.unlock(password)

        else:

            self.unlockedBefore = True
            print("  => Its unlocked!\n")

        return True

    def loadProposals(self):

        print("\n** Loading open proposals from the portal **")

        self.proposals = None

        try:
            response = requests.get(URL_SMARTCASH + API_PROPOSAL_LIST)
        except Exception as e:
            error("Exception while loading the proposals: {}".format(str(e)))
        else:

            if response.status_code != 200:
                error("Could not fetch proposals from the portal: {} - {}".format(response.status_code, response.reason))
            else:

                try:

                    parsed = json.loads(response.text)

                    if 'status' in parsed and parsed['status'] == 'OK'\
                        and 'result' in parsed:

                        if not len(parsed['result']):
                            error("Looks like there are currently no proposals opened for vote?!")
                        else:
                            self.proposals = parsed['result']
                    else:
                        error("Invalid response from the voting portal.")

                except Exception as e:
                    error("Exception while loading the proposals from the portal: {}".format(str(e)))

        if not self.proposals:
            return False

        return True

    def askProposal(self):

        clear()

        print("** Select the proposal you want to vote **\n")

        self.activeProposal = None

        numError = "Your input needs no be a number from 1 to {}".format(len(self.proposals))

        idx = 0

        for proposal in self.proposals:
            idx += 1
            print("[{}] {}".format(idx, proposal['title']))

        idx = input("\nSelect any number from 1 to {}: ".format(len(self.proposals)))

        try:
            idx = int(idx) - 1
        except:

            error(numError)
            return False

        else:

            if idx < 0 or idx > len(self.proposals) - 1:

                error(numError)
                return False

            else:
                self.activeProposal = self.proposals[idx]

        return True

    def askVoteType(self):

        clear()

        print("** How do you want to vote the proposal? **\n")

        self.voteType = None

        ret = {'voteType' : None, 'result' : False }

        print("Selected proposal: {}\n".format(self.activeProposal['title']))
        voteType = input(("How do you want to vote?\n\n"
                          "[y] - YES\n"
                          "[a] - ABSTAIN\n"
                          "[n] - NO\n\n"
                          "Type y/a/n and hit enter: "))

        if voteType.upper() == 'Y':
            self.voteType = 'YES'
        elif voteType.upper() == 'A':
            self.voteType = 'Abstain'
        elif voteType.upper() == 'N':
            self.voteType =  'NO'

        else:

            error("You need to select one of the following: \n\n"
                    "y - to vote YES\n"
                    "a - to vote ABSTAIN\n"
                    "n - to vote NO")

            return False

        return True

    def castVotes(self):

        clear()

        print("** Start voting for - {}**\n".format(self.activeProposal['title']))

        self.success = 0
        self.failed = 0

        proposalId = self.activeProposal['proposalId']
        proposalUrl = self.activeProposal['url']

        for address, power in self.addresses.items():

            # If the wallet was unlocked before entering the
            # script leave it...
            if not self.unlockedBefore:
                self.rpc.unlockWallet(self.password)

            signed = self.rpc.signMessage(address, proposalUrl)

            if signed.error:
                error("Could not sign message: {}".format(signed.error))
                return False

            verified = self.rpc.verifyMessage(address, proposalUrl, signed.data)

            if verified.error:
                error("Could not verify message: {}".format(verified.error))
                return False

            # If the wallet was unlocked before entering the
            # script leave it...
            if not self.unlockedBefore:
                self.rpc.lockWallet()

            postData = {
             'proposalId': proposalId,
             'smartAddress': address,
             'signature': signed.data,
             'url' : proposalUrl,
             'voteType' : self.voteType
            }

            response = requests.post(URL_SMARTCASH + API_CAST_VOTE, data=postData )

            if response.status_code == 200:
                self.success += power
                result = "PASSED"
                message = "Voted with {} - Power {} SMART".format(address, power)
            else:
                self.failed += power
                result = "FAILED"
                message = "Could not vote with {} - {}:{}".format(address,response.status_code,response.reason)

            print("[{}] - {}".format(result, message))

        if self.success:
            print("\nVoted with {} SMART!".format(self.success))

        if self.failed:
            print("\nVotes with {} SMART failed. Try it again!".format(self.failed))

        return True

    def run(self):

        while self.state < STATE_DONE:

            if self.state == STATE_COLLECT:

                if self.collectAddresses():
                    self.state = STATE_WALLETLOCK
                else:
                    self.state = STATE_CANCELED

            elif self.state == STATE_WALLETLOCK:

                if self.checkWalletLock():
                    self.state = STATE_LOAD_PROPOSALS
                else:

                    if exit():
                        self.state = STATE_CANCELED
                    else:
                        clear()
                        continue

            elif self.state == STATE_LOAD_PROPOSALS:

                if self.loadProposals():
                    self.state = STATE_ASK_PROPOSAL
                else:
                    if exit("Do you want to try it again?"):
                        self.state = STATE_CANCELED
                    else:
                        clear()

            elif self.state == STATE_ASK_PROPOSAL:

                if self.askProposal():
                    self.state = STATE_ASK_VOTE_TYPE
                else:

                    if exit():
                        self.state = STATE_CANCELED

            elif self.state == STATE_ASK_VOTE_TYPE:

                if self.askVoteType():
                    self.state = STATE_CAST_VOTES
                else:

                    if exit():
                        self.state = STATE_CANCELED

            elif self.state == STATE_CAST_VOTES:

                if self.castVotes():

                    if exit("\nDo you want to vote again?\n"):

                        # If the wallet was unlocked before entering the
                        # script leave it up to the user to lock it again.
                        if not self.unlockedBefore:
                            self.rpc.lockWallet()

                        self.state = STATE_DONE

                    else:
                        # Ask again for the proposal to vote
                        self.state = STATE_ASK_PROPOSAL

                else:
                    error("Something went wrong during the voting process.")
                    self.state = STATE_CANCELED


        return self.state == STATE_DONE
