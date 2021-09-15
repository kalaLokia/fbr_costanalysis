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

    APPLOG.append(">>  Looking up for required data...")

    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    csv_db, log, reload = readFile(DB_DIR)
    art_db, log, reload = readFile("data/artList.csv")
    if reload:
        APPLOG.append(">>  Re-creating database... be patient, it will take a while.")

        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        csv_db, art_db = createAndLoadDB(root)
        if csv_db.empty:
            APPLOG.append(">>  FAILED TO CREATE DATABASE")

            root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
            return
        APPLOG.append(">>  A new database successfully created and loaded.")
    else:
        APPLOG.append(log)

    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    APPLOG.append(f">>  Looking up for Articles rate file...")

    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    articles_db, log, reload = readFile(ARTICLE_RATES_DIR)
    APPLOG.append(log)
    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
    if not root:
        return csv_db, art_db

    if not csv_db.empty:
        APPLOG.append("App ready!")
        root.forgetLog()
        if not articles_db.empty:
            articles_db["article"] = articles_db["article"].str.lower()
            articles_db.fillna(0)
        else:
            log = "Article's rates missing! Cannot calculate costs accuarately."
            APPLOG.append(log)
        MainApplication(root, csv_db, articles_db).pack()
    else:
        log = f">>  Required files missing! Failed to launch app."
        APPLOG.append(log)
        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])


def createAndLoadDB(root: App):
    """Load Bom CSV, Materials CSV for creating db"""

    bom_db = pd.DataFrame()
    items_db = pd.DataFrame()

    bom_db, log, reload = readFile(BOM_DATA_DIR)
    APPLOG.append(log)

    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    items_db, log, reload = readFile(ITEM_DATA_DIR)
    APPLOG.append(log)

    root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])

    if items_db.empty and bom_db.empty:
        log = ">>  ERROR OCCURED WHILE FETCHING DATA"
        APPLOG.append(log)

        root.log_msg.set("\n".join(APPLOG)) if root else print(APPLOG[-1])
        return pd.DataFrame()
    log = ">>  Creating new database.."
    APPLOG.append(log)

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
        elif dir.split(".")[-1] == "xlsx":
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("always")
                df = pd.read_excel(dir, engine="openpyxl")
        else:
            raise Exception("Invalid file format given, expected CSV, XLSX format.")
        log = f'>>  "{dir}" successfully loaded.'
    except FileNotFoundError:
        log = f'>>  NOT FOUND "{dir}".!'
        reload_db = True
    except IOError:
        log = f'>>  "{dir}" Found! Permission denied for reading.'
    except Exception as e:
        log = f">>  Unexpected error occured..!!! #{dir}"
        log += "\nBEGINING OF ERROR.............\n"
        log += e
        log += "\n..............ENDING OF ERROR"
        print(e)

    return (df, log, reload_db)
