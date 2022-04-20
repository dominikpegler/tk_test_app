import pandas as pd
import sqlite3
import pyodbc
import json
import platform


def load_config(DB):

    try:
        with open("./config.json", "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        if DB == "SL":
            CONN_STRING = config_data["SQLITE_STRING"]

            if CONN_STRING == "":
                raise ValueError("SQLITE_STRING cannot be empty string")
        elif DB == "OE":
            OPENEDGE_11_STRING_WIN = config_data["OPENEDGE_11_STRING_WIN"]
            OPENEDGE_11_STRING_LNX = config_data["OPENEDGE_11_STRING_LNX"]

            if platform.system() == "Windows":
                CONN_STRING = OPENEDGE_11_STRING_WIN
            else:
                CONN_STRING = OPENEDGE_11_STRING_LNX

            if CONN_STRING == "":
                raise ValueError("OPENEDGE_STRING cannot be empty string")

        else:
            raise ValueError(f"DB can only be 'SL' or 'OE', but is {repr(DB)}.")

    except Exception as e:
        output = "Problem beim Laden der Konfiguration (" + str(e) + ")"
        return ("Err", output)

    return ("Ok", CONN_STRING)


def get_item(input, CONN_STRING, DB):

    no_lock = " WITH (NOLOCK)" if DB == "OE" else ""
    limited = " LIMIT 1 " if DB == "SL" else ""
    top = " TOP 1 " if DB == "OE" else ""

    query = f"""
            
            SELECT {top}
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
                S_Artikel.Artikel = '{input}'
            AND
                Sprache = 'D'
            AND
                (P_ZeichnungArtikel.Hauptzeichnung=1 OR P_ZeichnungArtikel.Hauptzeichnung IS NULL)

            {limited}

            {no_lock}

            """

    try:
        conn = (
            pyodbc.connect(CONN_STRING) if DB == "OE" else sqlite3.connect(CONN_STRING)
        )

    except Exception as e:
        output = "Verbindung zu Datenbank fehlgeschlagen " + "(" + str(e) + ")"
        return "Err", output

    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        output = "Datenbankabfrage fehlerhaft " + "(" + str(e) + ")"
        return "Err", output

    if len(df) == 1:
        name, drawing, idx, img, cad = df.iloc[0, 0:5]
        name = name.replace(";", "\n")
        output = (name, drawing, idx, img, cad)
    elif len(df) > 1:
        output = ("Fehler in Abfrage",)
    else:
        output = ("Artikel nicht gefunden",)

    conn.close()

    return "Ok", output


def get_next_item(input, keysym, CONN_STRING, DB):

    no_lock = " WITH (NOLOCK)" if DB == "OE" else ""

    if keysym in ["Prior", "Up"]:
        operator = "<="
        ordered = " ORDER BY S_Artikel.Artikel DESC "
    elif keysym in ["Next", "Down"]:
        operator = ">="
        ordered = " "
    else:
        output = f"event.keysym kann nur 'Up', 'Down', 'Prior' oder 'Next' sein, ist aber {str(keysym)}. Check Code!"
        return "Err", (input, output)

    limited = " LIMIT 2 " if DB == "SL" else ""
    top = " TOP 2 " if DB == "OE" else ""

    query = f"""
            
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
                Sprache = 'D'
            AND
                (P_ZeichnungArtikel.Hauptzeichnung=1 OR P_ZeichnungArtikel.Hauptzeichnung IS NULL)

            {ordered}

            {limited}

            {no_lock}

            """

    try:
        conn = (
            pyodbc.connect(CONN_STRING) if DB == "OE" else sqlite3.connect(CONN_STRING)
        )

    except Exception as e:
        output = "Verbindung zu Datenbank fehlgeschlagen " + "(" + str(e) + ")"
        return "Err", (input, output)

    try:
        df = pd.read_sql(query, conn)
    except Exception as e:
        output = "Datenbankabfrage fehlerhaft " + "(" + str(e) + ")"
        return "Err", (input, output)

    if len(df) == 1:
        input_new, name, drawing, idx, img, cad = df.iloc[0, 0:6]
        name = name.replace(";", "\n")
        output = (input_new, name, drawing, idx, img, cad)
    elif len(df) == 2:
        input_new, name, drawing, idx, img, cad = df.iloc[1, 0:6]
        name = name.replace(";", "\n")
        output = (input_new, name, drawing, idx, img, cad)
    elif len(df) > 2:
        output = (input, "Fehler in Abfrage")
    else:
        output = (input, "Artikel nicht gefunden")

    conn.close()

    return "Ok", output
