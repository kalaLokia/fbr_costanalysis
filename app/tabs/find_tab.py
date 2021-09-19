"""
Find article by searching.
"""
import re

from tkinter import Frame, StringVar, IntVar

from app import APPLOG
from app.frames.advanced_frames import ButtonAdvancedFrame
from app.frames.general_frames import InfoGeneralFrame
from app.frames.log_frame import LogFrame
from app.frames.search_frames import ExportButtonFrame, SearchBoxFrame
from core import settings
from core.article import Article
from core.bom import Bom
from core.cost_analysis import calculateProfit
from core.excel_report import ExcelReporting


class TabFind(Frame):
    def __init__(self, container, app) -> None:
        super().__init__(container)
        self.app = app
        self.bom = None

        self.art_list = self.app.artList
        self.art_description = tuple(self.art_list.keys())

        self.checkVar = IntVar()
        self.checkVar.set(1)
        self.log_msg = StringVar(self)
        self.var_pc = StringVar(self)
        self.var_sc = StringVar(self)
        self.var_cop = StringVar(self)
        self.var_netm = StringVar(self)
        self.var_mrp = StringVar(self)
        self.var_basic = StringVar(self)

        self.frame1 = SearchBoxFrame(self)
        self.frame2 = InfoGeneralFrame(self)
        self.frame3 = LogFrame(self)
        self.frame4 = ExportButtonFrame(self)

        self.log_msg.set(APPLOG[-1])

        self.frame1.pack()
        # self.frame2.pack(pady=20)
        self.frame3.pack(pady=20)
        # self.frame4.pack()

    @property
    def is_db(self):
        if self.app.bom_db.empty:
            return False
        else:
            return True

    def hide_info_frame(self) -> None:
        self.frame2.pack_forget()
        self.frame4.pack_forget()
        self.frame3.pack(pady=25)

    def show_info_frame(self, netm) -> None:
        self.frame3.pack_forget()
        self.frame2.pack(pady=5)
        self.frame4.pack(pady=5)
        if self.frame2.lbl_netm:
            if netm > 0:
                self.frame2.lbl_netm.config(foreground="#179900")
            elif netm < 0:
                self.frame2.lbl_netm.config(foreground="#f70f02")
            else:
                self.frame2.lbl_netm.config(foreground="#000")

    def on_keyrelease(self, event):

        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()

        # get data from art_description
        if value == "":
            data = self.art_description
        else:
            data = []
            for item in self.art_description:
                if self.checkVar.get():
                    if value in item.lower():
                        data.append(item)
                else:
                    all_re = ".*"
                    re_pattern = all_re + all_re.join([x for x in value]) + all_re
                    if re.search(re_pattern, item.lower()):
                        data.append(item)

        # update data in listBox
        self.frame1.listbox_update(data)

    def on_select(self, event):
        # display element selected on list
        cur_selection = event.widget.get(event.widget.curselection())
        # prev_selection = event.widget.get("active")

        # print("(event) previous:", prev_selection)
        # print("(event)  current:", cur_selection)
        # print("Selected: ", self.art_list[cur_selection])

        self.calculateNetMargin(self.art_list[cur_selection])

    def calculateNetMargin(self, sap_code):
        if self.bom:
            self.bom = None

        if not self.is_db:
            print("Accessing db failed.")
            return

        self.hide_info_frame()

        if self.app.article_db.empty:
            self.log_msg.set("Cannot calculate costs, rates file missing.")
            # print("Can't calculate netmargin, rates file missing.")
            return

        if not sap_code and not sap_code.lower().startswith("2-fb"):
            self.log_msg.set("No article selected.")
            return

        article = Article.from_sap_code(sap_code)
        self.bom = Bom(article=article)
        response = self.bom.createFinalBom(self.app.bom_db)
        if response["status"] == "OK":
            article = self.bom.article
            if article.article_code in self.app.article_db.article.values:
                rates = self.app.article_db[
                    self.app.article_db.article == article.article_code
                ].values[0]
                article.stitch_rate = float(rates[1])
                article.print_rate = float(rates[2])
                article.basic_rate = float(rates[3])

                data = calculateProfit(article, self.bom.get_cost_of_materials)

                self.show_info_frame(netm=data[2])
                self.var_netm.set(f"{data[2]}%")
                self.var_basic.set(f"₹{article.basic_rate}")
                self.var_mrp.set(f"₹{article.mrp}")
                self.var_sc.set(f"₹{article.stitch_rate}")
                self.var_pc.set(f"₹{article.print_rate}")
                self.var_cop.set(f"₹{data[0]}")

            else:
                self.log_msg.set(
                    f'{self.bom.article.article_name} is not in "{settings.ARTICLE_RATES_DIR}"'
                )
                # print(f"{bom.article} is not in rates file.")
                return

        else:
            self.log_msg.set(response.get("message", "Something bad happened."))
            # print(f"Response: {response}")
            return

    def exportExcelReport(self):
        if not self.bom:
            self.log_msg.set("No article selected to export.")
            # print(f"Response: {response}")
            return
        reporting = ExcelReporting(
            self.bom.article,
            self.bom.rexine_df,
            self.bom.component_df,
            self.bom.moulding_df,
            self.bom.packing_df,
        )
        response = reporting.generateTable()

        self.log_msg.set(response.get("message", "Something bad happened."))
        self.hide_info_frame()
