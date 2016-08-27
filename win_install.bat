@ECHO OFF
FOR /f %%p in ('where python') do SET PYTHONPATH=%%p
virtualenv -p %PYTHONPATH% --no-site-packages --distribute .env
cmd /k ".env\Scripts\activate & pip install -r requirements.txt & deactivate"
exit 0