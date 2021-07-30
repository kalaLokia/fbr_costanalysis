"""
Main module for the program excecution.

Made with ❤️ by kalaLokia
"""

from typing import Tuple

import pandas as pd

from core import BOM_DATA_DIR, ITEM_DATA_DIR, ARTICLE_RATES_DIR
from core import excel_report
from core.bom import Bom
from core.article import Article
from core.excel_report import ExcelReporting

APPLOG = []
bom_db = pd.DataFrame()
items_db = pd.DataFrame()
articles_db = pd.DataFrame()


def readCsv(dir: str) -> Tuple[pd.DataFrame, str]:
    """
    Try to read external csv file.
    """
    df = pd.DataFrame()
    try:
        df = pd.read_csv(dir)
        log = f'>>  "{dir}" successfully loaded.'
    except FileNotFoundError:
        log = f'>>  NOT FOUND "{dir}".!'
    except IOError:
        log = f'>>  "{dir}" Found! Permission denied for reading.'
    except Exception as e:
        log = ">>  Unexpected error occured..!!!"
        print(e)

    return (df, log)


def loadDatabase() -> None:
    global bom_db
    global items_db
    global articles_db

    APPLOG.append(">>  Looking up for required data...")

    bom_db, log = readCsv(BOM_DATA_DIR)
    APPLOG.append(log)

    items_db, log = readCsv(ITEM_DATA_DIR)
    APPLOG.append(log)

    APPLOG.append(f">>  Looking up for Articles rate file...")

    articles_db, log = readCsv(ARTICLE_RATES_DIR)
    APPLOG.append(log)

    if not bom_db.empty and not items_db.empty:
        APPLOG.append("App ready!")
        if not articles_db.empty:
            articles_db["article"] = articles_db["article"].str.lower()
            articles_db.fillna(0)
        else:
            log = "Article's rates missing! Cannot calculate costs accuarately."
            APPLOG.append(log)
        # MainApplication(root, bom_db, items_db, articles_db).pack()
    else:
        log = f">>  Required files missing! Failed to launch app."
        APPLOG.append(log)


if __name__ == "__main__":
    loadDatabase()

    article = Article("Smartak", "l2124", "br", 12, "1-p6")
    article._category = "x"

    bom = Bom(article)
    data = bom.createFinalBom(bom_db, items_db)
    print(bom.bom_df)

    # reporting = ExcelReporting(
    #     article,
    #     bom.rexine_df,
    #     bom.component_df,
    #     bom.moulding_df,
    #     bom.packing_df,
    # )
    # reporting.generateTable()
