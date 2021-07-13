Mandatory Files : in directory "data" in the root of the exe file
_______________________

+ bom file name       : "Bom Hierarchy final.csv"  [ From SAP query: bom heirarchy final ]
+ material file name  : "materials.csv"   [ From SAP: all in item master data (find by searching a single * in search area) ]

Optional  : in directory "data" in the root of the exe file
_______________________

+ article file name   : "articles.csv"   [ Columns in order: "article, stitch, print, basic" ]


ERROR CODES
_______________________

1. ERR 40  : database file not found or is not in CSV format or name mistake (case sensitive). 

Notes: 
- For bulk cost sheet file creation, max 5 seconds required per file. (for normal system it is < 1 second)
- If program stuck for more than 3 minutes, kill it by using windows task manager.
- Never allow program to get stuck more than 15 minutes.


###############################################################################
####       BULK CREATION OF COSTSHEET OR CALCULATION OF NET MARGIN         ####
###############################################################################
- Providing file for bulk calculation must be a "CSV" file.
- Columns in the provided csv must be in the order : article, print, stitch, basic




#############################################
########     CALCULATIONS            ########
#############################################

Constants:
- expenses_overheads = 19.04
- sell_distr_royalty = 0.1725  (Selling and Distribution = 16.75%, Royalty = 0.50%)
- sales_return = 1.01  (Sales Return = 1%)

Expressions:
- st_rate    : Stitching rate
- pr_rate    : Printing rate
- ba_rate    : Basic rate
- mat_cost   : Total cost of materials as per bom calculated
- cup	     : Cost of upper production
- cop        : Cost of production
- total_cost : Total cost
- net_margin : Net margin


Calcs:
______________

> cup (cost of upper prod) = (st_rate + pr_rate + mat_cost)
> cop (cost of prod) = cup + expenses_overheads 
> total_cost = ((ba_rate * sell_distr_royalty) + cop) * sales_return 
> net_margin = (ba_rate - total_cost) / ba_rate
> net_margin_percent = net_margin * 100 

#####################################################################







