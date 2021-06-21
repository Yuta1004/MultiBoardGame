import tkinter as tk
from tkinter import ttk


class Starter(tk.Frame):

    def __init__(self, master):
        """
        Starterのコンストラクタ

        ## Params
        - master : Tk()
        """

        super().__init__(master)
        self.configure(bg="gray92")
        self.pack()

        self.master.title("MultiBoardGame Starter")
        self.setup_widgets()

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
        self.available_game_list = tk.Listbox(frame_room_create, height=7)
        self.available_game_list.insert(tk.END, "Game A")
        self.available_game_list.insert(tk.END, "Game B")
        self.available_game_list.insert(tk.END, "Game C")
        self.available_game_list.insert(tk.END, "Game D")
        self.available_game_list.select_set(0)
        self.available_game_list.grid(row=0, column=0, padx=5, pady=5)

        ### 部屋名入力欄
        self.entry_room_create = ttk.Entry(frame_room_create)
        self.entry_room_create.insert(0, "RoomName")
        self.entry_room_create.grid(row=1, column=0, padx=5, pady=5)

        ### 部屋作成ボタン
        button_room_create = ttk.Button(frame_room_create)
        button_room_create.configure(text="Create")
        button_room_create.grid(row=2, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ## 部屋"参加"フレーム
        frame_room_join = ttk.LabelFrame(frame_room, text="Join Room")
        frame_room_join.grid(row=0, column=1, padx=8, pady=8, stick=tk.W+tk.E+tk.N+tk.S)

        ### 参加可能な部屋のリスト
        self.available_room_list = tk.Listbox(frame_room_join, height=7)
        self.available_room_list.insert(tk.END, "Room1 (KoiKoi)")
        self.available_room_list.insert(tk.END, "Room2 (Sevens)")
        self.available_room_list.insert(tk.END, "Room3 (Old Maid)")
        self.available_room_list.select_set(0)
        self.available_room_list.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        ### 部屋参加ボタン
        button_room_join = ttk.Button(frame_room_join)
        button_room_join.configure(text="Update")
        button_room_join.grid(row=1, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ### 部屋リスト更新ボタン
        button_room_update = ttk.Button(frame_room_join)
        button_room_update.configure(text="Join")
        button_room_update.grid(row=2, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        # 設定フレーム
        frame_settings = ttk.LabelFrame(self, text="Settings")
        frame_settings.grid(row=0, column=1, padx=3, pady=3, stick=tk.W+tk.E+tk.N+tk.S)

        ## インタフェース表示
        ttk.Label(frame_settings, text="Interfaces").grid(row=0, column=0, padx=5, pady=1, stick=tk.W)
        self.text_interfaces = tk.Text(frame_settings, width=40, height=5)
        self.text_interfaces.insert("1.0", "xxx.xxx.xxx.xxx / xxx.xxx.xxx.xxx\n"*4)
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
        self.text_log.insert("1.0", "[xxxx/xx/xx xx:xx:xx] aaaaaaaaaaaaaaaaaaaaaa\n"*7)
        self.text_log.configure(state=tk.DISABLED)
        self.text_log.grid(row=0, column=0, padx=5, pady=5, stick=tk.W+tk.E)
