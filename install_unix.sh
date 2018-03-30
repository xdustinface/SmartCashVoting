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

echo 'Installing SmartCashVoting...'

if hash python 2>/dev/null ; then
    echo 'Python found! Download python-smartcash lib now...'

    url='https://github.com/xdustinface/python-smartcash/archive/v0.0.1.tar.gz'
    archive='python-smartcash.tar.gz'

    wget $url -O $archive 2>/dev/null || curl -sL $url -o $archive

    tar -xf $archive
    rm $archive

    echo "Enter the rpc user from your smartcash.conf.."

    read -p "rpcuser: " rpcuser </dev/tty

    echo "Enter the rpc password from your smartcash.conf.."
    read -p "rpcpassword: " rpcpassword </dev/tty

    sed -i "s/rpcuser=.*/rpcuser=\"${rpcuser}\"/g" wallet.py
    sed -i "s/rpcpassword=.*/rpcpassword=\"${rpcpassword}\"/g" wallet.py

    cd python-smartcash-0.0.1/

    echo 'Installing python-smartcash...'

    python setup.py install --user

    echo 'Done! Now you can start the python SmartCashVoting.py to run the voting script.'
else
    echo 'Canceled. You need to install python first!'
fi
