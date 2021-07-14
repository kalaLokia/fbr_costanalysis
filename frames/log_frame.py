from tkinter.ttk import Frame, Label
from tkinter import Message


class LogFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, *args, **kwargs)

        Message(
            self,
            textvariable=tab.log_msg,
            font=("Halvetica", 10, "italic"),
            background="#feffad",
            width=300,
        ).pack(pady=25)
