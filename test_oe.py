from collections import namedtuple
from json import load
from typing import NamedTuple
import pyodbc
import pandas as pd
from queries import load_config
import time

start = time.time()

_, CONN_STRING = load_config("OE")


query = """
         SELECT TOP 1
                S_Artikel.Artikel,
                S_ArtikelSpr.Bezeichnung,
                P_ZeichnungArtikel.Zeichnung,
                PMM_Drawing.IndexNo AS 'IndexNr',
                PMM_Drawing.ImageNumber AS 'BildNummer',
                PMM_Drawing.CadNumber AS 'CADNummer'
    
            FROM
                S_Artikel

            LEFT JOIN
                S_ArtikelSpr
            ON
                S_Artikel.Firma = S_ArtikelSpr.Firma
            AND
                S_Artikel.Artikel = S_ArtikelSpr.Artikel

            LEFT JOIN
                P_ZeichnungArtikel
            ON
                S_Artikel.Firma=P_ZeichnungArtikel.Firma
            AND
                S_Artikel.Artikel=P_ZeichnungArtikel.Artikel
                
            LEFT JOIN
                PMM_Drawing
            ON
                P_ZeichnungArtikel.Firma=PMM_Drawing.Company
            AND
                P_ZeichnungArtikel.Zeichnung=PMM_Drawing.PMM_Drawing_ID

            LEFT JOIN
                PMM_DrawingMaster
            ON
                PMM_Drawing.Company=PMM_DrawingMaster.Company
            AND
                PMM_Drawing.PMM_DrawingMaster_Obj=PMM_DrawingMaster.PMM_DrawingMaster_Obj

            WHERE
                S_Artikel.Firma = 200
            AND
                S_Artikel.Artikel = '144386'
            AND
                Sprache = 'D'
            AND
                (P_ZeichnungArtikel.Hauptzeichnung=1 OR P_ZeichnungArtikel.Hauptzeichnung IS NULL)

"""

input = "159400"

no_lock = " WITH (NOLOCK)"

operator = "<="
ordered = ""

limited = ""
top = " TOP 2 "

backwards_query = f"""
            
            SELECT {top}
                S_Artikel.Artikel,
                S_ArtikelSpr.Bezeichnung,
                P_ZeichnungArtikel.Zeichnung,
                PMM_Drawing.IndexNo AS 'IndexNr',
                PMM_Drawing.ImageNumber AS 'BildNummer',
                PMM_Drawing.CadNumber AS 'CADNummer'
    
            FROM
                S_Artikel

            LEFT JOIN
                S_ArtikelSpr
            ON
                S_Artikel.Firma = S_ArtikelSpr.Firma
            AND
                S_Artikel.Artikel = S_ArtikelSpr.Artikel

            LEFT JOIN
                P_ZeichnungArtikel
            ON
                S_Artikel.Firma=P_ZeichnungArtikel.Firma
            AND
                S_Artikel.Artikel=P_ZeichnungArtikel.Artikel
                
            LEFT JOIN
                PMM_Drawing
            ON
                P_ZeichnungArtikel.Firma=PMM_Drawing.Company
            AND
                P_ZeichnungArtikel.Zeichnung=PMM_Drawing.PMM_Drawing_ID

            LEFT JOIN
                PMM_DrawingMaster
            ON
                PMM_Drawing.Company=PMM_DrawingMaster.Company
            AND
                PMM_Drawing.PMM_DrawingMaster_Obj=PMM_DrawingMaster.PMM_DrawingMaster_Obj

            WHERE
                S_Artikel.Firma = 200
            AND
                S_Artikel.Artikel {operator} '{input}'
            AND
                S_ArtikelSpr.Sprache = 'D'
            AND
                (P_ZeichnungArtikel.Hauptzeichnung=1 OR P_ZeichnungArtikel.Hauptzeichnung IS NULL)

            ORDER BY
                S_Artikel.Artikel DESC,
                S_Artikel.Firma DESC,
                P_ZeichnungArtikel.Zeichnung DESC,
                PMM_Drawing.PMM_Drawing_ID DESC,
                PMM_Drawing.PMM_DrawingMaster_Obj DESC,
                S_ArtikelSpr.Sprache DESC,
                P_ZeichnungArtikel.Hauptzeichnung DESC



            {limited}

            {no_lock}

            """

conn = pyodbc.connect(CONN_STRING)
# df = pd.read_sql(backwards_query, conn)
conn.close()

# print(df)


print("\n\n", "Time:", format((time.time() - start) * 1000, ".0f"), "ms", "\n")

# import json
# import shutil

# from pathlib import Path

# with open("./config.json", "r", encoding="utf-8") as config_file:
#     config_data = json.load(config_file)

# PDF_DIR = config_data["PDF_DIR"]
# DWG_DIR = config_data["DWG_DIR"]

# pdf_file = PDF_DIR + df.BildNummer.values[0]
# shutil.copy(pdf_file, Path.joinpath(Path.home(), "Desktop"))
