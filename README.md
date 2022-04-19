# tk_test_app
a primitive tkinter app that you can quickly use for various tasks

## compile to exe with pyinstaller

creates executables in dist/ directory

### standard

`pyinstaller --windowed --clean -i icon.ico --add-data "icon.ico;." --add-data "config.json;." app.py`

### only one file option

- make sure that icon.ico and config files (e.g. config.json) are also available at location of app.exe
- --icon / -i option will not work with onefile

`pyinstaller --onefile --windowed --clean app.py`

## compile to exe with cx_Freeze

creates executables in build/ directory

### standard

`python3 setup.py build`

### create msi installer for windows

`python3 setup.py bdist_msi`

### create mac disk image

`python3 setup.py bdist_dmg`
