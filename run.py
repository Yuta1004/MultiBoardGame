import tkinter as tk

from starter import Starter
from game.example.main import Example

games = {
    "Example": (Example, 2)      # "ゲーム名" : (ゲーム実行可能クラス, 人数上限)
}

starter = Starter(tk.Tk(), games)
starter.pack()
starter.mainloop()
