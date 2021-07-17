"""
Design for all frames inside advanced tab.
"""

from tkinter.constants import DISABLED, NORMAL
from tkinter.ttk import Button, Frame, Entry


class ChooseFileFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        Entry(
            self,
            textvariable=tab.picked_file,
            width=40,
            font=("Halvetica", 8),
            state="readonly",
        ).grid(row=0, column=0)

        Button(self, text="Choose File", command=tab.openFile, style="B2.TButton").grid(
            row=0, column=1, padx=10
        )


class ButtonAdvancedFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        self.b1 = Button(
            self,
            text="Export Cost Report",
            command=tab.generateNetMarginReport,
            padding=10,
            style="B1.TButton",
        )

        self.b2 = Button(
            self,
            text="Export All Costsheets",
            command=tab.generateBulkCostsheet,
            padding=10,
            style="B1.TButton",
        )
        self.b1.pack()
        self.b2.pack(pady=20)

    def disableButtons(self):
        self.b1["state"] = DISABLED
        self.b2["state"] = DISABLED

    def enableButtons(self):
        self.b1["state"] = NORMAL
        self.b2["state"] = NORMAL
