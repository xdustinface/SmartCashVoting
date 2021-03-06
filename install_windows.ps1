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

Function Test-CommandExists

{

 Param ($command)

 $oldPreference = $ErrorActionPreference

 $ErrorActionPreference = 'stop'

 try {if(Get-Command $command){RETURN $true}}

 Catch {RETURN $false}

 Finally {$ErrorActionPreference=$oldPreference}

}

$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$libversion = "0.0.2"

if(Test-CommandExists python)
{
    $AllProtocols = [System.Net.SecurityProtocolType]'Tls11,Tls12'
    [System.Net.ServicePointManager]::SecurityProtocol = $AllProtocols

    echo "`r`nPython found! Download python-smartcash lib now...`r`n"

    Invoke-WebRequest https://github.com/xdustinface/python-smartcash/archive/v${libversion}.zip -OutFile $scriptPath\python-smartcash.zip

    if( $? ){

        if (Test-Path $scriptPath\python-smartcash-0.0.2/ -PathType Container) {
		    Remove-Item -path $scriptPath\python-smartcash-0.0.2/ -recurse -force
	    }

        Expand-Archive -Path $scriptPath\python-smartcash.zip -DestinationPath $scriptPath
        Remove-Item $scriptPath\python-smartcash.zip

        $rpcuser = Read-Host 'Enter the rpc user from your smartcash.conf: '
        $rpcpassword = Read-Host 'Enter the rpc password from your smartcash.conf: '

        (Get-Content $scriptPath\wallet.py) `
            -replace 'rpcuser=.*', $('rpcuser="' + $rpcuser + '"') `
            -replace 'rpcpassword=.*', $('rpcpassword="' + $rpcpassword + '"') |
            Out-File -Encoding "UTF8" $scriptPath\wallet.py

        cd $scriptPath\python-smartcash-0.0.2

        echo "`r`nInstalling python-smartcash...`r`n"

        python setup.py install

        Read-Host -Prompt "`r`nDone! Now you can start the run_windows.ps1 to run the voting script."

    }else{
        echo "[ERROR] Could not download python-smartcash v${libversion}."
    }

}
else
{
    echo "`r`n`r`nYou need to install python first!`r`n`r`nhttps://www.python.org/downloads/`r`n`r`n"
    echo "NOTE: You need to select - Add python.exe to Path - during the installation`r`n"
    Read-Host -Prompt "Press Enter to exit"
}
