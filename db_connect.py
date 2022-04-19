import sqlite3
import pandas as pd

query = '''

SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;

'''

conn = sqlite3.connect("sqlite.db")
df = pd.read_sql(query, conn)
conn.close()

print(df)