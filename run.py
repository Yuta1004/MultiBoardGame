import tkinter as tk

from launcher import Launcher
from game.example.main import Example

games = {
    "Example": (Example, 2)      # "ゲーム名" : (ゲーム実行可能クラス, 人数上限)
}

launcher = Launcher(tk.Tk(), games)
launcher.pack()
launcher.mainloop()
