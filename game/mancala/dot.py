import random

import tkinter as tk
from tkinter import ttk


RADIUS = 15


class Dot:

    def __init__(self, pos):
        """
        Dotのコンストラクタ

        ## Params
        - pos : Dotの配置場所
        """
        self.pos = pos
        (self.nx, self.ny) = self.calc_abs_pos()
        self.change_pos(pos)

    def change_pos(self, pos):
        """
        Dot位置の更新を行う

        ## Params
        - pos : Dotの配置場所
        """
        self.pos = pos
        (self.x, self.y) = self.calc_abs_pos()
        (self.rx, self.ry) = (random.randint(RADIUS+20, 150-RADIUS-20), random.randint(RADIUS+20, 150-RADIUS-20))
        (self.dx, self.dy) = ((self.x-self.nx)/50, (self.y-self.ny)/50)

    def draw(self, canvas):
        """
        Dotの描画を行う

        ## Params
        - canvas : 描画対象Canvas
        """
        x = self.nx + self.rx; y = self.ny + self.ry
        canvas.create_oval(x, y, x+RADIUS*2, y+RADIUS*2, fill="brown", width=4, outline="black")
        if self.needs_update():
            self.nx += self.dx
            self.ny += self.dy

    def needs_update(self):
        """
        まだ描画し続ける必要があるかどうかを返す (アニメーション用)
        """
        return abs(self.x-self.nx) > 1 or abs(self.y-self.ny) > 1

    def calc_abs_pos(self):
        """
        Dotの配置場所からCanvas上の座標を求める
        """
        if 0 <= self.pos <= 2:
            return (225 + self.pos*250, 400)
        elif 4 <= self.pos <= 6:
            return (725 - (self.pos-4)*250, 50)
        elif self.pos == 3:
            return (910, 225)
        elif self.pos == 7:
            return (40, 225)
