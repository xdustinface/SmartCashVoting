# SmartCashVoting

Python script to vote with all your voting power in one shot.

**This no official SmartCash script. PLEASE ONLY use the version you cloned by yourself
from this repo and never any version you got from somewhere/someone else. This script requires
your wallet to be unlocked which means any modification could empty your wallet!**

## What?
This is attempt to increase the overall voting power for the SmartCash voting portal.
I assume people who have split their SMART's into many addresses (Nodes, SmartRewards or whatever reasons)
currently don't have the most motivation to vote with their full power. With this script
you can cast votes with your overall voting power in one shot.

- This script uses the RPC interface of your desktop wallet fetch all addresses with SMART holdings.
- Pulls the required data from the voting portal: https://vote.smartcash.cc.
- Asks you which proposal you want to vote.
- Signs all the required voting message for each of your addresses with the RPC interface.
- Casts all votes consecutively without any action of yourself required.

## Configuration of you wallet
To be able to use this script you need to enable the RPC server of your wallet. To do this
you need to append the following lines to the `smartcash.conf` in your wallets data directory.

```
rpcuser=someusername
rpcpassword=somepassword
rpcallowip=127.0.0.1
listen=1
server=1
```

Replace `someusername` and `somepassword` with your desired ones.

**You need to restart the wallet afterwards**

## Python for Windows

To use this script on windows you will have to install python. To do this download either
Python 2 or Python 3.
https://www.python.org/downloads/

 **During the installation select Add python to PATH**

## Python for macOS and Linux
As mac/linux user you just need to use your terminal and follow the next steps. Python should be available
there :)

## Install python-smartcash

To use this script you need to install my `python-smartcash` package. Its not yet
available as pip package so just either clone the git repo and checkout the tag `v0.0.1`

```
git clone git@github.com:xdustinface/python-smartcash.git
git checkout tags/v0.0.1
```

or just download the zip

https://github.com/xdustinface/python-smartcash/archive/v0.0.1.zip

then go into the directory and run `python setup.py install`

## Vote!

To run the voting script you now just need to run

```
git clone git@github.com:xdustinface/SmartCashVoting.git
cd SmartCashVoting
```
or like above you can download the zipped file from here:

https://github.com/xdustinface/SmartCashVoting/archive/v0.0.1.zip

then open the file `wallet.py` and change the variables

```
rpcuser="someusername"
rpcpassword="somepassword"
```

that they match the values you entered in your wallets `smartcash.conf`.

Now just start the script with:

```
python SmartCashVoting.py
```

# Beer, coffee and further development
If you enjoy it and you are feeling the urge to tip me...go ahead :D

SMART STsDhYJZZrVFCaA5FX2AYWP27noYo3RUjD

BTC 1Hx9aPhHuKojtVqeFseUejMqnM87xTKDx1

ETH 0xFf2ED74286a5686Bc4F4896761718DE0316884fA
