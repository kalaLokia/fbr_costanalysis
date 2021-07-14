from tkinter.ttk import Frame, Button, Label, Entry, OptionMenu, Combobox


class ButtonGeneralFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        # Button
        self.btnCreate = Button(
            self, text="Create", command=tab.exportCostSheet, style="B1.TButton"
        ).grid(row=0, column=0, padx=10)
        self.btnNetMargin = Button(
            self, text="Net margin", command=tab.calculateNetMargin, style="B1.TButton"
        ).grid(
            row=0, column=1
        )  # findNetMargin


class EntryGeneralFrame(Frame):
    CASE_TYPES = ["1", "2", "3", "2-P6", "3-P6"]
    CATEGORIES = ["Gents", "Ladies", "Giants", "Boys", "Girls", "Kids", "Children"]
    BRANDS = [
        "PRIDE",
        "DEBONGO",
        "VKC DEBONGO",
        "KAPERS",
        "STILE",
        "L.PRIDE",
        "SMARTAK",
    ]

    txtSize = 12
    lblSize = 10
    txtPady = 5
    txtPadx = 20

    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        # Widgets
        # Labels in the frame
        Label(self, text="Brand", font=("Halvetica", self.lblSize)).grid(
            row=0, column=0, sticky="w"
        )
        Label(self, text="Article", font=("Halvetica", self.lblSize)).grid(
            row=0 + 1, column=0, sticky="w"
        )
        Label(self, text="Color", font=("Halvetica", self.lblSize)).grid(
            row=0 + 2, column=0, sticky="w"
        )
        Label(self, text="Category", font=("Halvetica", self.lblSize)).grid(
            row=0 + 3, column=0, sticky="w"
        )
        Label(self, text="Size", font=("Halvetica", self.lblSize)).grid(
            row=0 + 4, column=0, sticky="w"
        )
        Label(self, text="Case Code", font=("Halvetica", self.lblSize)).grid(
            row=0 + 5, column=0, sticky="w"
        )
        # Label semicolon in frame
        for i in range(0, 6):
            Label(self, text=":", font=("Halvetica", self.lblSize)).grid(
                row=i,
                column=1,
            )

        # Text Box for entering input
        self.artno = Entry(self, width=10, font=("Halvetica", self.txtSize))
        self.color = Entry(self, width=10, font=("Halvetica", self.txtSize))
        self.size = Entry(self, width=5, font=("Halvetica", self.txtSize))

        # Option Menu
        self.brand = OptionMenu(self, tab.var_brand, self.BRANDS[0], *self.BRANDS)
        self.category = OptionMenu(
            self, tab.var_category, self.CATEGORIES[0], *self.CATEGORIES
        )
        self.case_type = Combobox(self, textvariable=tab.var_casetype, width=12)

        # Align User Input Widgets
        self.brand.grid(
            row=0,
            column=2,
            columnspan=2,
            padx=self.txtPadx,
            pady=self.txtPady,
            sticky="ew",
        )
        self.artno.grid(
            row=1,
            column=2,
            padx=self.txtPadx,
            pady=self.txtPady,
        )
        self.color.grid(
            row=2,
            column=2,
            padx=self.txtPadx,
            pady=self.txtPady,
        )
        self.category.grid(
            row=3,
            column=2,
            padx=self.txtPadx,
            pady=self.txtPady,
            sticky="ew",
        )
        self.size.grid(
            row=4,
            column=2,
            padx=self.txtPadx,
            pady=self.txtPady,
            sticky="w",
        )
        self.case_type.grid(
            row=5,
            column=2,
            padx=self.txtPadx,
            pady=self.txtPady,
            sticky="w",
        )

        # default values
        tab.var_casetype.set(self.CASE_TYPES[0])
        self.case_type["values"] = self.CASE_TYPES
        self.size.insert(0, "8")


class InfoGeneralFrame(Frame):
    COL_GREEN = "#179900"
    COL_RED = "#f70f02"
    COL_NETM = "#000"
    COL_BLUE_LT = "#049dc7"
    COL_BLUE = "#0940e6"

    rate_txt = 15
    rate_txt2 = 12
    name_txt = 9
    name_txt2 = 8
    pad_x = 10

    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        Label(self, text="Stitching Charges", font=("Halvetica", self.name_txt2)).grid(
            row=1, column=0, sticky="ns", padx=self.pad_x
        )
        Label(self, text="Printing Charges", font=("Halvetica", self.name_txt2)).grid(
            row=1, column=1, sticky="ns", padx=self.pad_x
        )
        Label(self, text="Cost of Production", font=("Halvetica", self.name_txt2)).grid(
            row=1, column=2, sticky="ns", padx=self.pad_x
        )
        Label(
            self, textvariable=tab.var_sc, font=("Halvetica", self.rate_txt2, "bold")
        ).grid(row=0, column=0, sticky="ns", padx=self.pad_x)
        Label(
            self, textvariable=tab.var_pc, font=("Halvetica", self.rate_txt2, "bold")
        ).grid(row=0, column=1, sticky="ns", padx=self.pad_x)
        Label(
            self, textvariable=tab.var_cop, font=("Halvetica", self.rate_txt2, "bold")
        ).grid(row=0, column=2, sticky="ns", padx=self.pad_x)
        Label(self, text="").grid(row=2, column=1)
        self.lbl_netm = Label(
            self,
            textvariable=tab.var_netm,
            font=("Halvetica", self.rate_txt, "bold"),
            foreground=self.COL_NETM,
            background="#fff",
        )
        self.lbl_netm.grid(row=3, column=0, sticky="ns", padx=self.pad_x)
        Label(self, text="Net margin", font=("Halvetica", self.name_txt)).grid(
            row=4, column=0, sticky="ns", padx=self.pad_x
        )
        Label(
            self,
            textvariable=tab.var_mrp,
            font=("Halvetica", self.rate_txt, "bold"),
            foreground=self.COL_BLUE,
            background="#fff",
        ).grid(row=3, column=1, sticky="ns", padx=self.pad_x)
        Label(self, text="MRP", font=("Halvetica", self.name_txt)).grid(
            row=4, column=1, sticky="ns", padx=self.pad_x
        )
        Label(
            self,
            textvariable=tab.var_basic,
            font=("Halvetica", self.rate_txt, "bold"),
            foreground=self.COL_BLUE_LT,
            background="#fff",
        ).grid(row=3, column=2, sticky="ns", padx=self.pad_x)
        Label(self, text="Basic Rate", font=("Halvetica", self.name_txt)).grid(
            row=4, column=2, sticky="ns", padx=self.pad_x
        )
