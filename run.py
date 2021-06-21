import tkinter as tk

from starter import Starter
from games.fordebug.main import ForDebugGame

games = {
    "Debug": ForDebugGame,
    "KoiKoi": None,
    "Sevens": None,
    "OldMaid": None
}

starter = Starter(tk.Tk(), games)
starter.pack()
starter.mainloop()

