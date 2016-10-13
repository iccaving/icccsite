@ECHO OFF
cmd /k ".env\Scripts\activate & pelican content -s publishconf.py & deactivate"
exit 0