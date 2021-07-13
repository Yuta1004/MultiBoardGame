import random

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance

from game.base import GameBase
from game.koikoi.manager import KoiKoiGameManager


class KoiKoi(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        # 描画関連初期化 (メソッド呼び出しの順番を変えないこと)
        self.msg = "Waiting..."
        self.load_resources()
        super().__init__(master, room_mgr, port_udp, title="KoiKoi", width=1200, height=700)
        self.game_manager = KoiKoiGameManager(self.canvas)
        self.draw()

    def load_resources(self):
        # 背景
        bg_img = Image.open(open("game/koikoi/resource/bg.png", "rb"))
        bg_img = bg_img.resize((1200, 700))
        bg_img = ImageEnhance.Brightness(bg_img).enhance(0.7)
        self.bg_img = ImageTk.PhotoImage(bg_img)

        # 合い札置き場
        aihuda_img = Image.open(open("game/koikoi/resource/aihuda.png", "rb"))
        aihuda_img = aihuda_img.resize((280, 700))
        self.aihuda_img = ImageTk.PhotoImage(aihuda_img)

        # 札(裏)
        back_card_img = Image.open(open("game/koikoi/resource/card/back.png", "rb"))
        back_card_img = back_card_img.resize((90, 120))
        self.back_card_img = ImageTk.PhotoImage(back_card_img)

        # メッセージボックス
        msg_box_img = Image.open(open("game/koikoi/resource/message.png", "rb"))
        msg_box_img = msg_box_img.resize((640, 40))
        self.msg_box_img = ImageTk.PhotoImage(msg_box_img)

    def setup_widgets(self):
        # キャンバス初期化
        self.canvas = tk.Canvas(self, width=1200, height=700, bg="white")
        self.canvas.pack()

        # 背景画像
        self.canvas.create_image(0, 0, image=self.bg_img, anchor=tk.NW)

        # 合い札置き場
        self.canvas.create_image(0, 0, image=self.aihuda_img, anchor=tk.NW)
        self.canvas.create_image(920, 0, image=self.aihuda_img, anchor=tk.NW)
        self.canvas.create_line(0, 400, 280, 400, width=3, fill="black")
        self.canvas.create_line(920, 300, 1200, 300, width=3, fill="black")

        # 山札
        self.canvas.create_image(350, 350, image=self.back_card_img, anchor=tk.CENTER)

        # メッセージウィンドウ
        self.canvas.create_image(280, 0, image=self.msg_box_img, anchor=tk.NW)
        self.canvas.create_text(600, 20, text=self.msg, font=("Courier", 30), anchor=tk.CENTER)

    def update(self):
        pass

    def draw(self):
        needs_update = self.game_manager.draw()
        if needs_update:
            self.after(20, self.draw)
