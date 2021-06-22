import tkinter as tk

from launcher import Launcher
from game.example.main import Example
from game.mancala.main import Mancala

games = {
    # "Example": (Example, 2)      # "ゲーム名" : (ゲーム実行可能クラス, 人数上限)
    "Mancala": (Mancala, 2)
}

launcher = Launcher(tk.Tk(), games)
launcher.pack()
launcher.mainloop()
