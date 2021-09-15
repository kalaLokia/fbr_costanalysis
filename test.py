"""
Main module for the program excecution.

Made with ❤️ by kalaLokia
"""

from core.load_database import loadDatabase
from core.bom import Bom
from core.article import Article

APPLOG = []

if __name__ == "__main__":
    db, art_db = loadDatabase(None)

    art_list = dict(zip(art_db["fathername"], art_db["father"]))
    print(art_list.values())

    # article = Article("", "8125", "nb", 8, "1")
    # article._category = "l"
    # article.basic_rate = 152
    # article.stitch_rate = 15.5
    # article.print_rate = 1

    # bom = Bom(article)
    # data = bom.createFinalBom(db)
    # print(bom.bom_df)

    # art_list = dict(zip(article_list["fathername"], article_list["father"]))
    # print(art_list.values())
