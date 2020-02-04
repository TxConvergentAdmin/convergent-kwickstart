#!/bin/bash
/Library/Frameworks/Python.framework/Versions/3.8/bin/pyinstaller --clean -c -F -n Kwickstart --icon=logo.ico \
    --add-data kwickstart/templates/flask.zip;templates \
    --add-data kwickstart/templates/nlptools.zip;templates \
    ./main.py