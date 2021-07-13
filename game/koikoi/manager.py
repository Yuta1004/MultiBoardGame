from game.koikoi.card.card import Card


class KoiKoiGameManager:
    """
    ゲームの全体的な管理を行う (進行や描画など)
    """

    def __init__(self, canvas):
        """
        KoiKoiGameManagerのコンストラクタ

        ## Params
        - canvas : キャンバス(tkinter)
        """
        self.canvas = canvas
        self.setup_cards()

    def setup_cards(self):
        """
        管理する札(Card)を初期化する
        """
        self.cards = {}
        for card_num in range(48):
            card = Card(card_num, self.canvas)
            card.set_front_visibility(False)
            card.set_highlight_visibility(False)
            self.cards[card_num] = card
            self.canvas.tag_bind("Card"+str(card_num), "<Button-1>", self.card_click_event)

    def draw(self):
        """
        札の描画の更新を行う

        ## Returns
        - needs_udpate : アニメーションが必要な場合True
        """
        needs_more_move = False
        for card in self.cards.values():
            needs_more_move |= card.move()
        return needs_more_move

    def card_click_event(self, event):
        print(event)
