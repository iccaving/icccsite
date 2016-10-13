@ECHO OFF
set /p username=Username?:
REM Get passoword in a nice-ish masked way
powershell -Command $pword = read-host "Enter password" -AsSecureString ; $BSTR=[System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pword) ; [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR) > .tmp.txt & set /p password=<.tmp.txt & del .tmp.txt
echo open %username%@dougal.union.ic.ac.uk 10022 > psftp.txt
echo put -r output /home/www/htdocs/rcc/caving >> psftp.txt
REM echo %CD% >> psftp.txt
psftp.exe -pw %password% -b psftp.txt
if exist psftp.txt del psftp.txt
pause