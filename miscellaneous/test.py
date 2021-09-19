import sqlite3
import pandas as pd

from core import BOM_DATA_DIR, ITEM_DATA_DIR
from core.article import Article
from core.load_database import readFile
from core.create_sql_db import createBomDB

con = sqlite3.connect("bom.db")

if __name__ == "__main__":

    # # Test DB creation ..........
    # bom_df, _, __ = readFile(BOM_DATA_DIR)
    # item_df, _, __ = readFile(ITEM_DATA_DIR)
    # bdf, adf = createBomDB(bom_df, item_df)
    # # ..........

    # Test BOM
    article = Article("", "8125", "nb", 8, "1")
    article._category = "l"
    article.basic_rate = 152
    article.stitch_rate = 15.5
    article.print_rate = 1
    headers = [
        "father",
        "fathername",
        "brand",
        "child",
        "childname",
        "childqty",
        "childuom",
        "childrate",
        "childtype",
        "producttype",
        "mrp",
        "process",
        "processorder",
        "application",
    ]
    query = f"""
    with recursive cte ({",".join(headers)}) as (
        select     {",".join(headers)}
        from       bom
        where      father = "{article.get_mc_name.upper()}"
        union all
        select     {",".join(["p." + x for x in headers])}
        from       bom p
        inner join cte
                on p.father = cte.child
        )
    select * from cte
    """

    query2 = "SELECT * FROM bom WHERE father Like '{}'".format(article.get_mc_name)

    # df = pd.read_sql_query(
    #     f"SELECT * FROM bom WHERE father Like '{article.get_mc_name}'", con
    # )
    df = pd.read_sql_query(query, con)
    print(df)
