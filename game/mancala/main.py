import tkinter as tk
from tkinter import ttk

from game.base import GameBase


class Mancala(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        super().__init__(master, room_mgr, port_udp, title="Mancala", width=1100, height=600)

    def setup_widgets(self):
        self.canvas = tk.Canvas(self, width=1100, height=600, bg="white")
        self.canvas.pack()

    def update(self):
        self.draw()

    def draw(self):
        """
        主にCanvasの描画を行う
        """
        # フィールド
        for i in range(3):
            x = 225 + i*250
            self.canvas.create_rectangle(x, 50, x+150, 50+150, width=5, outline="blue", fill="white")
            self.canvas.create_rectangle(x, 400, x+150, 400+150, width=5, outline="red", fill="white", activewidth=10)
        self.canvas.create_rectangle(40, 225, 50+150, 225+150, width=3, fill="white", dash=(10, 10))
        self.canvas.create_rectangle(910, 225, 910+150, 225+150, width=3, fill="white", dash=(10, 10))

        # 指示位置
        self.canvas.create_line(250, 330, 850, 330)
        self.canvas.create_text(550, 300, text="Waiting players...", font=("Menlo", 40), tag="msg_box")
