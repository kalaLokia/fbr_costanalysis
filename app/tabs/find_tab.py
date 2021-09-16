"""
Find article by searching.
"""

from tkinter import Frame, Listbox, Entry

from app import APPLOG


class TabFind(Frame):
    def __init__(self, container, app) -> None:
        super().__init__(container)

        self.app = app
        self.art_list = None
        if self.app.artList:
            self.art_list = self.app.artList
        self.test_list = tuple(self.art_list.keys())

        self.entry = Entry(self, width=31, bd=4, font=("Helvetica 14"))
        self.entry.pack()
        self.entry.bind("<KeyRelease>", self.on_keyrelease)

        self.listbox = Listbox(
            self, width=50, height=12, font=("Calibri 11"), bg="#c9fffc"
        )
        self.listbox.pack()
        # listbox.bind('<Double-Button-1>', on_select)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox_update(self.test_list)

    def on_keyrelease(self, event):

        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()

        # get data from test_list
        if value == "":
            data = self.test_list
        else:
            data = []
            for item in self.test_list:
                if value in item.lower():
                    data.append(item)

        # update data in listbox
        self.listbox_update(data)

    def listbox_update(self, data):
        # delete previous data
        self.listbox.delete(0, "end")

        # sorting data
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            self.listbox.insert("end", item)

    def on_select(self, event):
        # display element selected on list
        cur_selection = event.widget.get(event.widget.curselection())
        prev_selection = event.widget.get("active")

        print("(event) previous:", prev_selection)
        print("(event)  current:", cur_selection)
        print("Selected: ", self.art_list[cur_selection])

    # --- main ---
