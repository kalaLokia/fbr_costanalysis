"""
This is the main file for excecution in console.

Made by kalaLokia and Tony
Github: https://github.com/kalalokia/python
"""

from runapp import ARTINFO_DB
import sys
import pandas as pd
from article import Article
from bom import Bom
from excel_report import ExcelReporting
import math
from net_margin import calculateNetMargin
from datetime import datetime

# bom_source = "data/Bom Hierarchy final.xlsx"
# items_source = "data/materials.xlsx"
bom_source = "data/Bom Hierarchy final.csv"
items_source = "data/materials.csv"
article_source = "data/articles.csv"
ARTLIST_DB = None
ARTICLE_INFO_DB = pd.DataFrame()

try:
    # bom_db = pd.read_excel(bom_source, sheet_name="Sheet1", engine="openpyxl")
    # items_db = pd.read_excel(items_source, sheet_name="Sheet1", engine="openpyxl")
    bom_db = pd.read_csv(bom_source)
    items_db = pd.read_csv(items_source)
except FileNotFoundError:
    print("File not found! materials.xlsx or Bom Hierarchy final.xlsx")
except:
    e = sys.exc_info()[0]
    print(e)


try:
    ARTICLE_INFO_DB = pd.read_csv(article_source)
    ARTICLE_INFO_DB["article"] = ARTICLE_INFO_DB["article"].str.lower()
except FileNotFoundError:
    ARTICLE_INFO_DB = pd.DataFrame()

except:
    e = sys.exc_info()[0]
    print(e)


# def openFile():
#     global ARTLIST_DB

#     filename = "C:/Users/nightfury/Workshop/data/articles.csv"

#     try:
#         ARTLIST_DB = pd.read_csv(filename)
#     except:
#         print("Couldn't read data! File missing or invalid.")

#     if ARTLIST_DB.shape[1] != 4:
#         ARTLIST_DB = None
#         print("Correpted file. Accepts only 4 columns.")

#     elif ARTLIST_DB[ARTLIST_DB.columns[0]].isnull().values.any():
#         ARTLIST_DB = None
#         print("Correpted file. Some article name is not provided in the data.")

#     else:
#         # ARTLIST_DB.replace({"0": math.nan, 0: math.nan}, inplace=True)
#         print(f"Successfully fetched data from the given file.")


if __name__ == "__main__":

    article = Article(artno="DG9531", color="bk")

    bom = Bom(article=article)
    response = bom.createFinalBom(bom_db, items_db)
    print(bom.bom_df)
