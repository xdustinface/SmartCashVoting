#####
# Part of `SmartCashVoting`
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


import os, traceback
from smartcash.rpc import RPCConfig
from vote import SmartCashVoting
from version import __version__
import wallet
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='SmartCashVoting')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.parse_args()

    print("*" * 21)
    print("** SmartCashVoting **")
    print("**  Version {}    **".format(__version__))
    print("** by @dustinface  **")
    print("*" * 21)

    error = False

    rpcConfig = RPCConfig(wallet.rpcuser,wallet.rpcpassword)

    voting = SmartCashVoting(rpcConfig)

    try:
        error = not voting.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        error = True
        print("[ERROR] => {}".format(str(e)))
        print(traceback.format_exc())
    finally:

        if not voting.unlockedBefore:
            voting.rpc.lockWallet()

    if error:
        print("\nNeed help? Contact me:\n\n@dustinface in telegram\n@dustinface#6318 in discord")

    print(("\n\n***\n"
            "* Beer & Coffee => STsDhYJZZrVFCaA5FX2AYWP27noYo3RUjD\n"
            "***\n"))
