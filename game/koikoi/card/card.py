import tkinter as tk
from PIL import Image, ImageTk


class Card:
    """
    カード1枚の情報をもつクラス

    ## カード情報の表し方
    - 48ビットを用いて表す
    - 最下位ビットからの距離を用いて以下のようにカードの種類を定義する
        - 0 ~ 9 : タン (10)
        - 4 ~ 6 : 赤短 (3)
        - 7 ~ 9 : 青短 (3)
        - 15 ~ 15 : 盃 (1)
        - 10 ~ 18 : タネ (9)
        - 16 ~ 18 : 猪鹿蝶 (3)
        - 19 ~ 19 : 桜 (1)
        - 20 ~ 20 : 月 (1)
        - 19 ~ 21 : 三光 (3)
        - 19 ~ 22 : 四光 (4)
        - 23 ~ 23 : 雨 (1)
        - 19 ~ 23 : 五光 (5)
        - 24 ~ 47 : カス (24)
    - 月
        - 1月 : 21, 4, 24, 25
        - 2月 : 10, 5, 26, 27
        - 3月 : 19, 6, 28, 29
        - 4月 : 11, 0, 30, 31
        - 5月 : 12, 1, 32, 33
        - 6月 : 16, 7, 34, 35
        - 7月 : 17, 2, 36, 37
        - 8月 : 20, 13, 38, 39
        - 9月 : 15, 8, 40, 41
        - 10月 : 18, 9, 42, 43
        - 11月 : 23, 14, 3, 44
        - 12月 : 22, 45 46, 47
        47                                                                                                0
        |000000000000000000000000|00000|000|00000|000|000|0000|
        |                   カス                      |20点札|    10点札   |       5点札       |
    """

    def __init__(self, card_num, canvas, init_x, init_y):
        """
        Cardのコンストラクタ

        ## Params
        - card_num : カード番号 (詳細はCardクラスのdocstring)
        - canvas : キャンバス (Tkinter)
        - init_x : 初期座標 (x成分)
        - init_y : 初期座標 (y成分)
        """
        self.card_num = card_num

        self.canvas = canvas
        (self.x, self.y) = (init_x, init_y)
        (self.nx, self.ny) = (self.x, self.y)
        (self.dx, self.dy) = (0, 0)

        self.load_resources()
        self.setup_canvas()

    def load_resources(self):
        # 札画像(表)
        card_img = Image.open(open("game/koikoi/resource/card/{}.png".format(self.card_num), "rb"))
        card_img = card_img.resize((65, 105))
        self.card_img = ImageTk.PhotoImage(card_img)

        # 札画像(裏)
        card_back_img = Image.open(open("game/koikoi/resource/card/back.png", "rb"))
        card_back_img = card_back_img.resize((65, 105))
        self.card_back_img = ImageTk.PhotoImage(card_back_img)

        # ハイライト画像
        highlight_img = Image.open(open("game/koikoi/resource/card/highlight.png", "rb"))
        highlight_img = highlight_img.resize((75, 115))
        self.highlight_img = ImageTk.PhotoImage(highlight_img)

    def setup_canvas(self):
        """
        キャンバスへの描画準備を行う

        ## Params
        - canvas : キャンバス (Tkinter)
        """
        base_tag = "Card"+str(self.card_num)
        self.canvas.create_image(self.nx, self.ny, image=self.highlight_img, anchor=tk.CENTER, tags=(base_tag, base_tag+"highlight"))
        self.canvas.create_image(self.nx, self.ny, image=self.card_img, anchor=tk.CENTER, tags=(base_tag))
        self.canvas.create_image(self.nx, self.ny, image=self.card_back_img, anchor=tk.CENTER, tags=(base_tag, base_tag+"back"))

    def move(self):
        """
        札の再描画(=アニメーション)を行う

        ## Params
        - canvas : キャンバス(Tkinter)

        ## Return
        - needs_more_move : まだ再描画を続ける必要がある場合はTrue
        """
        if abs(self.nx-self.x) > 0.1 or abs(self.ny-self.y) > 0.1:
            self.nx += self.dx
            self.ny += self.dy
            self.canvas.move("Card"+str(self.card_num), self.dx, self.dy)
            return True
        return False

    def update_pos(self, x, y):
        """
        札の位置を更新する

        ## Params
        - x : 更新後の位置 (x成分)
        - y : 更新後の位置 (y成分)
        """
        self.x = x
        self.y = y
        self.dx = (self.x - self.nx) / 30
        self.dy = (self.y - self.ny) / 30

    def get_pos(self):
        """
        現在表示されている位置を返す

        ## Returns
        - (x, y) : 座標のx成分とy成分のタプル
        """
        return (self.x, self.y)

    def set_front_visibility(self, visibility=True):
        """
        札の表を表示するかどうかを制御する

        ## Params
        - visibility : 表を表示する場合True
        """
        self.canvas.itemconfigure("Card"+str(self.card_num)+"back", state=tk.HIDDEN if visibility else tk.NORMAL)

    def set_highlight_visibility(self, visibility=True):
        """
        札のハイライト効果を表示するかを制御する

        ## Params
        - visibility : ハイライト効果を表示する場合True
        """
        self.canvas.itemconfigure("Card"+str(self.card_num)+"highlight", state=tk.NORMAL if visibility else tk.HIDDEN)
