import tkinter as tk
from tkinter import ttk

from game.base import GameBase


class Example(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        super().__init__(master, room_mgr, port_udp, title="Empty", width=700, height=400)

    def setup_widgets(self):
        ttk.Label(self, text="Example").grid(row=0, column=0)
        self.text_viewer = tk.Text(self, width=20, height=10)
        self.text_viewer.grid(row=1, column=0)

    def update(self):
        self.text_viewer.insert("1.0", "Updated\n")
