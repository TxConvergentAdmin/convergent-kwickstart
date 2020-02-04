@echo off
del /f Kwickstart.spec
pyinstaller --clean -c -F -n Kwickstart --icon=logo.ico --uac-admin ^
--add-data kwickstart/templates/flask.zip;templates ^
--add-data kwickstart/templates/nlptools.zip;templates ^
.\main.py