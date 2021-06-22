import threading

import tkinter as tk
from tkinter import ttk

from roomlib import Host, Client


class Template(tk.Frame):

    def __init__(self, master, room_mgr, port_udp):
        """
        コンストラクタ

        ## Params
        - master : Tk()
        - room_mgr : roomlib.Host / roomlib.Client
        - port_udp : ルームの招待を送るポート番号
        """
        # Tkinterの初期化
        super().__init__(master)
        self.master.geometry("600x600")
        self.master.title("Mancala")
        self.master.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.pack()

        # 通信関連初期化
        self.port_udp = port_udp
        self.room_mgr = room_mgr
        self.room_mgr.set_values()
        self.room_mgr.add_update_notice_func(self.draw)

        # UI初期化
        self.setup_widgets()
        self.update(None)

        # ユーザ待機処理(Hostとして開始した場合のみ)
        self.waiting_user = False
        if type(self.room_mgr) is Host:
            threading.Thread(target=self.host_process).start()

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """
        pass

    def host_process(self):
        """
        ホスト専用処理(ゲーム開始時)
        """
        self.waiting_user = True
        while True:
            while True:
                if self.room_mgr.wait(1.5, self.port_udp):
                    break
            if len(self.room_mgr.user_list)  >= self.users_limit:
                break
        self.waiting_user = False

    def update(self, _):
        """
        更新処理を行う
        ※変数更新時に呼ばれる
        """
        pass

    def draw(self):
        """
        Canvas/Widgetの描画および更新を行う
        """
        pass

    def quit_window(self):
        """
        ウィンドウを閉じるときに呼ばれる
        """
        self.room_mgr.quit()
        self.master.destroy()
