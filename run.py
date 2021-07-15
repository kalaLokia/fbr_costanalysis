"""
For easy test purpose console based access without tkinter UI
"""

import sys
import pandas as pd
from core.article import Article
from core.bom import Bom
from core.excel_report import ExcelReporting

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


# try:
#     ARTICLE_INFO_DB = pd.read_csv(article_source)
#     ARTICLE_INFO_DB["article"] = ARTICLE_INFO_DB["article"].str.lower()
# except FileNotFoundError:
#     ARTICLE_INFO_DB = pd.DataFrame()

# except:
#     e = sys.exc_info()[0]
#     print(e)


if __name__ == "__main__":

    article = Article(artno="3290", color="br")

    bom = Bom(article=article)
    response = bom.createFinalBom(bom_db, items_db)
    print(bom.bom_df)
