"""
Main module for the program excecution.

Made with ❤️ by kalaLokia
"""
import threading
from typing import Tuple

import pandas as pd

from app import APPLOG
from app.base import App, MainApplication
from core.settings import BOM_DATA_DIR, ITEM_DATA_DIR, ARTICLE_RATES_DIR


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


def loadDatabase(root: App) -> None:
    bom_db = pd.DataFrame()
    items_db = pd.DataFrame()
    articles_db = pd.DataFrame()

    APPLOG.append(">>  Looking up for required data...")
    root.log_msg.set("\n".join(APPLOG))

    bom_db, log = readCsv(BOM_DATA_DIR)
    APPLOG.append(log)
    root.log_msg.set("\n".join(APPLOG))

    items_db, log = readCsv(ITEM_DATA_DIR)
    APPLOG.append(log)
    root.log_msg.set("\n".join(APPLOG))

    APPLOG.append(f">>  Looking up for Articles rate file...")
    root.log_msg.set("\n".join(APPLOG))
    root.log_msg.set("\n".join(APPLOG))

    articles_db, log = readCsv(ARTICLE_RATES_DIR)
    APPLOG.append(log)

    if not bom_db.empty and not items_db.empty:
        APPLOG.append("App ready!")
        root.forgetLog()
        if not articles_db.empty:
            articles_db["article"] = articles_db["article"].str.lower()
            articles_db.fillna(0)
        else:
            log = "Article's rates missing! Cannot calculate costs accuarately."
            APPLOG.append(log)
        MainApplication(root, bom_db, items_db, articles_db).pack()
    else:
        log = f">>  Required files missing! Failed to launch app."
        APPLOG.append(log)
        root.log_msg.set("\n".join(APPLOG))


if __name__ == "__main__":

    APPLOG.append(">>  Starting APP...")
    root = App()
    root.title("Create Cost Sheet")
    root.geometry("400x470")
    # root.iconbitmap("icon/dollar_bulb.ico")
    root.resizable(0, 0)

    thread = threading.Thread(target=loadDatabase, args=(root,))
    thread.daemon = True
    thread.start()
    root.mainloop()
