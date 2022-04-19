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

    conn_sl = sqlite3.connect(SQLITE_STRING)
    df = pd.read_sql(query, conn_sl)

    if len(df) == 1:
        output = df.iloc[0, 0]
    elif len(df) > 1:
        output = "Fehler in Abfrage"
    else:
        output = "Artikel nicht gefunden"

    conn_sl.close()

    return output
