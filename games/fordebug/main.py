import threading

import tkinter as tk
from tkinter import ttk

from roomlib import Host, Client


class ForDebugGame(tk.Frame):

    def __init__(self, master, room_mgr, port_udp):
        """
        ForDebugGameのコンストラクタ

        ## Params
        - master : Tk()
        - room_mgr : roomlib.Host / roomlib.Client
        - port_udp : ルームの招待を送るポート番号
        """

        super().__init__(master)
        self.master.geometry("400x400")
        self.master.title("For Debug Game")
        self.master.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.pack()

        self.port_udp = port_udp
        self.room_mgr = room_mgr
        self.room_mgr.set_values(red="", green="", blue="")
        self.room_mgr.add_update_notice_func(self.draw)

        self.setup_widgets()
        self.draw(None)

        if type(self.room_mgr) is Host:
            threading.Thread(target=self.host_process).start()

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """

        # キャンバス
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(fill=tk.BOTH)

        # 色入力欄 (左)
        self.entry_left = ttk.Entry(self, width=8)
        self.entry_left.place(x=60, y=120)

        # 色入力欄 (中央)
        self.entry_center = ttk.Entry(self, width=8)
        self.entry_center.place(x=160, y=120)

        # 色入力欄 (右)
        self.entry_right = ttk.Entry(self, width=8)
        self.entry_right.place(x=260, y=120)

        # 送信ボタン
        self.button_send = ttk.Button(self, text="Send", width=18, command=self.button_pressed)
        self.button_send.place(x=100, y=250)

    def host_process(self):
        """
        ホスト専用処理(ゲーム開始時)
        """

        while True:
            if self.room_mgr.wait(1.5, self.port_udp):
                break

    def draw(self, room_mgr):
        """
        キャンバスの更新を行う
        """

        # 図形
        self.canvas.create_rectangle(60, 150, 140, 230, fill="red")
        self.canvas.create_rectangle(160, 150, 240, 230, fill="green")
        self.canvas.create_rectangle(260, 150, 340, 230, fill="blue")

        # UIウィジェット
        self.entry_left.delete(0, tk.END)
        self.entry_center.delete(0, tk.END)
        self.entry_right.delete(0, tk.END)
        self.entry_left.insert(0, self.room_mgr.get_value("red"))
        self.entry_center.insert(0, self.room_mgr.get_value("green"))
        self.entry_right.insert(0, self.room_mgr.get_value("blue"))

    def button_pressed(self):
        """
        送信ボタンが押されたときに呼ばれる
        """

        self.room_mgr.set_values(
            red=self.entry_left.get(),
            green=self.entry_center.get(),
            blue=self.entry_right.get()
        )
        self.room_mgr.sync()

    def quit_window(self):
        """
        ウィンドウを閉じるときに呼ばれる
        """

        self.room_mgr.quit()
        self.master.destroy()
