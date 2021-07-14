"""
This is the main file for excecution in tkinter UI

Made by kalaLokia
"""

import threading
import pandas as pd
from tkinter import Tk, Frame, StringVar
from tkinter.ttk import Notebook, Style
from tabs.advanced_tab import TabAdvanced
from tabs.general_tab import TabGeneral
from frames.log_frame import LogFrame

BOM_DATA_DIR = "data/Bom Hierarchy final.csv"
ITEM_DATA_DIR = "data/materials.csv"
ARTINFO_DIR = "data/articles.csv"
APPLOG = []


class MainApplication(Frame):
    def __init__(self, root, bomdb, itemdb, artdb, *args, **kwargs) -> None:
        super().__init__(root, *args, **kwargs)
        self.bom_db = bomdb
        self.items_db = itemdb
        self.article_db = artdb

        style = Style(root)
        style.configure("B1.TButton", font=("Helvetica", 16))
        style.configure("B2.TButton", font=("Helvetica", 9))

        notebook = Notebook(root, width=400, height=470, padding=10)

        tab_general = TabGeneral(notebook, self)
        tab_advanced = TabAdvanced(notebook, self)

        notebook.add(tab_general, text="General")
        notebook.add(tab_advanced, text="Advanced")

        notebook.pack()


class App(Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log_msg = StringVar(self)
        self.log_frame = LogFrame(self)
        self.log_frame.pack(
            fill="both", side="left", anchor="w", expand=True, padx=5, pady=5
        )

    def forgetLog(self) -> None:
        self.log_frame.pack_forget()


def loadDatabase(root: App) -> None:
    bom_db = pd.DataFrame()
    items_db = pd.DataFrame()
    articles_db = pd.DataFrame()

    APPLOG.append(">>  Looking up for required data...")
    root.log_msg.set("\n".join(APPLOG))

    try:
        bom_db = pd.read_csv(BOM_DATA_DIR)
        APPLOG.append(">>  Bom data successfully loaded.")
    except FileNotFoundError:
        APPLOG.append(f'>>  "{BOM_DATA_DIR}" Not Found! Failed to get bom data.')
    except Exception as e:
        APPLOG.append(">>  Unexpected error occured..!!!")
        print(e)
    finally:
        root.log_msg.set("\n".join(APPLOG))

    try:
        items_db = pd.read_csv(ITEM_DATA_DIR)
        APPLOG.append(">>  Item master data successfully loaded.")
    except FileNotFoundError:
        APPLOG.append(
            f'>>  "{ITEM_DATA_DIR}" Not Found! Failed to get item master data.'
        )
    except Exception as e:
        APPLOG.append(">>  Unexpected error occured..!!!")
        print(e)
    finally:
        root.log_msg.set("\n".join(APPLOG))

    APPLOG.append(f">>  Looking up for Articles rate file...")
    root.log_msg.set("\n".join(APPLOG))
    try:
        articles_db = pd.read_csv(ARTINFO_DIR)
        articles_db["article"] = articles_db["article"].str.lower()
        articles_db.fillna(0)
        APPLOG.append(">>  Articles rate file successfully loaded.")
    except FileNotFoundError:
        APPLOG.append(f'">>  {ARTINFO_DIR}" Not found! Net rate cannot be calculated.')
    except Exception as e:
        APPLOG.append(">>  Unexpected error occured..!!!")
        print(e)
    finally:
        root.log_msg.set("\n".join(APPLOG))

    if not bom_db.empty and not items_db.empty:
        root.forgetLog()
        MainApplication(root, bom_db, items_db, articles_db).pack()
    else:
        APPLOG.append(f">>  Failed to launch app.")
        root.log_msg.set("\n".join(APPLOG))


if __name__ == "__main__":
    APPLOG.append(">>  Starting APP...")
    root = App()
    root.title("Create Cost Sheet")
    root.geometry("400x470")
    # root.iconbitmap("icon/dollar_bulb.ico")
    root.resizable(0, 0)

    threading.Thread(target=loadDatabase, args=(root,)).start()
    root.mainloop()
