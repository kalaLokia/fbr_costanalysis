"""
Article model structure.

Made by kalaLokia
Github: https://github.com/kalalokia/python
"""

import math


class Article:
    def __init__(
        self,
        brand: str = "pride",
        artno: str = "3290",
        color: str = "bk",
        size: int = 8,
        case_type: str = "1",
    ):
        self.artno = artno.lower()
        self.color = color.lower()
        self._category = "g"
        self.size = size
        self.case_type = case_type.lower()
        self.brand = brand.lower()
        self.pairs_in_case = 0
        self.mrp = 0
        self.stitch_rate = 0
        self.print_rate = 0
        self.basic_rate = 0

    @property
    def get_mc_name(self) -> str:
        prefix = "2-fb"
        return "-".join(
            [prefix, self.artno, self.color, self.category + self.case_type]
        )

    @property
    def get_category_size(self) -> str:
        return "{}{:02d}".format(self.category, self.size)

    @property
    def get_filename(self) -> str:
        return f"{self.artno.upper()} {self.color.upper()}-CS.xlsx"

    @property
    def category(self):
        return self._category

    @property
    def article_code(self) -> str:
        return f"{self.artno}-{self.color}-{self._category}"

    @category.setter
    def category(self, value):
        self._category = {
            "gents": "g",
            "ladies": "l",
            "giants": "x",
            "children": "c",
            "kids": "k",
            "boys": "b",
            "girls": "r",
        }.get(value.lower(), "g")

    def __str__(self):
        return self.article_code

    @classmethod
    def from_bulk_list(cls, article, rates):
        try:
            artno, color, catg = article.lower().split("-")
            catg = catg[0]
        except:
            artno, color, catg = "0000", "bk", "g"

        size = {"g": 8, "l": 7, "x": 12, "c": 12, "k": 8, "r": 3, "b": 3}.get(catg, 8)
        obj = cls(brand="___", artno=artno, color=color, size=size)
        obj._category = catg
        obj.print_rate = 0 if math.isnan(rates[0]) else rates[0]
        obj.stitch_rate = 0 if math.isnan(rates[1]) else rates[1]
        obj.basic_rate = 0 if math.isnan(rates[2]) else rates[2]
        return obj
