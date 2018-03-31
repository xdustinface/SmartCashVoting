# SmartCashVoting
Python script to vote with all your voting power in one shot.

**This no official SmartCash script. PLEASE ONLY use the version you installed by yourself
from this repo and never any version you got from somewhere/someone else. This script requires
your wallet to be unlocked with an local RPC server enabled which means any malicious modification of this script could empty your wallet!**

**Use it with care and sanity! I cant take over any responsibilities for your funds.**

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

## Configuration of your wallet
To be able to use this script you need to enable the local RPC server of your wallet. To do this
you need to **append** the following lines to the `smartcash.conf` in your wallets data directory.

```
rpcuser=someusername
rpcpassword=somepassword
rpcallowip=127.0.0.1
server=1
```

Replace `someusername` and `somepassword` with your desired ones.

**You need to restart the wallet afterwards**

# Install by script

## Linux

First make sure `python` and `python-setuptools` are installed and up to date

```
sudo apt install python python-setuptools
```

then change the directory to the path where you want to store the installed files like `cd ~/MySmartCashStuff` and run:

```
curl -LSs https://gist.githubusercontent.com/xdustinface/94350c0eca48638d9e4d34e0f6218524/raw | bash
```

this will create a folder named `SmartCashVoting-x.x` where the script will be located.

# macOS

Im currently don't have the chance to test the install script on a clean mac. My one is already infested with all those stuff. I think the best way to go is just using the python installation provided per default by apple. Just make sure your python setuptools are up to date. In your terminal run

```
python -m pip install --upgrade pip setuptools
```

then change the directory to the path where you want to store the installed files like `cd ~/MySmartCashStuff` and run:

```
curl -LSs https://gist.githubusercontent.com/xdustinface/94350c0eca48638d9e4d34e0f6218524/raw | bash
```

this will create a folder named `SmartCashVoting-x.x` where the script will be located.

## Windows

To use this script on windows you will have to install python. To do this download either
Python 2 or Python 3.
https://www.python.org/downloads/

 **During the installation select Add python to PATH**

Then open the windows powershell, change the directory to the path where you want to
store the installed files like `cd ~/MySmartCashStuff`

```
Invoke-WebRequest https://gist.github.com/xdustinface/da980926115e45f6e53010b68fdb9cd2/raw -OutF
ile install_voting.ps1
```

to download the install file. If you receive any TLS error here run the following and try it again

```
$AllProtocols = [System.Net.SecurityProtocolType]'Tls11,Tls12'
[System.Net.ServicePointManager]::SecurityProtocol = $AllProtocols
```

If you got no error just run

```
powershell .\install_voting.ps1
```

And follow the instructions.

## Install by yourself

If you have any concerns about the install scripts you can simply install my `python-smartcash` package. Its not yet
available as pip package so just either clone the git repo and checkout the tag `v0.0.1`

```
git clone git@github.com:xdustinface/python-smartcash.git
git checkout tags/v0.0.1
```

or just download the archive

https://github.com/xdustinface/python-smartcash/archive/v0.0.1.zip

https://github.com/xdustinface/python-smartcash/archive/v0.0.1.tar.gz

then go into the directory and run `python setup.py install`

To clone/download this repo

```
git clone git@github.com:xdustinface/SmartCashVoting.git
cd SmartCashVoting
```

or to download the archived file from here:

https://github.com/xdustinface/SmartCashVoting/archive/master.zip

https://github.com/xdustinface/SmartCashVoting/archive/master.tar.gz

extract and open the file `wallet.py` to change the variables

```
rpcuser="someusername"
rpcpassword="somepassword"
```

so that they match the entries in your `smartcash.conf`

Done!

## Vote!

Just start the script with

```
python SmartCashVoting.py
```

Windows user can also just right click the `run_windows.ps1` file and then press
`Run with powershell`.

Now follow the instructions and go voting with your full power! :)

# Beer, coffee and further development
If you enjoy it and you are feeling the urge to tip me...go ahead :D

SMART STsDhYJZZrVFCaA5FX2AYWP27noYo3RUjD

BTC 1Hx9aPhHuKojtVqeFseUejMqnM87xTKDx1

ETH 0xFf2ED74286a5686Bc4F4896761718DE0316884fA
