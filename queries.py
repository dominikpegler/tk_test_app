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

    NO_LOCK = " WITH (NOLOCK)" if DB == "OE" else ""

    query_sl = f"""
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

    query_oe = (
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

    query = query_oe if DB == "OE" else query_sl

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
        output = df.iloc[0, 0]
    elif len(df) > 1:
        output = "Fehler in Abfrage"
    else:
        output = "Artikel nicht gefunden"

    conn.close()

    return "Ok", output


def get_next_item(input, keysym, CONN_STRING, DB):

    no_lock = " WITH (NOLOCK)" if DB == "OE" else ""

    if keysym in ["Prior", "Up"]:
        operator = "<="
        ordered = " ORDER BY Artikel DESC "
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
                Artikel,
                SortBezeichnung

            FROM
                S_Artikel
            
            WHERE
                Artikel {operator} '{input}'
            AND
                Firma = 200

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
        output = tuple(df.iloc[0, 0:2])
    elif len(df) == 2:
        output = tuple(df.iloc[1, 0:2])
    elif len(df) > 2:
        output = (input, "Fehler in Abfrage")
    else:
        output = (input, "Artikel nicht gefunden")

    conn.close()

    return "Ok", output
