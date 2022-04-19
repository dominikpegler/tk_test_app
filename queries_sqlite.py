import pandas as pd
import sqlite3

SQLITE_STRING = "sqlite.db"

def get_item(input):

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
