"""
Load the Database to the memory. 
"""
import warnings

from typing import Tuple

import pandas as pd

from app import APPLOG
from app.base import App, MainApplication
from core.create_db import createBomDB
from core.settings import DB_DIR, BOM_DATA_DIR, ITEM_DATA_DIR, ARTICLE_RATES_DIR


def loadDatabase(root: App) -> None:
    """Load DB from data folder"""

    articles_db = pd.DataFrame()
    art_list = None

    APPLOG.append(">>  Looking up for required data...")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    art_db, _ = readFile("data/artList.csv")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    csv_db, reload = readFile(DB_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
    if reload:
        APPLOG.append(">>  Re-creating database... be patient, it will take a while.")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

        csv_db, art_db = createAndLoadDB(root)
        if csv_db.empty:
            APPLOG.append(">>  FAILED TO CREATE DATABASE")
            root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
            return
        APPLOG.append(">>  A new database successfully created and loaded.")

    APPLOG.append(f">>  Looking up for Articles rate file...")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    articles_db, _ = readFile(ARTICLE_RATES_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    if not root:
        return csv_db, art_db

    if not csv_db.empty:
        APPLOG.append("App ready!")
        if not art_db.empty:
            art_list = dict(zip(art_db["fathername"], art_db["father"]))
        root.forgetLog()
        if not articles_db.empty:
            articles_db["article"] = articles_db["article"].str.lower()
            articles_db.fillna(0)
        else:
            APPLOG.append(
                "Article's rates missing! Cannot calculate costs accuarately."
            )
        MainApplication(root, csv_db, articles_db, art_list).pack()
    else:
        APPLOG.append(f">>  Required files missing! Failed to launch app.")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])


def createAndLoadDB(root: App):
    """Load Bom CSV, Materials CSV for creating db"""

    bom_db = pd.DataFrame()
    items_db = pd.DataFrame()

    bom_db, _ = readFile(BOM_DATA_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    items_db, _ = readFile(ITEM_DATA_DIR)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    if items_db.empty and bom_db.empty:
        APPLOG.append(">>  ERROR OCCURED WHILE FETCHING DATA")
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        return pd.DataFrame()
    APPLOG.append(">>  Creating new database..")
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    df, art_df = createBomDB(bom_db, items_db)

    return (df, art_df)


def readFile(dir: str) -> Tuple[pd.DataFrame, str]:
    """
    Try to read external csv/excel file.
    """
    df = pd.DataFrame()
    reload_db: bool = False
    try:
        if dir.split(".")[-1] == "csv":
            df = pd.read_csv(dir, low_memory=False)
        elif dir.split(".")[-1] in ["xlsx", "xls"]:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(dir, engine="openpyxl")
        else:
            raise Exception("Invalid file format given, expected CSV, XLSX format.")
        log = f'>>  "{dir}" successfully loaded.'
    except FileNotFoundError:
        log = f'>>  NOT FOUND "{dir}".!'
        if dir == DB_DIR:
            reload_db = True
    except IOError:
        log = f'>>  "{dir}" Found! Permission denied for reading.'
    except Exception as e:
        log = f">>  Unexpected error occured..!!! #{dir}"
        log += "\nBEGINING OF ERROR.............\n"
        log += e
        log += "\n..............ENDING OF ERROR"
        # print(e)

    APPLOG.append(log)
    return (df, reload_db)
