"""
Main module for the program excecution without tkinter GUI

Made with ❤️ by kalaLokia
"""


import pandas as pd

from core.load_database import loadDatabase
from core import excel_report
from core.bom import Bom
from core.article import Article
from core.excel_report import ExcelReporting

APPLOG = []


if __name__ == "__main__":
    db, _ = loadDatabase()

    article = Article("Smartak", "l2124", "br", 12, "1-p6")
    article._category = "x"

    bom = Bom(article)
    data = bom.createFinalBom(db)
    print(bom.bom_df)

    # reporting = ExcelReporting(
    #     article,
    #     bom.rexine_df,
    #     bom.component_df,
    #     bom.moulding_df,
    #     bom.packing_df,
    # )
    # reporting.generateTable()
