import tkinter as tk
from tkinter import ttk

from game.base import GameBase


class KoiKoi(GameBase):

    def __init__(self, master, room_mgr, port_udp):
        super().__init__(master, room_mgr, port_udp, title="KoiKoi", width=700, height=400)

    def setup_widgets(self):
        ttk.Label(self, text="KoiKoi").grid(row=0, column=0)

    def update(self):
        pass
