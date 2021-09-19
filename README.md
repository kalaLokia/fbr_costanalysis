# Cost Analysis
Cost analysis of all articles using python tkinter UI, pandas and XlsxWriter.


Made with ❤️ by kalaLokia

<br/>

## Intro
The application is for calculating cost of an article by extracting the bill of materials of the article from SAP "bom heirarchy" report,
that contains complete heirarchial representation of every article in the unit. 

<br/>

## Configuration
*The configuration file (`.config.ini`) is in the root of the application file, update it accordingly.*

+ **EXTERNAL FILES** - This section contains path to required files that is neccessary at the first time app starting to create a database. The supported format for these reports are: "XLSX", "XLS", "CSV-UTF8"

    > **bom_heriarchy**   : *SAP report "Bom Hierarchy final" (can be found by searching on search menu option right top)*
    
    > **item_master**     : *All materials information from SAP "Item Master Data" (search * in the item master data)*
    
    > **article_rates**   : *This file should contain articles stitching charges, printing charges and basic rate.* `table headers: "article", "stitch", "print", "basic"` and  `data sample: "1111-br-g", "28.2", "4.1", "477"`

+ **FIXED RATES** - 
    This section contains the extra charges for an article, you can edit the rate or add more or even delete the existing one.
Just make sure to use underscore "_" in keys instead of space (eg: `wastage_and_benefits`).

+ **CASE TYPES** - You can add or delete it, just points the ending of SAP FG code. Like 1 in G1, L1 or B1 and 2 in G2 or L2 etc


All other sections values can be changed not the keys

<br/>

## Setup
1. Make sure you have *bom_heriarchy* and *item_master* files in the desired folder (default: "data" folder). This is required when running app for first time.
2. Check and update `.config.ini` accordinlgy. 
3. Start the app (`runapp.exe`)
    * App will check for the database. and if it is missing it will create one in directory "data" that requires the files in the step 1.
    * If you ever want to update the database, just delete the `bom.db` file in directory "data" and relanuch the app.
4. For analyzing the cost of article, that article details has to be in *article_rates* file in the external files section.
5. For bulk creation of cost analysis report, a file(format: csv/excel) of *article_rates* need to be selected, by default it will show report of all articles in the *article_rates* external file. 
6. Cost sheet(s) exported will be saved to the directory "files" in the root of the application.
7. Enjoy

<br/>

## Calculations

    Expressions used in the formula:

        - expenses_overheads : Fixed Rates (decalred in config file)
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

<br/>