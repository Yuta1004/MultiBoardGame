import time
import random

import tkinter as tk
from tkinter import ttk

from game.base import GameBase
from game.mancala.dot import Dot


HOST = 0
CLIENT = 1


class Mancala(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        super().__init__(master, room_mgr, port_udp, title="Mancala", width=1100, height=600)

        # 状態変数初期化
        self.room_mgr.set_values(
            now_gaming=False,
            turn=random.randint(0, 1),       ## Host=>0, Client=>1
            board=[4, 4, 4, 0, 4, 4, 4, 0]     ## ホストの陣地の左端が0
        )
        self.pos_diff = 0 if self.is_host() else 4

        # Dot準備
        self.dots = []
        for i in range(3):
            for j in range(4):
                self.dots.append(Dot(i))
                self.dots.append(Dot(i+4))

        self.draw()

    def setup_widgets(self):
        self.canvas = tk.Canvas(self, width=1100, height=600, bg="white")
        self.canvas.tag_bind("myland", "<Button-1>", self.myland_clicked)
        self.canvas.pack()

    def update(self):
        # プレイヤーが揃ったらゲーム開始
        if self.is_host():
            if not self.room_mgr.get_value("now_gaming") and len(self.room_mgr.user_list) == 1:
                time.sleep(2)
                self.room_mgr.set_values(now_gaming=True)
                self.room_mgr.sync()

        self.draw()

    def draw(self):
        """
        主にCanvasの描画を行う
        """
        # 背景
        self.canvas.create_rectangle(0, 0, 1100, 600, fill="white")

        # フィールド
        my_color = ["red", "blue"][self.pos_diff%3]
        oppo_color = ["blue", "red"][self.pos_diff%3]
        for i in range(3):
            x = 225 + i*250
            self.canvas.create_rectangle(x, 50, x+150, 50+150, width=5, outline=oppo_color, fill="white")
            self.canvas.create_rectangle(x, 400, x+150, 400+150, width=5, outline=my_color, fill="white", activewidth=10, tags="myland")
        self.canvas.create_rectangle(40, 225, 50+150, 225+150, width=3, fill="white", dash=(10, 10))
        self.canvas.create_rectangle(910, 225, 910+150, 225+150, width=3, fill="white", dash=(10, 10))

        # 指示内容決定
        msg = ""
        if not self.room_mgr.get_value("now_gaming"):
            msg = "Waiting players..."
        elif (self.is_host() and self.room_mgr.get_value("turn") == HOST) or (not self.is_host() and self.room_mgr.get_value("turn") == CLIENT):
            msg = "Your turn"
        else:
            msg =  "Thinking..."

        # 指示位置
        self.canvas.create_line(250, 330, 850, 330)
        self.canvas.create_text(550, 300, text=msg, font=("Menlo", 40))

        # Dot描画
        needs_update = True
        for dot in self.dots:
            dot.draw(self.canvas)
            needs_update &= dot.needs_update()

    def myland_clicked(self, event):
        """
        自陣地がクリックされたとき呼ばれる
        """
        clicked_land_pos = int((event.x-225)/250) +self.pos_diff
