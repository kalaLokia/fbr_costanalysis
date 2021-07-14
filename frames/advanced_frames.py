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

        Button(
            self,
            text="Calculate\nprofit/loss",
            command=tab.generateNetMarginReport,
            style="B1.TButton",
        ).pack()

        Button(
            self,
            text="Generate\nCostsheet",
            command=tab.generateBulkCostsheet,
            style="B1.TButton",
        ).pack(pady=20)
