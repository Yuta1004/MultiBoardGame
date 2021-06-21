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

        self.master.geometry("800x500")
        self.master.title("MultiBoardGame Starter")
        self.setup_widgets()

    def setup_widgets(self):
        """
        表示するウィジェットの配置/設定を行う
        """

        # 部屋フレーム

        ## 部屋"作成"フレーム
        self.frame_room_create = ttk.LabelFrame(self, text="Create Room")
        self.frame_room_create.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)

        ### 実行可能ゲームのリスト
        self.available_game_list = tk.Listbox(self.frame_room_create, height=5)
        self.available_game_list.insert(tk.END, "Game A")
        self.available_game_list.insert(tk.END, "Game B")
        self.available_game_list.insert(tk.END, "Game C")
        self.available_game_list.insert(tk.END, "Game D")
        self.available_game_list.select_set(0)
        self.available_game_list.grid(row=0, column=0)

        ### 部屋名入力欄
        self.entry_room_create = ttk.Entry(self.frame_room_create)
        self.entry_room_create.insert(0, "部屋名")
        self.entry_room_create.grid(row=1, column=0)

        ### 部屋作成ボタン
        self.button_room_create = ttk.Button(self.frame_room_create)
        self.button_room_create.configure(text="Create")
        self.button_room_create.grid(row=2, column=0)

        ## 部屋"参加"フレーム
        self.frame_room_join = ttk.LabelFrame(self, text="Join Room")
        self.frame_room_join.grid(row=0, column=0, padx=5, pady=5, stick=tk.W+tk.E)

        ### 参加可能な部屋のリスト
        self.available_room_list = tk.Listbox(self.frame_room_join, height=6)
        self.available_room_list.insert(tk.END, "おへや1 (こいこい)")
        self.available_room_list.insert(tk.END, "おへや2 (7並べ)")
        self.available_room_list.insert(tk.END, "おへや3 (ババ抜き)")
        self.available_room_list.select_set(0)
        self.available_room_list.grid(row=0, column=0, columnspan=2)

        ### 部屋参加ボタン
        self.button_room_join = ttk.Button(self.frame_room_join)
        self.button_room_join.configure(text="Join")
        self.button_room_join.grid(row=1, column=0)

        ### 部屋リスト更新ボタン
        self.button_room_update = ttk.Button(self.frame_room_join)
        self.button_room_update.configure(text="Update")
        self.button_room_update.grid(row=1, column=1)

        # 設定フレーム

        # ログフレーム

