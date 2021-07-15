from tkinter import StringVar
from tkinter.ttk import Frame

from app import APPLOG
from app.frames.log_frame import LogFrame
from app.frames.general_frames import (
    EntryGeneralFrame,
    ButtonGeneralFrame,
    InfoGeneralFrame,
)
from core.article import Article
from core.bom import Bom
from core.cost_analysis import calculateProfit
from core.excel_report import ExcelReporting
from core import settings


class TabGeneral(Frame):
    def __init__(self, container, app) -> None:
        super().__init__(container)
        self.app = app

        self.log_msg = StringVar(self)
        self.var_brand = StringVar(self)
        self.var_category = StringVar(self)
        self.var_casetype = StringVar(self)

        self.var_pc = StringVar(self)
        self.var_sc = StringVar(self)
        self.var_cop = StringVar(self)
        self.var_netm = StringVar(self)
        self.var_mrp = StringVar(self)
        self.var_basic = StringVar(self)

        self.frame1 = EntryGeneralFrame(self)
        self.frame2 = ButtonGeneralFrame(self)
        self.frame3 = InfoGeneralFrame(self)
        self.frame4 = LogFrame(self)

        self.log_msg.set(APPLOG[-1])

        self.frame1.pack(pady=20)
        self.frame2.pack(pady=10)
        # self.frame3.pack(pady=10)  # Initially hidden
        self.frame4.pack(pady=25)

    @property
    def is_db(self):
        if self.app.bom_db.empty and self.app.items_db.empty:
            return False
        else:
            return True

    def hide_info_frame(self) -> None:
        self.frame3.pack_forget()
        self.frame4.pack(pady=25)

    def show_info_frame(self, netm) -> None:
        self.frame3.pack(pady=10)
        self.frame4.pack_forget()
        if self.frame3.lbl_netm:
            if netm > 0:
                self.frame3.lbl_netm.config(foreground="#179900")
            elif netm < 0:
                self.frame3.lbl_netm.config(foreground="#f70f02")
            else:
                self.frame3.lbl_netm.config(foreground="#000")

    def exportCostSheet(self):
        print("f : Export costsheet")
        if not self.is_db:
            print("Accessing db failed.")
            return

        self.hide_info_frame()

        article = Article(
            brand=self.var_brand.get(),
            artno=self.frame1.artno.get(),
            color=self.frame1.color.get(),
            size=int(self.frame1.size.get()),
            case_type=self.var_casetype.get(),
        )
        article.category = self.var_category.get()

        bom = Bom(article=article)
        response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
        if response["status"] == "OK":
            article = bom.article
            if not self.app.article_db.empty:
                if article.article_code in self.app.article_db.article.values:
                    rates = self.app.article_db[
                        self.app.article_db.article == article.article_code
                    ].values[0]
                    article.stitch_rate = float(rates[1])
                    article.print_rate = float(rates[2])
                    article.basic_rate = float(rates[3])

            self.log_msg.set(response.get("message", "Something bad happened."))
            reporting = ExcelReporting(
                article,
                bom.rexine_df,
                bom.component_df,
                bom.moulding_df,
                bom.packing_df,
            )
            response = reporting.generateTable()

            self.log_msg.set(response.get("message", "Something bad happened."))
        else:
            self.log_msg.set(response.get("message", "Something bad happened."))

        print(f"Response: {response}")

    def calculateNetMargin(self):
        print("f : Calculate net margin")
        if not self.is_db:
            print("Accessing db failed.")
            return

        self.hide_info_frame()
        if self.app.article_db.empty:
            self.log_msg.set("Cannot calculate costs, rates file missing.")
            print("Can't calculate netmargin, rates file missing.")
            return

        article = Article(
            brand=self.var_brand.get(),
            artno=self.frame1.artno.get(),
            color=self.frame1.color.get(),
            size=int(self.frame1.size.get()),
            case_type=self.var_casetype.get(),
        )
        article.category = self.var_category.get()
        bom = Bom(article=article)
        response = bom.createFinalBom(self.app.bom_db, self.app.items_db)
        if response["status"] == "OK":
            article = bom.article
            if article.article_code in self.app.article_db.article.values:
                rates = self.app.article_db[
                    self.app.article_db.article == article.article_code
                ].values[0]
                article.stitch_rate = float(rates[1])
                article.print_rate = float(rates[2])
                article.basic_rate = float(rates[3])

                data = calculateProfit(article, bom.get_cost_of_materials)

                self.show_info_frame(netm=data[2])
                self.var_netm.set(f"{data[2]}%")
                self.var_basic.set(f"₹{article.basic_rate}")
                self.var_mrp.set(f"₹{article.mrp}")
                self.var_sc.set(f"₹{article.stitch_rate}")
                self.var_pc.set(f"₹{article.print_rate}")
                self.var_cop.set(f"₹{data[0]}")

            else:
                self.log_msg.set(
                    f'{bom.article.article_name} is not in "{settings.ARTICLE_RATES_DIR}"'
                )
                print(f"{bom.article} is not in rates file.")
                return
        else:
            self.log_msg.set(response.get("message", "Something bad happened."))
            print(f"Response: {response}")
            return
