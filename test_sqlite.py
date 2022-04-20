import sqlite3
import pandas as pd

# show tables in db

query = """

SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;

"""

query_2 = """
         SELECT

                SortBezeichnung
            
            FROM
                S_Artikel
            WHERE
                Firma = 200
            AND
                Artikel = '103033'

            LIMIT 1
"""

query_3 = """
            SELECT
                Artikel_prior,
                SortBezeichnung_prior

            FROM (
                SELECT
                    Artikel,
                    SortBezeichnung,
                    LAG(Artikel) over (order by Artikel) as Artikel_prior,
                    LAG(SortBezeichnung) over (order by Artikel) as SortBezeichnung_prior
                FROM
                    S_Artikel
            ) AS t
            
            WHERE
                Artikel = '103033'

"""

query_4 = """
            SELECT
                Artikel_next,
                SortBezeichnung_next

            FROM (
                SELECT
                    Artikel,
                    SortBezeichnung,
                    LEAD(Artikel) over (order by Artikel) as Artikel_next,
                    LEAD(SortBezeichnung) over (order by Artikel) as SortBezeichnung_next
                FROM
                    S_Artikel
            ) AS t
            
            WHERE
                Artikel = '103033'

"""

conn = sqlite3.connect("sqlite.db")
df = pd.read_sql(query, conn)
conn.close()

print(df)
