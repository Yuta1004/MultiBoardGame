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

    def __init__(self, card_num):
        """
        Cardのコンストラクタ

        ## Params
        - card_num : カード番号 (詳細はCardクラスのdocstring)

        ## Warning
        - 0未満または47を超える番号を指定した場合は47番で初期化される
        """
        if card_num < 0 or 47 < card_num:
            card_num = 47
        self.card_num = 0
        self.card_num |= (1 << card_num)

        (self.x, self.y) = (0, 0)
        (self.nx, self.ny) = (0, 0)
        (self.dx, self.dy) = (0, 0)
        self.show_front = False

        self.load_resources()

    def load_resources(self):
        # 札画像(表)
        card_img = Image.open(open("game/koikoi/resource/card/{}.png".format(1<<self.card_num), "rb"))
        card_img = card_img.resize((90, 120))
        self.card_img = ImageTk.PhotoImage(card_img)

        # 札画像(裏)
        card_back_img = Image.open(open("game/koikoi/resource/card/back.png", "rb"))
        card_back_img = card_back_img.resize((90, 120))
        self.card_back_img = ImageTk.PhotoImage(card_back_img)

        # ハイライト画像
        highlight_img = Image.open(open("game/koikoi/resource/card/highlight.png", "rb"))
        highlight_img = highlight_img.resize((100, 130))
        self.highlight_img = ImageTk.PhotoImage(highlight_img)

    def draw(self, canvas):
        """
        札を描画する

        ## Params
        - canvas : キャンバス(Tkinter)
        """
        canvas.create_image(self.nx, self.ny, image=self.highlight_img, anchor=tk.CENTER)
        canvas.create_image(self.nx, self.ny, image=self.card_img, anchor=tk.CENTER)
        if not self.show_front:
            canvas.create_image(self.nx, self.ny, image=self.card_back_img, anchor=tk.CENTER)
