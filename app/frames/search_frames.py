"""
Frames for Search box tab
"""
from tkinter import Frame, Listbox, Entry, Checkbutton, IntVar
from tkinter.constants import DISABLED, NORMAL
from tkinter.ttk import Button


class SearchBoxFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        self.seachBox = Entry(self, width=25, bd=4, font=("Halvetica 14"))
        self.seachBox.grid(row=0, column=0, padx=10)
        self.seachBox.bind("<KeyRelease>", tab.on_keyrelease)

        self.checkbox = Checkbutton(
            self,
            text="Strict",
            variable=tab.checkVar,
            onvalue=1,
            offvalue=0,
            height=3,
            # width=3,
        ).grid(row=0, column=1)

        self.listBox = Listbox(
            self, width=50, height=12, font=("Calibri 11"), bg="#c9fffc"
        )
        self.listBox.grid(row=1, column=0, columnspan=2, pady=10)
        # self.listBox.bind("<Double-Button-1>", tab.on_select)
        self.listBox.bind("<<ListboxSelect>>", tab.on_select)
        self.listbox_update(tab.art_description)

    def listbox_update(self, data):
        # delete previous data
        self.listBox.delete(0, "end")

        # sorting data
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            self.listBox.insert("end", item)


class ExportButtonFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        self.b1 = Button(
            self,
            text="Export",
            command=tab.exportExcelReport,
            padding=3,
            style="B2.TButton",
        )
        self.b1.pack()

    def disableButton(self):
        self.b1["state"] = DISABLED

    def enableButton(self):
        self.b1["state"] = NORMAL
