"""
Getting actual BOM of an article.
"""

import math
import pandas as pd
from .article import Article


class Bom:
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
    def get_cost_of_materials(self):
        if self.bom_df.empty:
            return 0
        mtypes = ["Synthetic Leather", "Component", "Footwear Sole", "Packing Material"]
        total_sum = self.bom_df[self.bom_df.childtype.isin(mtypes)]["rate"].sum()
        total_sum += 3  # Other material cost
        total_sum = math.ceil(total_sum * 100) / 100  # round up to 2 decimal places
        return total_sum

    def createFinalBom(self, df, items_df) -> dict:
        mc_name = self.article.get_mc_name
        mc_conditions = (df["Father"].str.lower() == mc_name) & (
            df["Process Order"] == 1
        )
        mc_bom = df[mc_conditions]

        sc_head = self.getHeadsList(mc_bom)
        sc_bom = df[df["Father"].isin(sc_head)]

        mpu_head = self.getHeadsList(sc_bom)
        mpu_bom = df[df["Father"].isin(mpu_head)]

        fu_head = self.getHeadsList(mpu_bom)
        fu_bom = df[df["Father"].isin(fu_head)]

        semi1_head = self.getHeadsList(fu_bom)
        semi1_bom = df[df["Father"].isin(semi1_head)]

        semi2_head = self.getHeadsList(semi1_bom)
        semi2_bom = df[df["Father"].isin(semi2_head)]

        semi3_head = self.getHeadsList(semi2_bom)
        semi3_bom = df[df["Father"].isin(semi3_head)]

        semi4_head = self.getHeadsList(semi3_bom)
        semi4_bom = df[df["Father"].isin(semi4_head)]

        # semi5_head = self.getHeadsList(semi4_bom) # Extra
        # semi5_bom = df[df["Father"].isin(semi5_head)]

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

        self.updateBom(items_df)

        return {
            "status": "OK",
            "message": f"Fetched bom for {self.article.article_name}",
        }

    def updateBom(self, df) -> None:
        unwanted_columns = [
            "Father Name",
            "Father No of pairs",
            "Father Qty",
            "Child Name",
            "Item No._x",
            "Item No._y",
        ]
        self.bom_df = self.bom_df.merge(
            df[["Item No.", "FOREIGN NAME", "INVENTORY UOM", "Last Purchase Price"]],
            how="left",
            left_on="Child",
            right_on="Item No.",
        )
        self.bom_df = self.bom_df.merge(
            df[["Item No.", "MRP", "Product Type"]],
            how="left",
            left_on="Father",
            right_on="Item No.",
        )
        self.bom_df.drop(unwanted_columns, axis=1, inplace=True, errors="ignore")
        self.bom_df.columns = [
            self.changeColumnName(name) for name in self.bom_df.columns.values
        ]
        self.bom_df["childtype"] = self.bom_df.apply(
            lambda x: self.getMaterialType(x.father, x.child), axis=1
        )
        # MC, SC
        self.bom_df["application"] = self.bom_df.apply(
            lambda x: self.getApplication(x.father, x.processorder), axis=1
        )
        self.bom_df["childqty"] = pd.to_numeric(
            self.bom_df["childqty"], errors="coerce"
        )
        self.bom_df["childrate"] = pd.to_numeric(
            self.bom_df["childrate"], errors="coerce"
        )
        self.article.mrp = float(self.bom_df.mrp.iloc[0])
        self.article.pairs_in_case = int(self.get_pairs_in_mc)
        self.updateRexinConsumption()
        self.updateComponentConsumption()
        self.updatePuxConsumption()
        self.bom_df["rate"] = self.bom_df.apply(
            lambda x: self.calculateRate(x.processorder, x.childrate, x.childqty),
            axis=1,
        )

    def getHeadsList(self, df):
        """Returns list of heads in the given dataframe's column Child"""
        condition1 = df["Child"].str.startswith("3-") | df["Child"].str.startswith("4-")
        condition2 = (
            df["Child"].str.lower().str.endswith(self.article.get_category_size)
            | df["Child"].str.lower().str.endswith(self.article.category)
            | df["Child"].str.lower().str.startswith("4-pux-")
        )
        return df[condition1 & condition2]["Child"].unique()

    def changeColumnName(self, name) -> str:
        return {
            "FOREIGN NAME": "childname",
            "INVENTORY UOM": "childuom",
            "Last Purchase Price": "childrate",
        }.get(name, name.lower().replace(" ", ""))

    def getMaterialType(self, head: str, tail: str) -> str:
        item = tail[2:4].lower()
        head_item = "".join(head.split("-")[1:2]).lower()

        material_types = {
            "nl": "Synthetic Leather",
            "co": "Component",
            "pu": "PU Mix",
        }
        default_material_types = {
            "fb": "Packing Material",
            "mpu": "Footwear Sole",
            "pux": "Footwear Sole",
        }
        try:
            value = int(tail[0])
            if value > 4 or tail[:5].lower() == "4-pux":
                default_type = default_material_types.get(head_item, "Other Material")
                return material_types.get(item, default_type)
            else:
                return item
        except:
            return "Unknown"

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

    def getApplication(self, head, process) -> str:
        value = "".join(head.split("-")[1:2])

        if value.lower() == "fb":
            if process == 1:
                return "MC"
            elif process == 2:
                return "SC"
            else:
                return "NA"
        else:
            return value

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
