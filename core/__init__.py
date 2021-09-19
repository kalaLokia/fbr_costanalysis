# DEFAULT CONFIGURATIONS TO USE IF "config.ini" IS NOT ACCESSIBLE
# OR DOESN'T CONTAINS REQUIRED SECTIONS


DB_MOD = "SQL"

SQL_CONN = "sqlite:///data/bom.db"
SQL_DB_DIR = "data/bom.db"
SQL_T_BOM = "bom"
SQL_T_ARTLIST = "artlist"

DB_DIR = "data/db.csv"
ARTLIST_DIR = "data/artlist.csv"

BOM_DATA_DIR = "data/Bom Hierarchy final.csv"
ITEM_DATA_DIR = "data/materials.csv"
ARTICLE_RATES_DIR = "data/articles.csv"


ROYALTY = 0.5
SELLING_DISTRIBUTION = 0.1675
SALES_RETURN = 0.01

FIXED_RATES = {
    "wastage_and_benefits": 9.72,
    "salaries_and_emoluments": 0.79,
    "other_factory_overheads": 1.73,
    "admin_expenses": 1.37,
    "interest_and_bank_charges": 0.02,
    "depreciation": 4.35,
    "other_expenses": 0.0,
    "finance_costs": 1.06,
}  # EXPENSES_AND_OVERHEADS

CASE_TYPES = ["1", "2", "3"]
