import datetime

import tkinter as tk
from tkinter import ttk

from roomlib import Client
from roomlib.net.info import get_host_ipaddresses


class Starter(tk.Frame):

    def __init__(self, master, games):
        """
        Starterのコンストラクタ

        ## Params
        - master : Tk()
        - games : プレイ可能なゲーム一覧 (key: ゲーム名, value: クラス)
        """

        super().__init__(master)
        self.configure(bg="gray92")
        self.master.title("MultiBoardGame Starter")
        self.pack()

        self.setup_widgets()
        self.log("Widget", "Successfuly builded")

        self.games = games;
        self.initialize()
        self.log("Widget", "Successfuly initialized")

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """

        # 部屋フレーム
        frame_room = ttk.LabelFrame(self, text="Room")
        frame_room.grid(row=0, column=0, padx=3, pady=3, stick=tk.W+tk.E+tk.N+tk.S)

        ## 部屋"作成"フレーム
        frame_room_create = ttk.LabelFrame(frame_room, text="Create Room")
        frame_room_create.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W+tk.E+tk.N+tk.S)

        ### 実行可能ゲームのリスト
        ttk.Label(frame_room_create, text="Games").grid(row=0, column=0, padx=5, pady=1, stick=tk.W)
        self.available_game_list = tk.Listbox(frame_room_create, height=7)
        self.available_game_list.grid(row=1, column=0, padx=5, pady=5)

        ### 部屋名入力欄
        ttk.Label(frame_room_create, text="Room Name").grid(row=2, column=0, padx=5, pady=1, stick=tk.W)
        self.entry_room_create = ttk.Entry(frame_room_create)
        self.entry_room_create.insert(0, "aaaaaaaaaaaaa")
        self.entry_room_create.grid(row=3, column=0, padx=5, pady=5)

        ### 部屋作成ボタン
        button_room_create = ttk.Button(frame_room_create)
        button_room_create.configure(text="Create")
        button_room_create.grid(row=4, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ## 部屋"参加"フレーム
        frame_room_join = ttk.LabelFrame(frame_room, text="Join Room")
        frame_room_join.grid(row=0, column=1, padx=8, pady=8, stick=tk.W+tk.E+tk.N+tk.S)

        ### 参加可能な部屋のリスト
        ttk.Label(frame_room_join, text="Available Rooms").grid(row=0, column=0, padx=5, pady=1, stick=tk.W)
        self.available_room_list = tk.Listbox(frame_room_join, height=7)
        self.available_room_list.grid(row=1, column=0, columnspan=1, padx=5, pady=5)

        ### 部屋リスト更新ボタン
        button_room_join = ttk.Button(frame_room_join, command=self.search_rooms)
        button_room_join.configure(text="Update")
        button_room_join.grid(row=2, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ### 部屋入室ボタン
        button_room_update = ttk.Button(frame_room_join, command=self.join_room)
        button_room_update.configure(text="Join")
        button_room_update.grid(row=3, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        # 設定フレーム
        frame_settings = ttk.LabelFrame(self, text="Settings")
        frame_settings.grid(row=0, column=1, padx=3, pady=3, stick=tk.W+tk.E+tk.N+tk.S)

        ## インタフェース表示
        ttk.Label(frame_settings, text="Interfaces").grid(row=0, column=0, padx=5, pady=1, stick=tk.W)
        self.text_interfaces = tk.Text(frame_settings, width=40, height=7)
        self.text_interfaces.configure(state=tk.DISABLED)
        self.text_interfaces.grid(row=1, column=0, padx=5, pady=5)

        ## パスワード入力欄
        ttk.Label(frame_settings, text="Password").grid(row=2, column=0, padx=5, pady=1, stick=tk.W)
        self.entry_password = ttk.Entry(frame_settings)
        self.entry_password.insert(0, "aaaaa")
        self.entry_password.grid(row=3, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ## ポート入力フレーム
        frame_port = ttk.LabelFrame(frame_settings, text="Port")
        frame_port.grid(row=4, column=0, padx=8, pady=8, stick=tk.W+tk.E+tk.N+tk.S)

        ### ポート入力欄(TCP)
        ttk.Label(frame_port, text="TCP: ").grid(row=0, column=0, padx=1, pady=1)
        self.entry_port_tcp = ttk.Entry(frame_port, width=8)
        self.entry_port_tcp.insert(0, 50000)
        self.entry_port_tcp.grid(row=0, column=1, padx=1, pady=1)

        ### ポート入力欄(UDP)
        ttk.Label(frame_port, text="UDP: ").grid(row=0, column=3, padx=1, pady=1)
        self.entry_port_udp = ttk.Entry(frame_port, width=8)
        self.entry_port_udp.insert(0, 50001)
        self.entry_port_udp.grid(row=0, column=4, padx=1, pady=1)

        # ログフレーム
        frame_log = ttk.LabelFrame(self, text="Log")
        frame_log.grid(row=1, column=0, columnspan=2, padx=3, pady=3, stick=tk.W+tk.E+tk.N+tk.S)

        ## ログ表示
        self.text_log = tk.Text(frame_log, width=105, height=10)
        self.text_log.configure(state=tk.DISABLED)
        self.text_log.grid(row=0, column=0, padx=5, pady=5, stick=tk.W+tk.E)

    def initialize(self):
        """
        UIやその他諸々の初期化を行う
        """

        # インタフェース
        addresses = get_host_ipaddresses()
        self.text_interfaces.configure(state=tk.NORMAL)
        for (address, mask) in addresses:
            self.text_interfaces.insert("1.0", "{}/{}\n".format(address, mask))
        self.text_interfaces.configure(state=tk.DISABLED)
        self.log("Interface", "Successfuly loaded")

        # ゲーム
        for game_name in self.games.keys():
            self.available_game_list.insert(tk.END, game_name)
        self.log("Game", "Found {} playable games".format(len(self.games.keys())))

        # roomlib
        self.host = None
        self.client = None
        self.rooms = {}

    def search_rooms(self):
        """
        入室可能な部屋を検索する
        """

        # ポート番号取得
        port_tcp = -1
        port_udp = -1
        try:
            port_tcp = int(self.entry_port_tcp.get())
            port_udp = int(self.entry_port_udp.get())
        except:
            self.log("Room", "Specify the port number as a number")
            return

        # Client初期化(self.client紐付け)
        self.log("Room", "Searching....")
        self.client = Client(port_tcp) if self.client is None else self.client
        orig_rooms = self.client.search(2.0, port_udp)
        self.log("Room", "Found {} rooms".format(len(orig_rooms.keys())))

        # 表示中の部屋情報全削除→更新
        self.available_room_list.delete(0, tk.END)
        for room_id, room_info in orig_rooms.items():
            self.available_room_list.insert(tk.END, room_info[2])
            self.rooms[room_info[2]] = room_id

    def join_room(self):
        """
        現在選択されている部屋に入室を試みる
        """

        # 選択されている部屋のIDを取得
        selected_idx = self.available_room_list.curselection()
        if len(selected_idx) == 0:
            return
        room_id = self.rooms[self.available_room_list.get(selected_idx)]

        # パスワードチェック
        password = self.entry_password.get()
        if len(password) == 0:
            self.log("Room", "Enter your password in the box")
            return

        # 入室申請
        if self.client.join(room_id, password):
            self.log("Room", "Successfuly entered the room")
        else:
            self.log("Room", "Error happened (check password)")

    def log(self, tag, msg):
        """
        ログフレームにログを新しく追加する

        ## Params
        - tag : タグ
        - msg : ログの内容
        """

        view_str = "[{}] [{}] {}\n".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), tag, msg)
        self.text_log.configure(state=tk.NORMAL)
        self.text_log.insert("1.0", view_str)
        self.text_log.configure(state=tk.DISABLED)
