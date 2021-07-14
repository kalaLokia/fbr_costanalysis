"""
This is the main file for excecution in tkinter UI

Made by kalaLokia
"""

from tkinter import *
from tkinter.ttk import *
import pandas as pd
from tabs.advanced_tab import TabAdvanced
from tabs.general_tab import TabGeneral


BOM_DATA_DIR = "data/Bom Hierarchy final.csv"
ITEM_DATA_DIR = "data/materials.csv"
ARTINFO_DIR = "data/articles.csv"
ARTLIST_DB = pd.DataFrame()
BOM_DB = pd.DataFrame()
ITEMS_DB = pd.DataFrame()

# Reading File
print("Trying to fetch data from data/*.csv files.")
try:
    BOM_DB = pd.read_csv(BOM_DATA_DIR)
    ITEMS_DB = pd.read_csv(ITEM_DATA_DIR)
    print("Database ready!")

except FileNotFoundError:
    print("Requird files not found in the directory data.")
except:
    print("Something I didn't understand, please report.")

try:
    ARTINFO_DB = pd.read_csv(ARTINFO_DIR)
    ARTINFO_DB["article"] = ARTINFO_DB["article"].str.lower()
    ARTINFO_DB.fillna(0)
except FileNotFoundError:
    print("Article rate file not found")
except:
    print("Something wrong with rates file, please report.")

print("Opening GUI..")


class MainApplication(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        style = Style(root)
        style.configure("B1.TButton", font=("Helvetica", 16))
        style.configure("B2.TButton", font=("Helvetica", 9))

        notebook = Notebook(root, width=400, height=470, padding=10)

        tab_general = TabGeneral(notebook, BOM_DB, ITEMS_DB, ARTINFO_DB)
        tab_advanced = TabAdvanced(notebook, BOM_DB, ITEMS_DB, ARTINFO_DB)

        notebook.add(tab_general, text="General")
        notebook.add(tab_advanced, text="Advanced")

        notebook.pack()


if __name__ == "__main__":

    # Root configuration
    root = Tk()
    root.title("Create Cost Sheet")
    root.geometry("400x470")
    # root.iconbitmap("icon/dollar_bulb.ico")
    root.resizable(0, 0)

    MainApplication(root).pack()
    root.mainloop()
