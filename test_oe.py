from json import load
import pyodbc
import pandas as pd
from queries import load_config

_, CONN_STRING = load_config("OE")

# show tables in db


query_2 = """
        SELECT TOP 2
                Artikel,
                SortBezeichnung,
                rowid
            
            FROM
                S_Artikel
            WHERE
                Firma = 200
            AND
                Artikel <= '103033'
            ORDER BY
                Artikel DESC

"""

conn = pyodbc.connect(CONN_STRING)
df = pd.read_sql(query_2, conn)
conn.close()

print(df)
