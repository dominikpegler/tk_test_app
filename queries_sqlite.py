import pandas as pd
import sqlite3
import json


def load_config():

    try:
        with open("./config.json", "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        SQLITE_STRING = config_data["SQLITE_STRING"]

        if SQLITE_STRING == "":
            raise ValueError("SQLITE_STRING cannot be empty string")

    except Exception as e:
        output = "Problem beim Laden der Konfiguration (" + str(e) + ")"
        return ("Err",output)

    return ("Ok", SQLITE_STRING)


def get_item(input,SQLITE_STRING):

    query = (
        f"""
            SELECT

                SortBezeichnung
            
            FROM
                S_Artikel
            WHERE
                Firma = 200
            AND
                Artikel = '{input}'

            LIMIT 1
    
    """
        
    )

    try:
        conn_sl = sqlite3.connect(SQLITE_STRING)

    except Exception as e:
        output = "Verbindung zu Datenbank fehlgeschlagen " + "(" + str(e) + ")"
        return "Err", output

    try:
        df = pd.read_sql(query, conn_sl)
    except Exception as e:
        output = "Datenbankabfrage fehlerhaft " + "(" + str(e) + ")"
        return "Err", output

    if len(df) == 1:
        output = df.iloc[0, 0]
    elif len(df) > 1:
        output = "Fehler in Abfrage"
    else:
        output = "Artikel nicht gefunden"

    conn_sl.close()

    return "Ok", output
