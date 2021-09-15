"""
Main module for the program excecution.

Made with ❤️ by kalaLokia
"""
import threading


from app import APPLOG
from app.base import App, MainApplication
from core.load_database import loadDatabase


if __name__ == "__main__":

    APPLOG.append(">>  Starting APP...")
    root = App()
    root.title("Create Cost Sheet")
    root.geometry("400x470")
    # root.iconbitmap("icon/dollar_bulb.ico")
    root.resizable(0, 0)

    thread = threading.Thread(target=loadDatabase, args=(root,))
    thread.daemon = True
    thread.start()
    root.mainloop()
