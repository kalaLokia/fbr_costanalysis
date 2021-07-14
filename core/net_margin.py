"""
Calculation of net margin, cost of production, etc.
"""

import math
from .article import Article


def calculateNetMargin(df, mrps: list, material_costs: list):
    """
    Calculates net margin from bulk data.
    """
    expenses_overheads = 19.04
    # Selling and Distribution = 16.75%, Royalty = 0.50%
    sell_distr_royalty = 0.1725
    sales_return = 1.01  # Sales Return = 1%

    df["mrp"] = mrps
    df["material cost"] = material_costs

    # Cost of Production including overheads and other expenses
    df["cost of production"] = (
        (df[df.columns[1]] + df[df.columns[2]] + df["material cost"])
        + expenses_overheads
    ).round(2)

    # Total Cost: Selling & Distribution, Royalty, Sales Return added
    df["total cost"] = (
        ((df[df.columns[3]] * sell_distr_royalty) + df["cost of production"])
        * sales_return
    ).round(2)

    # Net margin
    df.replace({"0": math.nan, 0: math.nan}, inplace=True)
    df["net margin"] = (
        (df[df.columns[3]] - df["total cost"]) / df[df.columns[3]]
    ).round(5)

    # Net margin in percentage
    df["net margin in percent"] = (
        (df[df.columns[3]] - df["total cost"]) / df[df.columns[3]] * 100
    ).round(2)

    return df


def calculateNetMarginSingle(article: Article, material_cost):
    """
    Calculates net margin for a article
    """
    expenses_overheads = 19.04
    # Selling and Distribution = 16.75%, Royalty = 0.50%
    sell_distr_royalty = 0.1725
    sales_return = 1.01  # Sales Return = 1%

    # Cost of Production including overheads and other expenses
    cost_of_upper_prod = round(
        article.stitch_rate + article.print_rate + material_cost, 2
    )
    cost_of_prod = cost_of_upper_prod + expenses_overheads

    # Total Cost: Selling & Distribution, Royalty, Sales Return added
    total_cost = (
        (article.basic_rate * sell_distr_royalty) + cost_of_prod
    ) * sales_return

    # Net margin
    if article.basic_rate != 0:
        net_margin = (article.basic_rate - total_cost) / article.basic_rate
        net_margin_percent = round(net_margin * 100, 2)
    else:
        net_margin = 0
        net_margin_percent = 0

    return (cost_of_upper_prod, total_cost, net_margin_percent)
