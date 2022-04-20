import json
import shutil
from pathlib import Path

with open("./config.json", "r", encoding="utf-8") as config_file:
    config_data = json.load(config_file)

PDF_DIR = config_data["PDF_DIR"]
DWG_DIR = config_data["DWG_DIR"]


def save_pdf(file):
    try:
        shutil.copy(PDF_DIR + file, Path.joinpath(Path.home(), "Desktop"))
    except Exception as e:
        return "Err", f"Fehler beim Speichern der PDF-Datei ({e})"

    return "Ok", "PDF gespeichert."


def save_dwg(file):
    try:
        shutil.copy(DWG_DIR + file, Path.joinpath(Path.home(), "Desktop"))
    except Exception as e:
        return "Err", f"Fehler beim Speichern der DWG-Datei ({e})"

    return "Ok", "DWG gespeichert."
