#/bin/bash

pyinstaller --windowed --clean -i icon.ico --add-data "icon.ico;." --add-data "config.json;." app.py

