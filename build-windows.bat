@echo off
del /f Kwickstart.spec
rmdir /s /q build
rmdir /s /q dist
pyinstaller --clean -c -F -n Kwickstart --icon=logo.ico --uac-admin .\main.py