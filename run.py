import tkinter as tk

from starter import Starter

games = {
    "KoiKoi": None,
    "Sevens": None,
    "OldMaid": None
}

starter = Starter(tk.Tk(), games)
starter.pack()
starter.mainloop()

