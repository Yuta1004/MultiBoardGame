import tkinter as tk

from starter import Starter
# from games.template.main import Template

games = {
    # "Empty": Template
}

starter = Starter(tk.Tk(), games)
starter.pack()
starter.mainloop()
