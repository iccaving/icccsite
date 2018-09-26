@ECHO OFF
cmd /k ".env\Scripts\activate & olm -s olmset.py -r -l INFO . & deactivate"
exit 0
