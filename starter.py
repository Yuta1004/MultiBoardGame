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
        self.pack()

        self.master.title("MultiBoardGame Starter")
        self.setup_widgets()

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """

        # 部屋フレーム
        self.frame_room = ttk.LabelFrame(self, text="Room")
        self.frame_room.grid(row=0, column=0, padx=10, pady=10, stick=tk.W+tk.E+tk.N+tk.S)

        ## 部屋"作成"フレーム
        self.frame_room_create = ttk.LabelFrame(self.frame_room, text="Create Room")
        self.frame_room_create.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W+tk.E+tk.N+tk.S)

        ### 実行可能ゲームのリスト
        self.available_game_list = tk.Listbox(self.frame_room_create, height=7)
        self.available_game_list.insert(tk.END, "Game A")
        self.available_game_list.insert(tk.END, "Game B")
        self.available_game_list.insert(tk.END, "Game C")
        self.available_game_list.insert(tk.END, "Game D")
        self.available_game_list.select_set(0)
        self.available_game_list.grid(row=0, column=0, padx=5, pady=5)

        ### 部屋名入力欄
        self.entry_room_create = ttk.Entry(self.frame_room_create)
        self.entry_room_create.insert(0, "RoomName")
        self.entry_room_create.grid(row=1, column=0, padx=5, pady=5)

        ### 部屋作成ボタン
        self.button_room_create = ttk.Button(self.frame_room_create)
        self.button_room_create.configure(text="Create")
        self.button_room_create.grid(row=2, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ## 部屋"参加"フレーム
        self.frame_room_join = ttk.LabelFrame(self.frame_room, text="Join Room")
        self.frame_room_join.grid(row=0, column=1, padx=8, pady=8, stick=tk.W+tk.E+tk.N+tk.S)

        ### 参加可能な部屋のリスト
        self.available_room_list = tk.Listbox(self.frame_room_join, height=7)
        self.available_room_list.insert(tk.END, "Room1 (KoiKoi)")
        self.available_room_list.insert(tk.END, "Room2 (Sevens)")
        self.available_room_list.insert(tk.END, "Room3 (Old Maid)")
        self.available_room_list.select_set(0)
        self.available_room_list.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        ### 部屋参加ボタン
        self.button_room_join = ttk.Button(self.frame_room_join)
        self.button_room_join.configure(text="Update")
        self.button_room_join.grid(row=1, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ### 部屋リスト更新ボタン
        self.button_room_update = ttk.Button(self.frame_room_join)
        self.button_room_update.configure(text="Join")
        self.button_room_update.grid(row=2, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        # 設定フレーム
        self.frame_settings = ttk.LabelFrame(self, text="Settings")
        self.frame_settings.grid(row=0, column=1, padx=10, pady=10, stick=tk.W+tk.E+tk.N+tk.S)

        ## インタフェース表示
        self.label_interfaces = ttk.Label(self.frame_settings, text="Interfaces")
        self.label_interfaces.grid(row=0, column=0, padx=5, pady=1, stick=tk.W)
        self.text_interfaces = tk.Text(self.frame_settings, width=40, height=5)
        self.text_interfaces.insert("1.0", "xxx.xxx.xxx.xxx / xxx.xxx.xxx.xxx\n"*4)
        self.text_interfaces.configure(state=tk.DISABLED)
        self.text_interfaces.grid(row=1, column=0, padx=5, pady=5)

        ## パスワード入力欄
        self.label_password = ttk.Label(self.frame_settings, text="Password")
        self.label_password.grid(row=2, column=0, padx=5, pady=1, stick=tk.W)
        self.entry_password = ttk.Entry(self.frame_settings)
        self.entry_password.insert(0, "aaaaa")
        self.entry_password.grid(row=3, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ## ポート入力フレーム
        self.frame_port = ttk.LabelFrame(self.frame_settings, text="Port")
        self.frame_port.grid(row=4, column=0, padx=8, pady=8, stick=tk.W+tk.E+tk.N+tk.S)

        ### ポート入力欄(TCP)
        self.label_port_tcp = ttk.Label(self.frame_port, text="TCP: ")
        self.label_port_tcp.grid(row=0, column=0, padx=1, pady=1)
        self.entry_port_tcp = ttk.Entry(self.frame_port, width=8)
        self.entry_port_tcp.insert(0, 50000)
        self.entry_port_tcp.grid(row=0, column=1, padx=1, pady=1)

        ### ポート入力欄(UDP)
        self.label_port_udp = ttk.Label(self.frame_port, text="UDP: ")
        self.label_port_udp.grid(row=0, column=3, padx=1, pady=1)
        self.entry_port_udp = ttk.Entry(self.frame_port, width=8)
        self.entry_port_udp.insert(0, 50001)
        self.entry_port_udp.grid(row=0, column=4, padx=1, pady=1)

        # ログフレーム

