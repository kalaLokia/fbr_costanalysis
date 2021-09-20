"""
Main module for the program excecution.

Made with ❤️ by kalaLokia
"""
import threading


from app import APPLOG
from app.base import App, MainApplication
from core.load_database import loadDatabase


if __name__ == "__main__":

    APPLOG.append("Made with ❤️ by Fortune Branch")
    APPLOG.append(">>  Starting APP...")
    root = App()
    root.title("Fortune Br - Analyse Article")
    root.geometry("400x480")
    root.iconbitmap("miscellaneous/iconb.ico")
    root.resizable(0, 0)

    thread = threading.Thread(target=loadDatabase, args=(root,))
    thread.daemon = True
    thread.start()
    root.mainloop()
