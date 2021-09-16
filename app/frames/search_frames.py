"""
Frames for Search box tab
"""
from tkinter import Frame, Listbox, Entry
from tkinter.constants import DISABLED, NORMAL
from tkinter.ttk import Button


class SearchBoxFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        self.seachBox = Entry(self, width=31, bd=4, font=("Halvetica 14"))
        self.seachBox.pack()
        self.seachBox.bind("<KeyRelease>", tab.on_keyrelease)

        self.listBox = Listbox(
            self, width=50, height=12, font=("Calibri 11"), bg="#c9fffc"
        )
        self.listBox.pack()
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
