import sqlite3
import pandas as pd
import time

start = time.time()
# show tables in db


query = """

SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;

"""

query_2 = """
         SELECT
                S_Artikel.Artikel,
                S_ArtikelSpr.Bezeichnung
            
            FROM
                S_Artikel

            LEFT JOIN
                S_ArtikelSpr
            ON
                S_Artikel.Firma = S_ArtikelSpr.Firma
            AND
                S_Artikel.Artikel = S_ArtikelSpr.Artikel

            WHERE
                S_Artikel.Firma = 200
            AND
                S_Artikel.Artikel = '103033'
            AND
                Sprache = 'D'

            LIMIT 1
"""


conn = sqlite3.connect("sqlite.db")
df = pd.read_sql(query_2, conn)
conn.close()

print(df)

print("\n\n", "Time:", format((time.time() - start) * 1000, ".0f"), "ms", "\n")
