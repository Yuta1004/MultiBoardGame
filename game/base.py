import threading

import tkinter as tk
from tkinter import ttk

from roomlib import Host, Client


class GameBase(tk.Frame):
    """
    MultiBoardGameで動くゲームを実装するためのベースクラス
    実装先でこのクラスを継承し，__init__, setup_widget, update をオーバーライドする

    ## Usage
    import tkinter as tk
    from tkinter import ttk

    class Example(GameBase):

        def __init__(self, master, room_mgr, port_udp):
            super().__init__(master, room_mgr, port_udp, title="Empty", width=700, height=400)

        def setup_widgets(self):
            ttk.Label(self, text="Example").grid(row=0, column=0)
            self.text_viewer = tk.Text(self, width=20, height=10)
            self.text_viewer.grid(row=1, column=0)

        def update(self):
            self.text_viewer.insert("1.0", "Updated\n")
    """

    def __init__(self, master, room_mgr, port_udp, title="Empty", width=600, height=600):
        """
        GameBaseのコンストラクタ

        ## Params
        - master : Tk()
        - room_mgr : roomlib.Host / roomlib.Client
        - port_udp : ルームの招待を送るポート番号
        """
        # Tkinterの初期化
        super().__init__(master)
        self.master.geometry("{}x{}".format(width, height))
        self.master.title(title)
        self.master.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.pack()

        # 通信関連初期化
        self.port_udp = port_udp
        self.room_mgr = room_mgr
        self.room_mgr.set_values()
        self.room_mgr.add_update_notice_func(self.__update)

        # UI初期化
        self.setup_widgets()

        # ユーザ待機処理(Hostとして開始した場合のみ)
        self.waiting_user = False
        if self.is_host():
            wait_user_thread = threading.Thread(target=self.wait_users)
            wait_user_thread.setDaemon(True)
            wait_user_thread.start()

    def is_host(self):
        """
        ホストとしてこのゲームに参加しているかどうかを返す

        ## Returns
        - result : 自分がホストである場合True
        """
        return type(self.room_mgr) is Host

    def wait_users(self):
        """
        ホスト専用処理(ゲーム開始時)
        """
        self.waiting_user = True
        while True:
            while True:
                if self.room_mgr.wait(1.5, self.port_udp):
                    break
            if len(self.room_mgr.user_list)  >= self.room_mgr.users_limit:
                break
        self.waiting_user = False

    def __update(self, _):
        """
        Host/Clientからの更新通知を受け取る
        (1回ここで受け取ってからself.updateを実行する)
        """
        if (not self.is_host()) and (not self.room_mgr.is_alive()):
            self.quit_window()
        self.update()

    def quit_window(self):
        """
        ウィンドウを閉じるときに呼ばれる
        """
        self.room_mgr.quit()
        self.master.destroy()

    ################# ↓継承先でオーバーライドするメソッド↓ #################

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """
        pass

    def update(self):
        """
        部屋の状態が更新された時(=共有変数の更新etc)に呼ばれる
        """

    ################# ↑継承先でオーバーライドするメソッド↑ #################
