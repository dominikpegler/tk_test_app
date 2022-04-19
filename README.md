# tk_test_app
a primitive tkinter app that you can quickly use for various tasks

## compile to exe

`pyinstaller --windowed --clean -i icon.ico --add-data "icon.ico;." app.py`

## compile to exe with `onefile` option

- make sure that icon.ico is also available at location of app.exe
- --icon / -i option will not work with onefile

`pyinstaller --onefile --windowed --clean app.py`