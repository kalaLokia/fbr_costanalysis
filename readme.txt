Intro:
______________
The application is for calculating cost of an article by extracting the bill of materials of the article from SAP "bom heirarchy" report,
that contains complete heirarchial representation of every article in the unit. 


Configuration:
______________

Application's configuration file (.config.ini) is in the root of the application file, update it accordingly.

    + EXTERNAL FILES -
        This section contains path to required files that is neccessary at the first time app starting.
        The supported format for these reports are: "XLSX", "XLS", "CSV-UTF8"

        bom_heriarchy   : SAP report "Bom Hierarchy final" (can be found by searching on search menu option right top)
        item_master     : All materials information from SAP "Item Master Data" (search * in the item master data)
        article_rates   : This file should contain articles stitching charges, printing charges and basic rate.
                        headers: "article", "stitch", "print", "basic"
                        data sample: 
                            article : 1111-br-g
                            stitch  : 28.2
                            print   : 4.1
                            basic   : 477

    + FIXED RATES - 
        This section contains the extra charges for an article, you can edit the rate or add more or even delete the existing one.
    Just make sure to use underscore "_" in keys instead of space.

    + CASE TYPES - You can add or delete it, just points the ending of SAP FG code. Like 1 in G1, 2 in G2 or L2 etc


    All other sections values can be changed not the keys



CALCULATION
______________

    Expressions used in the formula:

        - expenses_overheads : (decalred in config file)
        - sales_return = 1.01  (Sales Return = 1%  - decalred in config file)
        - sell_distr_royalty = 0.1725  (Selling and Distribution = 16.75%, Royalty = 0.50%  -  decalred in config file)

        - st_rate    : Stitching rate
        - pr_rate    : Printing rate
        - ba_rate    : Basic rate
        - mat_cost   : Total cost of materials as per bom calculated
        - cup	     : Cost of upper production
        - cop        : Cost of production
        - total_cost : Total cost
        - net_margin : Net margin


    Calcs:

        > cup (cost of upper prod) = (st_rate + pr_rate + mat_cost)
        > cop (cost of prod) = cup + expenses_overheads 
        > total_cost = ((ba_rate * sell_distr_royalty) + cop) * sales_return 
        > net_margin = (ba_rate - total_cost) / ba_rate
        > net_margin_percent = net_margin * 100 









