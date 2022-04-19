import platform
import pandas as pd
import pyodbc
import json


NO_LOCK = " WITH (NOLOCK)"

def load_config():

    try:
        with open("./config.json", "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        OPENEDGE_11_STRING_WIN = config_data["OPENEDGE_11_STRING_WIN"]
        OPENEDGE_11_STRING_LNX = config_data["OPENEDGE_11_STRING_LNX"]

        if platform.system() == "Windows":
            OPENEDGE_STRING = OPENEDGE_11_STRING_WIN
        else:
            OPENEDGE_STRING = OPENEDGE_11_STRING_LNX

        if OPENEDGE_STRING == "":
            raise ValueError("OPENEDGE_STRING cannot be empty string")

    except Exception as e:
        output = "Problem beim Laden der Konfiguration (" + str(e) + ")"
        return ("Err",output)

    return ("Ok", OPENEDGE_STRING)


def get_item(input, OPENEDGE_STRING):

    query = (
        f"""
            SELECT TOP 1

                SortBezeichnung
            
            FROM
                S_Artikel
            WHERE
                Firma = 200
            AND
                Artikel = '{input}'
    
    """
        + NO_LOCK
    )

    try:
        conn_oe = pyodbc.connect(OPENEDGE_STRING)

    except Exception as e:
        output = "Verbindung zu Datenbank fehlgeschlagen" + "(" + str(e) + ")"
        return "Err", output

    df = pd.read_sql(query, conn_oe)

    if len(df) == 1:
        output = df.iloc[0, 0]
    elif len(df) > 1:
        output = "Fehler in Abfrage"
    else:
        output = "Artikel nicht gefunden"

    conn_oe.close()

    return "Ok", output
