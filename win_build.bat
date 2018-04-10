@ECHO OFF
cmd /k ".env\Scripts\activate & olm -s olmset.py -l INFO . & deactivate"
exit 0
