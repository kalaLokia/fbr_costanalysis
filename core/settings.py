"""
Configuration file setup.
"""
from app import APPLOG
import os
import configparser
from typing import Tuple
from . import *


DB_CONNECTION = None


os.makedirs(os.path.dirname("files/test.txt"), exist_ok=True)

config = configparser.ConfigParser(interpolation=None)
ok_config = config.read("config.ini")


def to_float(input: str) -> Tuple[float, bool]:
    value = input.strip("%").strip()
    result = None
    try:
        result = float(value) / 100 if "%" in input else float(value)
    except:
        print("Cannot convert to float")
        return (None, False)

    return (result, True)


if not ok_config:
    print("LOADING WITH DEFAULT CONFIGURATION")
else:
    if config.has_option("EXTERNAL FILES", "bom_heirarchy"):
        BOM_DATA_DIR = config.get("EXTERNAL FILES", "bom_heirarchy")

    if config.has_option("EXTERNAL FILES", "item_master"):
        ITEM_DATA_DIR = config.get("EXTERNAL FILES", "item_master")

    if config.has_option("EXTERNAL FILES", "article_rates"):
        ARTICLE_RATES_DIR = config.get("EXTERNAL FILES", "article_rates")

    if config.has_option("MODE", "DB_MODE"):
        DB_MOD = config.get("MODE", "DB_MODE").upper()

    if config.has_section("FIXED RATES"):
        data = {}
        for key, item in dict(config.items("FIXED RATES")).items():
            result, ok = to_float(item)
            if ok:
                data[key] = result
            else:
                data = None
                print("Default value is used for FIXED RATES")
                break

        if data and isinstance(data, dict):
            FIXED_RATES = data

    if config.has_option("OTHER CHARGES", "selling_and_distribution"):
        result, ok = to_float(config.get("OTHER CHARGES", "selling_and_distribution"))
        if ok:
            SELLING_DISTRIBUTION = result
        else:
            print("Default values used for SELLING & DISTRIBUTION")

    if config.has_option("OTHER CHARGES", "royalty"):
        result, ok = to_float(config.get("OTHER CHARGES", "royalty"))
        if ok:
            ROYALTY = result
        else:
            print("Default values used for  ROYALTY")

    if config.has_option("OTHER CHARGES", "sales_return"):
        result, ok = to_float(config.get("OTHER CHARGES", "sales_return"))
        if ok:
            SALES_RETURN = result
        else:
            print("Default values used for SALES RETURN")

    if config.has_section("CASE TYPES"):
        data = []
        for item in dict(config.items("CASE TYPES")).values():
            data.append(item)

        if data:
            CASE_TYPES = data


SELL_DISTR_ROYALTY = SELLING_DISTRIBUTION + ROYALTY
EXPENSES_OVERHEADS = sum(FIXED_RATES.values())
