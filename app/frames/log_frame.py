# from tkinter.ttk import Frame,
from tkinter import Message, Frame


class LogFrame(Frame):
    def __init__(self, tab, *args, **kwargs) -> None:
        super().__init__(tab, background="#feffad", *args, **kwargs)
        # s = Style()
        # s.configure('My.TFrame', background='#feffad')
        Message(
            self,
            textvariable=tab.log_msg,
            font=("Halvetica", 10, "italic"),
            background="#feffad",
            width=360,
        ).pack(anchor="w", padx=10, pady=10)
