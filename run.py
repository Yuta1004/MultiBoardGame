import tkinter as tk

from starter import Starter
from games.template.main import Template

games = {
    "Empty": (Template, 4)      # "ゲーム名" : (ゲーム実行可能クラス, 人数上限)
}

starter = Starter(tk.Tk(), games)
starter.pack()
starter.mainloop()
