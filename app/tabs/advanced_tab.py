from datetime import datetime

import pandas as pd
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter.ttk import Frame

from app.frames.advanced_frames import ChooseFileFrame, ButtonAdvancedFrame
from app.frames.log_frame import LogFrame
from core.bom import Bom
from core.article import Article
from core.excel_report import ExcelReporting
from core.cost_analysis import costAnalysisReport


class TabAdvanced(Frame):
    def __init__(self, container, app) -> None:
        super().__init__(container)
        self.app = app
        self.artinfo_db = pd.DataFrame()

        self.log_msg = StringVar(self)
        self.picked_file = StringVar(self)
        self.log_msg.set("Message logging enabled")
        self.picked_file.set("No file selected")

        frame1 = ChooseFileFrame(self)
        frame2 = ButtonAdvancedFrame(self)
        frame3 = LogFrame(self)

        frame1.pack(pady=35)
        frame2.pack(pady=25)
        frame3.pack(pady=15)

    @property
    def is_db(self):
        if self.app.bom_db.empty and self.app.items_db.empty:
            return False
        else:
            return True

    def openFile(self):
        print("f : Opening File")
        filename = fd.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.picked_file.set(filename)
        try:
            self.artinfo_db = pd.read_csv(filename)
        except:
            self.log_msg.set(f"Unable to fetch data from the given file: {filename}")
            print(f"Unable to fetch data from the given file: {filename}")

        if self.artinfo_db.shape[1] != 4:
            self.log_msg.set("Correpted file. Accepts only 4 columns.")
            print("Rates file can only have 4 columns.")

        elif self.artinfo_db[self.artinfo_db.columns[0]].isnull().values.any():
            self.log_msg.set(
                "Correpted file. Some article name is not provided in the data."
            )
            print("Article name can't be blank in rates file.")

        else:
            self.log_msg.set(f"Successfully fetched data from the given file.")
            print("Provided file loaded successfully.")

    def generateNetMarginReport(self):
        print("f: Calculate bulk net margin")
        if not self.is_db:
            return

        if self.artinfo_db.empty:
            if self.app.article_db.empty:
                self.log_msg.set("Please choose a valid csv file!")
                return
            self.artinfo_db = self.app.article_db

        cost_materials = []
        mrp_article = []

        for i, row in self.artinfo_db.iterrows():
            if len(row) >= 4:
                print(f"Articles Found: {1}")
                item = row[0]
                rates = (row[1], row[2], row[3])
                article = Article.from_bulk_list(item, rates)

                bom = Bom(article=article)
                response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
                print(f"Response: {response}")
                if response["status"] == "OK":
                    cost_materials.append(bom.get_cost_of_materials)
                    mrp_article.append(bom.get_article_mrp)
                else:
                    cost_materials.append(0)
                    mrp_article.append(0)

        # Creating data
        df = costAnalysisReport(self.artinfo_db, mrp_article, cost_materials)
        filename = "files/report_{0}.csv".format(
            datetime.now().strftime("%d%m%y%H%M%S")
        )
        df.to_csv(filename)
        self.log_msg.set(f"Successfully created the report : {filename}")
        print(f"Report ready. {filename}")

    def generateBulkCostsheet(self):
        print("f : Bulk costsheet creation")
        if not self.is_db:
            return

        if self.artinfo_db.empty:
            if self.app.article_db.empty:
                self.log_msg.set("Please choose a valid csv file!")
                return
            self.artinfo_db = self.app.article_db

        failed_list = []

        for _, row in self.artinfo_db.iterrows():
            if len(row) >= 4:
                item = row[0]
                rates = (row[1], row[2], row[3])
                article = Article.from_bulk_list(item, rates)
                # print(f"Article: {article.article_code} - {i}")
                bom = Bom(article=article)
                response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
                # print(f"{i} Response: {response} = {article.article_code}")
                if response["status"] == "OK":
                    article.mrp = bom.article.mrp
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

        self.log_msg.set(f"Task completed, {len(failed_list)} skipped.")
        fail_name = "files/failed_{0}.txt".format(
            datetime.now().strftime("%d%m%y%H%M%S")
        )

        if failed_list:
            with open(fail_name, "w") as f:
                for item in failed_list:
                    f.write("%s\n" % item)
