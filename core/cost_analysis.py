"""
Calculation of net margin, cost of production, etc.
"""
from typing import TYPE_CHECKING, Union
import math
from .article import Article
from core.settings import SELL_DISTR_ROYALTY, SALES_RETURN, EXPENSES_OVERHEADS

if TYPE_CHECKING:
    from pandas import DataFrame


def costAnalysisReport(df, mrps: list, material_costs: list) -> "DataFrame":
    """
    Returns a dataframe with cost analysis report for all available articles.
    """

    df["mrp"] = mrps
    df["material cost"] = material_costs

    # Cost of Production including overheads and other expenses
    df["cost of production"] = (
        (df[df.columns[1]] + df[df.columns[2]] + df["material cost"])
        + EXPENSES_OVERHEADS
    ).round(2)

    # Total Cost: Selling & Distribution, Royalty, Sales Return added
    df["total cost"] = (
        ((df[df.columns[3]] * SELL_DISTR_ROYALTY) + df["cost of production"])
        * (1 + SALES_RETURN)
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


def calculateProfit(article: Article, material_cost: Union[float, int]) -> tuple:
    """
    Returns COP, Total Cost, NET MARGIN of a article.
    """
    # Cost of Production including overheads and other expenses
    cost_of_upper_prod = round(
        article.stitch_rate + article.print_rate + material_cost, 2
    )
    cost_of_prod = cost_of_upper_prod + EXPENSES_OVERHEADS

    # Total Cost: Selling & Distribution, Royalty, Sales Return added
    total_cost = ((article.basic_rate * SELL_DISTR_ROYALTY) + cost_of_prod) * (
        1 + SALES_RETURN
    )

    # Net margin
    if article.basic_rate != 0:
        net_margin = (article.basic_rate - total_cost) / article.basic_rate
        net_margin_percent = round(net_margin * 100, 2)
    else:
        net_margin = 0
        net_margin_percent = 0

    return (cost_of_upper_prod, total_cost, net_margin_percent)
