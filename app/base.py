"""
Main Tkinter UI setup.
"""
from app.tabs.find_tab import TabFind
from tkinter import Tk, Frame, StringVar
from tkinter.ttk import Notebook, Style

from app.frames.log_frame import LogFrame
from app.tabs.advanced_tab import TabAdvanced
from app.tabs.general_tab import TabGeneral


class App(Tk):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.log_msg = StringVar(self)
        self.log_frame = LogFrame(self)
        self.log_frame.pack(
            fill="both", side="left", anchor="w", expand=True, padx=5, pady=5
        )

    def forgetLog(self) -> None:
        self.log_frame.pack_forget()


class MainApplication(Frame):
    def __init__(self, root, bomdb, artdb, artList, *args, **kwargs) -> None:
        super().__init__(root, *args, **kwargs)
        self.bom_db = bomdb
        self.article_db = artdb
        self.artList = artList

        style = Style(root)
        style.configure("B1.TButton", font=("Helvetica", 12))
        style.configure("B2.TButton", font=("Helvetica", 9))

        notebook = Notebook(root, width=400, height=470, padding=10)

        tab_general = TabGeneral(notebook, self)
        tab_advanced = TabAdvanced(notebook, self)
        tab_find = TabFind(notebook, self)

        notebook.add(tab_general, text="General")
        notebook.add(tab_advanced, text="Advanced")
        notebook.add(tab_find, text="Find")

        notebook.pack()
