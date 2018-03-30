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


if(Test-CommandExists python)
{
    $AllProtocols = [System.Net.SecurityProtocolType]'Tls11,Tls12'
    [System.Net.ServicePointManager]::SecurityProtocol = $AllProtocols

    echo "`r`nPython found! Download python-smartcash lib now...`r`n"

    Invoke-WebRequest https://github.com/xdustinface/python-smartcash/archive/v0.0.1.zip -OutFile python-smartcash.zip

    if (Test-Path /python-smartcash-0.0.1/ -PathType Container) {
		Remove-Item -path python-smartcash-0.0.1/ -recurse -force
	}

    Expand-Archive -Path python-smartcash.zip -DestinationPath ./
    Remove-Item python-smartcash.zip

    cd python-smartcash-0.0.1/

    echo "`r`nInstalling python-smartcash...`r`n"

    python setup.py install;

    cd ../

    Get-Item "\\$_\C$\Program Files\My Application\MyApp.ini" \\} |

    Replace-FileString -Pattern 'Server=appserver1(\r\n)Port=7840'

    -Replacement 'rpcuser=test' -Overwrite

    Read-Host -Prompt "`r`nDone! Now you can start the run_windows.ps1 to run the voting script."
}
else
{
    echo "`r`n`r`nYou need to install python first!`r`n`r`nhttps://www.python.org/downloads/`r`n`r`n"
    echo "NOTE: You need to select - Add python.exe to Path - during the installation`r`n"
    Read-Host -Prompt "Press Enter to exit"
}
