"""
All Advanced tab related logic here.
"""

from datetime import datetime
import threading
from tkinter import filedialog as fd
from tkinter import StringVar
from tkinter.ttk import Frame

import pandas as pd

from app import APPLOG
from app.frames.advanced_frames import ChooseFileFrame, ButtonAdvancedFrame
from app.frames.log_frame import LogFrame, LogStatus
from core.article import Article
from core.bom import Bom
from core.cost_analysis import costAnalysisReport
from core.excel_report import ExcelReporting


class TabAdvanced(Frame):
    def __init__(self, container, app) -> None:
        super().__init__(container)
        self.app = app
        self.artinfo_db = pd.DataFrame()

        self.log_msg = StringVar(self)
        self.log_status = StringVar(self)
        self.picked_file = StringVar(self)
        self.log_msg.set(APPLOG[-1])
        self.log_status.set("\u2591" * 31)
        self.picked_file.set("No file selected")

        self.frame1 = ChooseFileFrame(self)
        self.frame2 = ButtonAdvancedFrame(self)
        self.frame3 = LogFrame(self)
        self.frame4 = LogStatus(self)

        self.frame1.pack(pady=35)
        self.frame2.pack(pady=25)
        self.frame3.pack(pady=5)
        self.frame4.pack(pady=15)

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
        if not self.is_db:
            return

        if self.artinfo_db.empty:
            if self.app.article_db.empty:
                self.log_msg.set("Please choose a valid csv file!")
                return
            self.artinfo_db = self.app.article_db

        def wrapped_func(self: TabAdvanced):
            cost_materials = []
            mrp_article = []
            length = 31
            count = self.artinfo_db.shape[0] / length
            for i, row in self.artinfo_db.iterrows():
                status = int(i / count)
                self.log_status.set("\u2588" * status + "\u2591" * (length - status))
                if len(row) >= 4:
                    # print(f"Articles Found: {1}")
                    item = row[0]
                    rates = (row[1], row[2], row[3])
                    article = Article.from_bulk_list(item, rates)

                    bom = Bom(article=article)
                    response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
                    # print(f"Response: {response}")
                    if response["status"] == "OK":
                        cost_materials.append(bom.get_cost_of_materials)
                        mrp_article.append(bom.get_article_mrp)
                    else:
                        cost_materials.append(0)
                        mrp_article.append(0)

            self.frame2.enableButtons()

            # Creating data
            df = costAnalysisReport(self.artinfo_db, mrp_article, cost_materials)
            filename = "files/Cost Analysis Report [{0}].csv".format(
                datetime.now().strftime("%d%m%y%H%M%S")
            )
            df.to_csv(filename)
            self.log_msg.set(f"Successfully created the report : {filename}")
            # print(f"Report ready. {filename}")
            self.log_status.set("\u2588" * length)

        self.frame2.disableButtons()
        self.log_msg.set("Please wait...")
        thread = threading.Thread(target=wrapped_func, args=(self,))
        thread.daemon = True
        thread.start()

    def generateBulkCostsheet(self):

        if not self.is_db:
            return

        if self.artinfo_db.empty:
            if self.app.article_db.empty:
                self.log_msg.set("Please choose a valid csv file!")
                return
            self.artinfo_db = self.app.article_db

        def wrapped_func(self):
            failed_list = []
            length = 31
            count = self.artinfo_db.shape[0] / length
            for i, row in self.artinfo_db.iterrows():
                status = int(i / count)
                self.log_status.set("\u2588" * status + "\u2591" * (length - status))
                if len(row) >= 4:
                    item = row[0]
                    rates = (row[1], row[2], row[3])
                    article = Article.from_bulk_list(item, rates)
                    bom = Bom(article=article)
                    response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
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
                            failed_list.append(article.article_name)
                    else:
                        failed_list.append(article.article_name)
                else:
                    print("Invalid data in the file, can't excecute. EXITING...")
                    break

            fail_name = "files/failed_{0}.txt".format(
                datetime.now().strftime("%d%m%y%H%M%S")
            )

            if failed_list:
                with open(fail_name, "w") as f:
                    for item in failed_list:
                        f.write("%s\n" % item)
            self.log_status.set("\u2588" * length)
            self.log_msg.set(
                f'Completed exporting reports to directory "files", {len(failed_list)} skipped.'
            )

        self.log_msg.set("Please wait...")
        thread = threading.Thread(target=wrapped_func, args=(self,))
        thread.daemon = True
        thread.start()
