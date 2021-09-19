"""
Load the Database to memory. 
"""

import warnings
import pandas as pd

from app import APPLOG
from app.base import App, MainApplication
from core.create_db import createBomDB
from core.settings import (
    DB_DIR,
    BOM_DATA_DIR,
    ITEM_DATA_DIR,
    ARTICLE_RATES_DIR,
    DB_MOD,
    ARTLIST_DIR,
    SQL_T_ARTLIST,
    SQL_T_BOM,
    SQL_DB_DIR,
)


DB_CONNECTION = None
ERROR_STYLE = """
>>  Unexpected error occured..!! #{1}
BEGINING OF ERROR .....................................
{0}
....................................... ENDING OF ERROR
"""


def loadDatabase(root: App = None) -> None:
    """Load DB from data folder"""
    global DB_CONNECTION
    articles_db = pd.DataFrame()
    art_list = None

    if not DB_MOD == "CSV":
        import sqlite3

        try:
            DB_CONNECTION = sqlite3.connect(SQL_DB_DIR)
        except Exception as e:
            APPLOG.append(">>  UNABLE TO CONNECT TO DATABASE.")
            APPLOG.append(">>  Try these:")
            APPLOG.append(">>      Close if another instance of this app is running.")
            APPLOG.append(">>      Check whether you have read permission to the DB.")
            APPLOG.append(">>      Someone else is currently using the same DB.")
            APPLOG.append(ERROR_STYLE.format(e, ""))

    APPLOG.append(">>  Loading database ....")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    db, artlist_db = readDatabase(root)

    if db.empty:
        APPLOG.append(">>  FAILED TO CREATE DATABASE")
        APPLOG.append(">>  Terminating ..")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        return
    APPLOG.append(">>  A new database successfully created and loaded.")

    APPLOG.append(f">>  Looking up for Articles rate file...")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    articles_db = readFile(ARTICLE_RATES_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    if not root:
        return db, artlist_db, articles_db

    APPLOG.append("App ready!")
    if not artlist_db.empty:
        art_list = dict(zip(artlist_db["fathername"], artlist_db["father"]))
    root.forgetLog()
    if not articles_db.empty:
        articles_db["article"] = articles_db["article"].str.lower()
        articles_db.fillna(0)
    else:
        APPLOG.append("Article's rates missing! Cannot calculate costs accuarately.")
    MainApplication(root, db, articles_db, art_list).pack()


def createAndLoadDB(root: App):
    """Load external Bom, Materials for creating db"""

    bom_db = pd.DataFrame()
    items_db = pd.DataFrame()

    bom_db = readFile(BOM_DATA_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    items_db = readFile(ITEM_DATA_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    if items_db.empty and bom_db.empty:
        APPLOG.append(">>  ERROR OCCURED WHILE FETCHING DATA")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        return pd.DataFrame()
    APPLOG.append(">>  Creating new database..")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    df, art_df = createBomDB(bom_db, items_db)

    return (df, art_df)


def readDatabase(root=None) -> tuple:
    """Read data from db."""
    df = a_df = pd.DataFrame()

    try:
        if not DB_CONNECTION:
            df = pd.read_csv(DB_DIR, low_memory=False)
            a_df = pd.read_csv(ARTLIST_DIR, low_memory=False)
        else:
            df = pd.read_sql(f"SELECT * FROM {SQL_T_BOM}", DB_CONNECTION)
            a_df = pd.read_sql(f"SELECT * FROM {SQL_T_ARTLIST}", DB_CONNECTION)
    except (FileNotFoundError, pd.io.sql.DatabaseError):
        APPLOG.append(">>  No Database found..!")
        APPLOG.append(">>  Creating new database... be patient, it will take a while.")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        df, a_df = createAndLoadDB(root)

    except IOError:
        APPLOG.append(f">>  Permission denied for reading DB.")

    except Exception as e:
        APPLOG.append(ERROR_STYLE.format(e, ""))

    finally:
        if DB_CONNECTION:
            DB_CONNECTION.close()
        if not root:
            print(">>  Database loaded successfully")
    return df, a_df


def readFile(dir: str) -> pd.DataFrame:
    """
    Try to read external csv/excel file.
    """
    df = pd.DataFrame()

    try:
        if dir.split(".")[-1] == "csv":
            df = pd.read_csv(dir, low_memory=False)

        elif dir.split(".")[-1] in ["xlsx", "xls"]:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(dir, engine="openpyxl")
        else:
            raise Exception(
                """Invalid file format given, expected CSV, XLSX or XLS format. 
                Update configuration file accordinlgy."""
            )
        APPLOG.append(f'>>  Successfully loaded "{dir}".')

    except FileNotFoundError:
        APPLOG.append(f'>>  NOT FOUND "{dir}".!')
    except IOError:
        APPLOG.append(f'>>  "{dir}" Found! Permission denied for reading.')
    except Exception as e:
        APPLOG.append(ERROR_STYLE.format(e, dir))

    return df
