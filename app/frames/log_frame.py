"""
Design of common log frame.
"""
from tkinter import Label, Message, Frame


class LogFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, background="#feffad", *args, **kwargs)

        Message(
            self,
            textvariable=tab.log_msg,
            font=("Halvetica", 10, "italic"),
            background="#feffad",
            width=360,
        ).pack(anchor="w", padx=10, pady=10)


class LogStatus(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(
            tab,
            width=360,
            highlightthickness=1,
            highlightbackground="#000",
            *args,
            **kwargs
        )

        Label(
            self,
            textvariable=tab.log_status,
            font=("Halvetica", 12, "italic"),
        ).pack(padx=6, pady=5)
