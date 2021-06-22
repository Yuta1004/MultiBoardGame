import random

import tkinter as tk
from tkinter import ttk

from game.base import GameBase


HOST = 0
CLIENT = 1


class Mancala(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        super().__init__(master, room_mgr, port_udp, title="Mancala", width=1100, height=600)

    def setup_widgets(self):
        self.canvas = tk.Canvas(self, width=1100, height=600, bg="white")
        self.canvas.pack()

    def update(self):
        # プレイヤーが揃ったらゲーム開始
        if self.is_host():
            if self.room_mgr.get_value("turn") is None and len(self.room_mgr.user_list) == 1:
                self.room_mgr.set_values(
                    turn=random.randint(0, 1),       ## Host=>0, Client=>1
                    board=[4, 4, 4, 0, 4, 4, 4, 0]     ## ホストの陣地の左端が0
                )
                self.room_mgr.sync()

        self.draw()

    def draw(self):
        """
        主にCanvasの描画を行う
        """
        # 背景
        self.canvas.create_rectangle(0, 0, 1100, 600, fill="white")

        # フィールド
        for i in range(3):
            x = 225 + i*250
            self.canvas.create_rectangle(x, 50, x+150, 50+150, width=5, outline="blue", fill="white")
            self.canvas.create_rectangle(x, 400, x+150, 400+150, width=5, outline="red", fill="white", activewidth=10)
        self.canvas.create_rectangle(40, 225, 50+150, 225+150, width=3, fill="white", dash=(10, 10))
        self.canvas.create_rectangle(910, 225, 910+150, 225+150, width=3, fill="white", dash=(10, 10))

        # 指示内容決定
        msg = ""
        if (self.is_host() and self.room_mgr.get_value("turn") == HOST) or (not self.is_host() and self.room_mgr.get_value("turn") == CLIENT):
            msg = "Your turn"
        elif self.room_mgr.get_value("turn") is None:
            msg = "Waiting players..."
        else:
            msg =  "Thinking..."

        # 指示位置
        self.canvas.create_line(250, 330, 850, 330)
        self.canvas.create_text(550, 300, text=msg, font=("Menlo", 40))
