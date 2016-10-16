@ECHO OFF
cmd /k ".env\Scripts\activate & pelican content -s pelicanconf.py & deactivate"
exit 0