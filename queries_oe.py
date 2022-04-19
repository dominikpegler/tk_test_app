import platform
import pandas as pd
import pyodbc
import json


with open("./config.json", "r", encoding="utf-8") as config_file:
    config_data = json.load(config_file)

NO_LOCK = " WITH (NOLOCK)"
OPENEDGE_11_STRING_WIN = config_data["OPENEDGE_11_STRING_WIN"]
OPENEDGE_11_STRING_LNX = config_data["OPENEDGE_11_STRING_LNX"]

if platform.system() == "Windows":
    OPENEDGE_STRING = OPENEDGE_11_STRING_WIN
else:
    OPENEDGE_STRING = OPENEDGE_11_STRING_LNX

if OPENEDGE_STRING == "":
    raise ValueError("OPENEDGE_STRING cannot be empty string")


print(OPENEDGE_STRING)


def get_item(input):

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

    conn_oe = pyodbc.connect(OPENEDGE_STRING)
    df = pd.read_sql(query, conn_oe)

    if len(df) == 1:
        output = df.iloc[0, 0]
    elif len(df) > 1:
        output = "Fehler in Abfrage"
    else:
        output = "Artikel nicht gefunden"

    conn_oe.close()

    return output
