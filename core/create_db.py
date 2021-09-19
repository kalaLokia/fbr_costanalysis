"""
Creates a new Database
"""
import re
from numpy import empty
import pandas as pd
from core.settings import (
    DB_MOD,
    DB_DIR,
    ARTLIST_DIR,
    SQL_T_ARTLIST,
    SQL_T_BOM,
    SQL_CONN,
)
from sqlalchemy import create_engine


def createBomDB(bom_df: pd.DataFrame, items_df: pd.DataFrame) -> tuple:
    """Save DB to directory data, either SQLITE or CSV format."""
    if bom_df.empty or items_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    unwanted_columns = [
        # "Father Name",
        "Father No of pairs",
        "Father Qty",
        "Child Name",
        "Item No._x",
        "Item No._y",
    ]
    bom_df["brand"] = bom_df.apply(
        lambda x: getBrandName(x.get("Process Order"), x.get("Father Name")), axis=1
    )
    bom_df = bom_df.merge(
        items_df[["Item No.", "FOREIGN NAME", "INVENTORY UOM", "Last Purchase Price"]],
        how="left",
        left_on="Child",
        right_on="Item No.",
    )
    bom_df = bom_df.merge(
        items_df[["Item No.", "Item MRP", "Product Type"]],
        how="left",
        left_on="Father",
        right_on="Item No.",
    )
    bom_df.drop(unwanted_columns, axis=1, inplace=True, errors="ignore")
    bom_df.columns = [changeColumnName(name) for name in bom_df.columns.values]
    bom_df["childtype"] = bom_df.apply(
        lambda x: getMaterialType(x.father, x.child), axis=1
    )
    # MC, SC
    bom_df["application"] = bom_df.apply(
        lambda x: getApplication(x.father, x.processorder), axis=1
    )
    bom_df["childqty"] = pd.to_numeric(bom_df["childqty"], errors="coerce")
    bom_df["childrate"] = pd.to_numeric(bom_df["childrate"], errors="coerce")

    artlist_df = create_article_list(bom_df)

    if DB_MOD == "CSV":
        bom_df.to_csv(DB_DIR, index=False)
        artlist_df.to_csv(ARTLIST_DIR, index=False)
    else:
        engine = create_engine(SQL_CONN, echo=False)
        bom_df.to_sql(SQL_T_BOM, con=engine, if_exists="replace", index=False)
        artlist_df.to_sql(SQL_T_ARTLIST, con=engine, if_exists="replace", index=False)

        engine.dispose()

    return bom_df, artlist_df


def create_article_list(db):
    """Creates a dataframe with article sapcode and description for Find tab.

    This helps to create a key-value pair of article's main parent description and sapcode,
    Only process first match case type (sorted by case type)
    """
    df = db[db["father"].str.startswith("2-FB-")][["father", "fathername"]].copy()
    df["art"] = (
        df.father.str.split("-").str[2:4].str.join("-")
        + "-"
        + df.father.str.split("-").str[4:].str[0].str[0]
    )
    df["case"] = df.father.str.split("-").str[4:].str.join("-").str[1:]
    df.sort_values("case", inplace=True)
    df.drop_duplicates(subset=["art"], ignore_index=True, inplace=True)
    df["fathername"] = df.fathername.str.replace("-", " ")

    return df


def changeColumnName(name) -> str:
    """For changing column names of the dataframe"""
    return {
        "FOREIGN NAME": "childname",
        "INVENTORY UOM": "childuom",
        "Item MRP": "mrp",
        "Last Purchase Price": "childrate",
    }.get(name, name.lower().replace(" ", ""))


def getMaterialType(head: str, tail: str) -> str:
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


def getApplication(head, process) -> str:
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


def getBrandName(process_no, item):
    """All SAP item description is not valid."""
    if process_no == 2 or process_no == 1:
        brand = item.split("-")[1].title()
        if has_digits(brand) or brand == "Fortune Kinaloor":
            brand = "Unknown"
        elif brand == "Smarblk":
            brand = "Smartak?"
        return brand
    return ""


def has_digits(inputString):
    return bool(re.search(r"\d", inputString))
