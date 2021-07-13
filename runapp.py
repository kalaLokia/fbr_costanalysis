"""
This is the main file for excecution in tkinter UI

Made by kalaLokia
Github: https://github.com/kalalokia/python
"""

from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
import pandas as pd

from bom import Bom
from excel_report import ExcelReporting
from article import Article
from net_margin import calculateNetMargin, calculateNetMarginSingle

BOM_DATA_DIR = "data/Bom Hierarchy final.csv"
ITEM_DATA_DIR = "data/materials.csv"
ARTINFO_DIR = "data/articles.csv"
ARTLIST_DB = pd.DataFrame()

CASE_TYPES = ["1", "2", "3", "2-P6", "3-P6"]
CATEGORIES = ["Gents", "Ladies", "Giants", "Boys", "Girls", "Kids", "Children"]
BRANDS = ["PRIDE", "DEBONGO", "VKC DEBONGO", "KAPERS", "STILE", "L.PRIDE", "SMARTAK"]
APP_LOG = "I am ready!"

COL_GREEN = "#179900"
COL_RED = "#f70f02"
COL_BLUE_LT = "#049dc7"
COL_BLUE = "#0940e6"
COL_NORMAL = "#3a8c29"


# Reading File
print("Trying to fetch data from data/*.csv files.")
try:
    bom_db = pd.read_csv(BOM_DATA_DIR)
    items_db = pd.read_csv(ITEM_DATA_DIR)
    APP_LOG = "I got the database, I am ready now ;-)"
    print("Database ready!")

except FileNotFoundError:
    APP_LOG = "Uhh ohh, I don't find the required files. [ERR: 40]"
    print("Requird files not found in the directory data.")
except:
    bom_db = None
    items_db = None
    print("Something I didn't understand, please report.")

try:
    ARTINFO_DB = pd.read_csv(ARTINFO_DIR)
    ARTINFO_DB["article"] = ARTINFO_DB["article"].str.lower()
    ARTINFO_DB.fillna(0)
except FileNotFoundError:
    print("Article rate file not found")
except:
    print("Something wrong with rates file, please report.")

print("Opening GUI..")

# Button For creating a single costsheet of an article # Main Frame
def createCostSheet():
    print("f : Create costsheet")
    hide_info_frame()
    article = Article(
        brand=var_brand.get(),
        artno=artno.get(),
        color=color.get(),
        size=int(size.get()),
        case_type=var_casetype.get(),
    )
    article.category = var_category.get()
    bom = Bom(article=article)
    response = bom.createFinalBom(bom_db, items_db)
    print(f"Response: {response}")
    if response["status"] == "OK":
        article = bom.article
        if not ARTINFO_DB.empty:
            if article.article_code in ARTINFO_DB.article.values:
                rates = ARTINFO_DB[ARTINFO_DB.article == article.article_code].values[0]
                article.stitch_rate = float(rates[1])
                article.print_rate = float(rates[2])
                article.basic_rate = float(rates[3])

        var_log.set(response.get("message", "Something bad happened."))
        reporting = ExcelReporting(
            article, bom.rexine_df, bom.component_df, bom.moulding_df, bom.packing_df
        )
        response = reporting.generateTable()
        print(f"Response: {response}")
        var_log.set(response.get("message", "Something bad happened."))
    else:
        var_log.set(response.get("message", "Something bad happened."))


def findNetMargin():
    """Calculate net margin of an article"""
    print("f : Calculate net margin")
    hide_info_frame()
    if ARTINFO_DB.empty:
        var_log.set("I didn't find file articles.csv in dir data.")
        print("Can't calculate netmargin, rates file missing.")
        return

    article = Article(
        brand=var_brand.get(),
        artno=artno.get(),
        color=color.get(),
        size=int(size.get()),
        case_type=var_casetype.get(),
    )
    article.category = var_category.get()
    bom = Bom(article=article)
    response = bom.createFinalBom(bom_db, items_db)
    print(f"Response: {response}")
    if response["status"] == "OK":
        article = bom.article
        if article.article_code in ARTINFO_DB.article.values:
            rates = ARTINFO_DB[ARTINFO_DB.article == article.article_code].values[0]
            article.stitch_rate = float(rates[1])
            article.print_rate = float(rates[2])
            article.basic_rate = float(rates[3])

            data = calculateNetMarginSingle(article, bom.get_cost_of_materials)

            show_info_frame()
            var_netm.set(f"{data[2]}%")
            var_basic.set(f"₹{article.basic_rate}")
            var_mrp.set(f"₹{article.mrp}")
            var_sc.set(article.stitch_rate)
            var_pc.set(article.print_rate)
            var_cop.set(data[0])
            # var_log.set(
            #     f"NET MRGN: {data[2]}% | MRP: {article.mrp} | BASIC: {article.basic_rate} | COP: {data[0]}"
            # )
        else:
            var_log.set(f'{bom.article} is not in "articles.csv" file.')
            print(f'{bom.article} is not in "articles.csv" file.')
            return
    else:
        var_log.set(response.get("message", "Something bad happened."))
        return


def openFile():
    global ARTLIST_DB
    print("f : Opening File")
    filename = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
    var_filename.set(filename)
    try:
        ARTLIST_DB = pd.read_csv(filename)
    except:
        var_log2.set(f"Unable to fetch data from the given file: {filename}")
        print(f"Unable to fetch data from the given file: {filename}")

    if ARTLIST_DB.shape[1] != 4:
        ARTLIST_DB = None
        var_log2.set("Correpted file. Accepts only 4 columns.")
        print("Rates file can only have 4 columns.")

    elif ARTLIST_DB[ARTLIST_DB.columns[0]].isnull().values.any():
        ARTLIST_DB = None
        var_log2.set("Correpted file. Some article name is not provided in the data.")
        print("Article name can't be blank in rates file.")

    else:
        var_log2.set(f"Successfully fetched data from the given file.")
        print("Provided file loaded successfully.")


# Button for calculating Margin of list of articles
def calculateMargin():
    """
    Creates a cost report of list of articles provided.

    Requires art_code, stitch, print, basic rate of articles in the supplied csv file.
    """
    global ARTLIST_DB
    cost_materials = []
    mrp_article = []
    print("f: Calculate bulk net margin")
    if ARTLIST_DB is None:
        var_log2.set("Please choose a valid csv file!")
        print("Invalid rates file.")
        return

    for i, row in ARTLIST_DB.iterrows():
        if len(row) >= 4:
            print(f"Articles Found: {1}")
            item = row[0]
            rates = (row[1], row[2], row[3])
            article = Article.from_bulk_list(item, rates)

            bom = Bom(article=article)
            response = bom.createFinalBom(bom_db, items_db)
            print(f"Response: {response}")
            if response["status"] == "OK":
                cost_materials.append(bom.get_cost_of_materials)
                mrp_article.append(bom.get_article_mrp)
            else:
                cost_materials.append(0)
                mrp_article.append(0)

    # Creating data
    df = calculateNetMargin(ARTLIST_DB, mrp_article, cost_materials)
    filename = "files/report_{0}.csv".format(datetime.now().strftime("%d%m%y%H%M%S"))
    df.to_csv(filename)
    var_log2.set(f"Successfully created the report : {filename}")
    print(f"Report ready. {filename}")


# Button for bulk cost sheet creation
def generateBulkCS():
    global ARTLIST_DB
    failed_list = []
    print("f : Bulk costsheet creation")
    if ARTLIST_DB is None:
        var_log2.set("Please choose a valid csv file!")
        return

    # var_log2.set("Please wait..! I am creating your files.")
    print("Trying for bulk costsheet creation, please hold on a bit.")
    for i, row in ARTLIST_DB.iterrows():
        if len(row) >= 4:
            item = row[0]
            rates = (row[1], row[2], row[3])
            article = Article.from_bulk_list(item, rates)
            print(f"Article: {article.article_code} - {i}")
            bom = Bom(article=article)
            response = bom.createFinalBom(bom_db, items_db)
            print(f"{i} Response: {response} = {article.article_code}")
            if response["status"] == "OK":
                article.mrp = bom.bom_df.mrp.iloc[0]
                article.pairs_in_case = bom.get_pairs_in_mc
                reporting = ExcelReporting(
                    article,
                    bom.rexine_df,
                    bom.component_df,
                    bom.moulding_df,
                    bom.packing_df,
                )
                response = reporting.generateTable()
                if not response["status"] == "CREATED":
                    failed_list.append(article.article_code)
            else:
                failed_list.append(article.article_code)
        else:
            print("Invalid data in the file, can't excecute. EXITING...")
            break

    var_log2.set(f"Task completed, {len(failed_list)} skipped.")
    fail_name = "files/failed_{0}.txt".format(datetime.now().strftime("%d%m%y%H%M%S"))

    if failed_list:
        with open(fail_name, "w") as f:
            for item in failed_list:
                f.write("%s\n" % item)


def hide_info_frame():
    frame3.pack_forget()
    frame4.pack(pady=20)


def show_info_frame():
    frame4.pack_forget()
    frame3.pack(pady=5)


if __name__ == "__main__":

    # Widget constants
    txtSize = 12
    lblSize = 10
    txtPady = 5
    txtPadx = 20

    # Root configuration
    root = Tk()
    root.title("Create Cost Sheet")
    root.geometry("400x450")
    # root.iconbitmap("icon/dollar_bulb.ico")
    root.resizable(0, 0)

    # Notebook configuration
    notebook = Notebook(root, width=400, height=450, padding=10)
    notebook.pack()

    # Main Frames for tabs in notebook
    frameMainTab = Frame(notebook)
    frameSecondTab = Frame(notebook)

    # Sub frames
    frame = Frame(frameMainTab)
    frame2 = Frame(frameMainTab)
    frame3 = Frame(frameMainTab)
    frame4 = Frame(frameMainTab)
    frame5 = Frame(frameSecondTab)
    frame6 = Frame(frameSecondTab)

    # Style configuration for button
    style = Style(root)
    style2 = Style(root)
    style.configure("TButton", font=("Helvetica", 16))
    style2.configure("B2.TButton", font=("Helvetica", 9))

    # StringVars for widgets
    var_brand = StringVar(frame)
    var_category = StringVar(frame)
    var_casetype = StringVar(frame)
    var_log = StringVar(frame)
    var_log2 = StringVar(frame6)
    var_pc = StringVar(frame3)
    var_sc = StringVar(frame3)
    var_cop = StringVar(frame3)
    var_netm = StringVar(frame3)
    var_mrp = StringVar(frame3)
    var_basic = StringVar(frame3)

    # Widgets
    # Labels in frame1
    Label(frame, text="Brand", font=("Halvetica", lblSize)).grid(
        row=0, column=0, sticky="w"
    )
    Label(frame, text="Article", font=("Halvetica", lblSize)).grid(
        row=0 + 1, column=0, sticky="w"
    )
    Label(frame, text="Color", font=("Halvetica", lblSize)).grid(
        row=0 + 2, column=0, sticky="w"
    )
    Label(frame, text="Category", font=("Halvetica", lblSize)).grid(
        row=0 + 3, column=0, sticky="w"
    )
    Label(frame, text="Size", font=("Halvetica", lblSize)).grid(
        row=0 + 4, column=0, sticky="w"
    )
    Label(frame, text="Case Code", font=("Halvetica", lblSize)).grid(
        row=0 + 5, column=0, sticky="w"
    )
    # Label semicolon in frame1
    for i in range(0, 6):
        Label(frame, text=":", font=("Halvetica", lblSize)).grid(
            row=i,
            column=1,
        )

    # Text Box for entering input
    artno = Entry(frame, width=10, font=("Halvetica", txtSize))
    color = Entry(frame, width=10, font=("Halvetica", txtSize))
    size = Entry(frame, width=5, font=("Halvetica", txtSize))
    # Option Menu
    brand = OptionMenu(frame, var_brand, BRANDS[0], *BRANDS)
    category = OptionMenu(frame, var_category, CATEGORIES[0], *CATEGORIES)
    case_type = Combobox(frame, textvariable=var_casetype, width=12)

    # Align User Input Widgets
    brand.grid(
        row=0,
        column=2,
        columnspan=2,
        padx=txtPadx,
        pady=txtPady,
        sticky="ew",
    )
    artno.grid(
        row=1,
        column=2,
        padx=txtPadx,
        pady=txtPady,
    )
    color.grid(
        row=2,
        column=2,
        padx=txtPadx,
        pady=txtPady,
    )
    category.grid(
        row=3,
        column=2,
        padx=txtPadx,
        pady=txtPady,
        sticky="ew",
    )
    size.grid(
        row=4,
        column=2,
        padx=txtPadx,
        pady=txtPady,
        sticky="w",
    )
    case_type.grid(
        row=5,
        column=2,
        padx=txtPadx,
        pady=txtPady,
        sticky="w",
    )

    # Set default values
    var_log.set(APP_LOG)
    var_log2.set("...")
    var_casetype.set(CASE_TYPES[0])

    case_type["values"] = CASE_TYPES
    size.insert(0, "8")

    # Pack Frame1
    frame.pack(pady=20)

    ## FRAME 2
    # Button
    btnCreate = Button(
        frame2, text="Create", command=createCostSheet, style="TButton"
    ).grid(row=0, column=0, padx=10)
    btnNetMargin = Button(
        frame2, text="Net margin", command=findNetMargin, style="TButton"
    ).grid(row=0, column=1)

    # Pack Frame2
    frame2.pack(pady=10)

    ## Frame 3

    rate_txt = 15
    rate_txt2 = 12
    name_txt = 9
    name_txt2 = 8
    pad_x = 10

    Label(frame3, text="Stitching Charges", font=("Halvetica", name_txt2)).grid(
        row=1, column=0, sticky="ns", padx=pad_x
    )
    Label(frame3, text="Printing Charges", font=("Halvetica", name_txt2)).grid(
        row=1, column=1, sticky="ns", padx=pad_x
    )
    Label(frame3, text="Cost of Production", font=("Halvetica", name_txt2)).grid(
        row=1, column=2, sticky="ns", padx=pad_x
    )
    Label(frame3, textvariable=var_sc, font=("Halvetica", rate_txt2)).grid(
        row=0, column=0, sticky="ns", padx=pad_x
    )
    Label(frame3, textvariable=var_pc, font=("Halvetica", rate_txt2)).grid(
        row=0, column=1, sticky="ns", padx=pad_x
    )
    Label(frame3, textvariable=var_cop, font=("Halvetica", rate_txt2)).grid(
        row=0, column=2, sticky="ns", padx=pad_x
    )
    Label(frame3, text="").grid(row=2, column=1)
    Label(
        frame3,
        textvariable=var_netm,
        font=("Halvetica", rate_txt, "bold"),
        foreground=COL_NORMAL,
        background="#fff",
    ).grid(row=3, column=0, sticky="ns", padx=pad_x)
    Label(frame3, text="Net margin", font=("Halvetica", name_txt)).grid(
        row=4, column=0, sticky="ns", padx=pad_x
    )
    Label(
        frame3,
        textvariable=var_mrp,
        font=("Halvetica", rate_txt, "bold"),
        foreground=COL_BLUE,
    ).grid(row=3, column=1, sticky="ns", padx=pad_x)
    Label(frame3, text="MRP", font=("Halvetica", name_txt)).grid(
        row=4, column=1, sticky="ns", padx=pad_x
    )
    Label(
        frame3,
        textvariable=var_basic,
        font=("Halvetica", rate_txt, "bold"),
        foreground=COL_BLUE_LT,
    ).grid(row=3, column=2, sticky="ns", padx=pad_x)
    Label(frame3, text="Basic Rate", font=("Halvetica", name_txt)).grid(
        row=4, column=2, sticky="ns", padx=pad_x
    )

    # FRAME 4
    info_log = Message(
        frame4, textvariable=var_log, font=("Halvetica", 10), width=350
    ).pack(pady=10)
    frame4.pack(pady=20)

    ##############     TAB2      #################
    ## FRAME 4
    var_filename = StringVar(frame5)
    var_filename.set("No file selected")

    file_dir = Entry(
        frame5,
        textvariable=var_filename,
        width=30,
        font=("Halvetica", 8),
        state="readonly",
    ).grid(row=0, column=0)

    btnOpenFile = Button(
        frame5, text="Choose File", command=openFile, style="B2.TButton"
    ).grid(row=0, column=1, padx=10)
    frame5.pack(pady=20, padx=0)

    # Pack Frame4
    frame5.pack(pady=20, padx=0)

    ## FRAME 5
    btnCalculateProfit = Button(
        frame6,
        text="Calculate\nprofit/loss",
        command=calculateMargin,
        style="TButton",
    ).pack()

    btnGenerateCS = Button(
        frame6, text="Generate\nCostsheet", command=generateBulkCS, style="TButton"
    ).pack(pady=20)

    bulk_log = Label(frame6, textvariable=var_log2, font=("Halvetica", 9)).pack(pady=15)

    # Pack Frame5
    frame6.pack(pady=40, padx=0)

    ##
    frameMainTab.pack(fill="both", expand=1)
    frameSecondTab.pack(fill="both", expand=1)

    notebook.add(frameMainTab, text="General")
    notebook.add(frameSecondTab, text="Advanced")

    root.mainloop()
