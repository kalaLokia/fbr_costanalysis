"""
Getting actual BOM of an article.
"""

import math

import pandas as pd

from .article import Article


class BomSQL:
    def __init__(self, article: Article) -> None:
        self.bom_df = None
        self.article = article

    @property
    def get_pairs_in_mc(self):
        return self.bom_df[self.bom_df.child == "FGMC-OH"]["childqty"].iloc[0]

    @property
    def get_outer_sole(self):
        condition = self.bom_df.child.str.lower().str.startswith("4-pux")
        return tuple(self.bom_df[condition][["child", "childqty"]].iloc[0])

    @property
    def rexine_df(self):
        return self.getTableData("Synthetic Leather")

    @property
    def component_df(self):
        return self.getTableData("Component")

    @property
    def moulding_df(self):
        return self.getTableData("Footwear Sole")

    @property
    def packing_df(self):
        return self.getTableData("Packing Material")

    @property
    def get_article_mrp(self):
        if self.bom_df.empty:
            return 0
        return self.bom_df.mrp.iloc[0]

    @property
    def get_brand_name(self):
        if self.bom_df.empty:
            return "Unknown"
        return self.bom_df.brand.iloc[0]

    @property
    def get_cost_of_materials(self):
        if self.bom_df.empty:
            return 0
        mtypes = ["Synthetic Leather", "Component", "Footwear Sole", "Packing Material"]
        total_sum = self.bom_df[self.bom_df.childtype.isin(mtypes)]["rate"].sum()
        total_sum += 3  # Other material cost
        total_sum = math.ceil(total_sum * 100) / 100  # round up to 2 decimal places
        return total_sum

    def createFinalBom(self, df) -> dict:
        """Get article's bom from the DB"""

        mc_name = self.article.get_mc_name
        mc_conditions = (df["father"].str.lower() == mc_name) & (
            df["processorder"] == 1
        )
        mc_bom = df[mc_conditions]

        sc_head = self.getHeadsList(mc_bom)
        sc_bom = df[df["father"].isin(sc_head)]

        mpu_head = self.getHeadsList(sc_bom)
        mpu_bom = df[df["father"].isin(mpu_head)]

        fu_head = self.getHeadsList(mpu_bom)
        fu_bom = df[df["father"].isin(fu_head)]

        semi1_head = self.getHeadsList(fu_bom)
        semi1_bom = df[df["father"].isin(semi1_head)]

        semi2_head = self.getHeadsList(semi1_bom)
        semi2_bom = df[df["father"].isin(semi2_head)]

        semi3_head = self.getHeadsList(semi2_bom)
        semi3_bom = df[df["father"].isin(semi3_head)]

        semi4_head = self.getHeadsList(semi3_bom)
        semi4_bom = df[df["father"].isin(semi4_head)]

        # semi5_head = self.getHeadsList(semi4_bom) # Extra
        # semi5_bom = df[df["father"].isin(semi5_head)]

        self.bom_df = pd.concat(
            [
                mc_bom,
                sc_bom,
                mpu_bom,
                fu_bom,
                semi1_bom,
                semi2_bom,
                semi3_bom,
                semi4_bom,
            ],
            ignore_index=True,
        )

        if self.bom_df.empty:
            return {
                "status": "NOT FOUND",
                "message": f'Bom for article "{self.article.article_name}" not found in the database. Update the database if it is too old.',
            }

        self.article.mrp = float(self.bom_df.mrp.iloc[0])
        self.article.pairs_in_case = int(self.get_pairs_in_mc)
        self.updateRexinConsumption()
        self.updateComponentConsumption()
        self.updatePuxConsumption()
        self.bom_df["rate"] = self.bom_df.apply(
            lambda x: self.calculateRate(x.processorder, x.childrate, x.childqty),
            axis=1,
        )

        if not self.article.brand:
            self.article.brand = self.get_brand_name

        return {
            "status": "OK",
            "message": f"Fetched bom for {self.article.article_name}",
        }

    def getHeadsList(self, df):
        """Returns list of heads in the given dataframe's column Child"""

        condition1 = df["child"].str.startswith("3-") | df["child"].str.startswith("4-")
        condition2 = (
            # df["Child"].str.lower().str.endswith(self.article.get_category_size) |
            df["child"]
            .str.lower()
            .str.contains(f"[gxlbrcki](?:{self.article.get_str_size})?$", regex=True)
            | df["child"].str.lower().str.startswith("4-pux-")
        )
        return df[condition1 & condition2]["child"].unique()

    def updateRexinConsumption(self) -> None:
        slt_df = self.bom_df[
            (self.bom_df.processorder == 8)
            & (self.bom_df.childtype == "Synthetic Leather")
        ]
        slt_items = slt_df["father"].tolist()
        for i, slt in enumerate(slt_items):
            slt_head_df = self.bom_df[self.bom_df.child == slt]
            if slt_head_df.processorder.iloc[0] < 7:
                length = slt_head_df["childqty"].iloc[0]
            else:
                fld = slt_head_df.father.iloc[0]
                fld_head_df = self.bom_df[self.bom_df.child == fld]
                length = fld_head_df["childqty"].iloc[0]

            self.bom_df.loc[slt_df.index.values[i], "childqty"] *= length

    def updateComponentConsumption(self) -> None:
        fld_df = self.bom_df[
            (self.bom_df.processorder == 7)
            & (
                (self.bom_df.childtype == "Component")
                | (self.bom_df.childtype == "Other Material")
            )
        ]
        fld_items = fld_df["father"].tolist()
        for i, fld in enumerate(fld_items):
            fld_head_df = self.bom_df[self.bom_df.child == fld]
            if fld_head_df.processorder.iloc[0] < 7:
                length = fld_head_df["childqty"].iloc[0]
                self.bom_df.loc[fld_df.index.values[i], "childqty"] *= length

    def updatePuxConsumption(self) -> None:
        self.bom_df.loc[
            self.bom_df["father"] == self.get_outer_sole[0], "childqty"
        ] *= self.get_outer_sole[1]

    def calculateRate(self, process, item_rate, qty) -> float:
        rate = item_rate * qty
        if process == 1:
            rate = rate / self.get_pairs_in_mc
        return rate

    def getTableData(self, mtype: str) -> pd.DataFrame:
        """
        Get costsheet table for given material type.

        Args
        -----
            :mtype: -- Material type
        """
        table_data = self.bom_df[self.bom_df.childtype == mtype].filter(
            ["application", "child", "childname", "childqty", "childrate", "rate"]
        )
        table_data = table_data.reset_index(drop=True)
        return table_data
