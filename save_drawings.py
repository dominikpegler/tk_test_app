import json
import shutil
from pathlib import Path

try:
    with open("./config.json", "r", encoding="utf-8") as config_file:
        config_data = json.load(config_file)

    PDF_DIR = config_data["PDF_DIR"]
    DWG_DIR = config_data["DWG_DIR"]

except Exception as e:
        print("Problem beim Laden der Folder-Konfiguration (" + str(e) + ")")
        PDF_DIR = ""
        DWG_DIR = ""

def save_pdf(file,PDF_DIR):
    try:
        shutil.copy(PDF_DIR + file, Path.joinpath(Path.home(), "Desktop"))
    except Exception as e:
        return "Err", f"Fehler beim Speichern der PDF-Datei ({e})"

    return "Ok", "PDF gespeichert."


def save_dwg(file,DWG_DIR):
    try:
        shutil.copy(DWG_DIR + file, Path.joinpath(Path.home(), "Desktop"))
    except Exception as e:
        return "Err", f"Fehler beim Speichern der DWG-Datei ({e})"

    return "Ok", "DWG gespeichert."
