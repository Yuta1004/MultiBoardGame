import copy
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
            winner=-1,
            now_gaming=False,
            turn=random.randint(0, 1),       ## Host=>0, Client=>1
            board=[4, 4, 4, 0, 4, 4, 4, 0]      ## ホストの陣地の左端が0
        )
        self.pos_diff = 0 if self.is_host() else 4
        self.now_viewing_board = [4, 4, 4, 0, 4, 4, 4, 0]

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

        # Dotアニメーションの準備
        board = copy.deepcopy(self.room_mgr.get_value("board"))
        recent_selected_pos = -1
        for idx in range(8):
            if self.now_viewing_board[idx] > board[idx]:
                recent_selected_pos = idx
                break
        if recent_selected_pos != -1:
            moving_target_nums = self.now_viewing_board[recent_selected_pos]
            for dot in self.dots:
                if dot.pos == (recent_selected_pos+self.pos_diff)%8:
                    dot.change_pos((recent_selected_pos+self.pos_diff+moving_target_nums)%8)
                    moving_target_nums -= 1
            self.now_viewing_board = board

        # 勝敗が決まっている場合操作を不能にする
        if self.room_mgr.get_value("winner") != -1:
            self.canvas.tag_unbind("myland", "<Button-1>")

        self.draw()

    def draw(self):
        """
        主にCanvasの描画を行う
        """
        # 背景
        self.canvas.delete(tk.ALL)

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
        if (self.is_host() and self.room_mgr.get_value("winner") == HOST) or (not self.is_host() and self.room_mgr.get_value("winner") == CLIENT):
            msg = "You WIN!"
        elif self.room_mgr.get_value("winner") != -1:
            msg = "You LOSE..."

        # 指示位置
        self.canvas.create_line(250, 330, 850, 330)
        self.canvas.create_text(550, 300, text=msg, font=("Menlo", 40))

        # Dot描画
        needs_update = False
        for dot in self.dots:
            dot.draw(self.canvas)
            needs_update |= dot.needs_update()

        # アニメーション続行判定
        if needs_update:
            self.after(20, self.draw)

    def myland_clicked(self, event):
        """
        自陣地がクリックされたとき呼ばれる
        """
        board = copy.deepcopy(self.room_mgr.get_value("board"))

        # 駒の有無など，妥当性検証
        clicked_land_pos = int((event.x-225)/250)
        if clicked_land_pos > 2:
            return
        clicked_land_pos = (clicked_land_pos+self.pos_diff) % 8
        dot_nums = board[clicked_land_pos]
        if dot_nums <= 0:
            return
        if not (self.is_host() and self.room_mgr.get_value("turn") == HOST) and not (not self.is_host() and self.room_mgr.get_value("turn") == CLIENT):
            return

        # 駒の移動
        board[clicked_land_pos] = 0
        for _ in range(dot_nums):
            clicked_land_pos  = (clicked_land_pos+1) % 8
            board[clicked_land_pos] += 1

        if board[self.pos_diff] + board[self.pos_diff+1] + board[self.pos_diff+2] == 0:
            self.room_mgr.set_values(winner=(HOST if self.is_host() else CLIENT))

        # ターン進行
        self.room_mgr.set_values(
            turn=(self.room_mgr.get_value("turn")+1)%2,
            board=board
        )
        self.room_mgr.sync()
