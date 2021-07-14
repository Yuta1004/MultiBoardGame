import time
import copy
import random

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance

from game.base import GameBase
from game.koikoi.ui_manager import KoiKoiUIManager

HOST = 0
CLIENT = 1
PH0_WAITING = 0
PH1_SELECT_MY_CARD = 1
PH2_PICK_FROM_DECK = 2
PH3_CALC_SCORE = 3
PH4_ASK_CONTINUE = 4


class KoiKoi(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        # UI周りの初期化処理 (この呼出順を変更しないこと)
        self.load_resources()
        super().__init__(master, room_mgr, port_udp, title="KoiKoi", width=1200, height=700)
        self.ui_manager = KoiKoiUIManager(self.canvas, self.card_clicked_event)
        self.draw()

        # 状態変数初期化
        self.room_mgr.set_values(
            now_playing=False,
            turn=random.randint(0, 1)       # Host=>0, Client=>1
        )
        self.phase = PH0_WAITING

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
        back_card_img = back_card_img.resize((65, 105))
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
        self.canvas.create_text(600, 20, text="", font=("Courier", 30), anchor=tk.CENTER, tags="msg_box")

    def update(self):
        # ゲーム開始処理
        if self.is_host():
            if not self.room_mgr.get_value("now_playing") and len(self.room_mgr.user_list) == 1:
                time.sleep(2)
                cards = [1 << idx for idx in range(48)]
                random.shuffle(cards)
                host_cards = cards[0:8]
                client_cards = cards[8:16]
                on_field_cards = cards[16:24]
                remain_cards = cards[24:]
                self.room_mgr.set_values(now_playing=True, on_field_cards=on_field_cards, host_cards=host_cards, client_cards=client_cards, host_collected_cards=[], client_collected_cards=[], remain_cards=remain_cards)
                self.room_mgr.sync()

        # ターン交代
        if (self.room_mgr.get_value("turn") == HOST and self.is_host()) or (self.room_mgr.get_value("turn") == CLIENT and not self.is_host()):
            if self.phase == PH0_WAITING:
                self.phase = PH1_SELECT_MY_CARD

        # 盤面同期
        self.ui_manager.replace_cards(
            self.room_mgr.get_value("on_field_cards"),
            self.room_mgr.get_value("host_cards" if self.is_host() else "client_cards"),
            self.room_mgr.get_value("client_cards" if self.is_host() else "host_cards"),
            self.room_mgr.get_value("host_collected_cards" if self.is_host() else "client_collected_cards"),
            self.room_mgr.get_value("client_collected_cards" if self.is_host() else "host_collected_cards")
        )
        self.draw()

    def draw(self):
        # メッセージウィンドウ
        msg = ""
        if self.room_mgr.get_value("now_playing"):
            if (self.room_mgr.get_value("turn") == HOST and self.is_host()) or (self.room_mgr.get_value("turn") == CLIENT and not self.is_host()):
                if self.phase == PH1_SELECT_MY_CARD:
                    msg = "Select your card"
                elif self.phase == PH2_PICK_FROM_DECK:
                    msg = "Picked a card from deck"
                elif self.phase == PH3_CALC_SCORE:
                    msg = "Calculated your score"
                elif self.phase == PH4_ASK_CONTINUE:
                    msg = "Choose your action!"
            else:
                msg = "Please wait..."
        else:
            msg = "Player Waiting..."
        self.canvas.itemconfig("msg_box", text=msg)

        # 札
        needs_update = self.ui_manager.draw()
        if needs_update:
            self.after(20, self.draw)

    def card_clicked_event(self, clicked_card_num):
        if self.phase == PH0_WAITING:
            return

        if self.phase == PH1_SELECT_MY_CARD:
            self.phase = PH2_PICK_FROM_DECK

        elif self.phase == PH2_PICK_FROM_DECK:
            self.phase = PH3_CALC_SCORE

        elif self.phase == PH3_CALC_SCORE:
            self.phase = PH4_ASK_CONTINUE

        elif self.phase == PH4_ASK_CONTINUE:
            self.phase = PH0_WAITING
            self.room_mgr.set_values(turn=1-self.room_mgr.get_value("turn"))
            self.room_mgr.sync()

        self.draw()
