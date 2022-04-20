import sys
from cx_Freeze import setup, Executable

APP_NAME = "ProLite App"
APP_VERSION = "0.0.1"

build_exe_options = {
    "include_files": ["icon.ico", "config.json"],
}

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "This is a description", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icon.ico"),
    ],
}

bdist_msi_options = {
    "add_to_path": False,
    "all_users": False,
    "data": msi_data,
    "upgrade_code": "{69f53468-5152-4897-9757-2386c0d99dfd}",
    "install_icon": "icon.ico",
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name=APP_NAME,
    version=APP_VERSION,
    description="",
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[
        Executable(
            "app.py",
            icon="icon.ico",
            shortcut_name=APP_NAME,
            shortcut_dir="DesktopFolder",
            base=base,
        )
    ],
)
