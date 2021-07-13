from game.koikoi.card.card import Card


class KoiKoiUIManager:
    """
    ゲームUIの管理を行う (主に札の描画)
    """

    def __init__(self, canvas):
        """
        KoiKoiUIManagerのコンストラクタ

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
            card = Card(1 << card_num, self.canvas, 350, 350)
            card.set_front_visibility(False)
            card.set_highlight_visibility(False)
            self.cards[1 << card_num] = card
            self.canvas.tag_bind("Card"+str(card_num), "<Button-1>", self.card_click_event)

    def replace_cards(self, on_field_cards, my_cards, oppo_cards, my_collected_cards, oppo_collected_cards):
        """
        札の再配置を行う

        ## Params
        - canvas : キャンバス(tkinter)
        - on_field_cards : 場札のリスト
        - my_cards : 自分が所持している札のリスト
        - oppo_cards : 相手が所持している札のリスト
        - my_collected_cards : 自分が所持している合札のリスト
        - oppo_collected_cards : 相手が所持している合札のリスト
        """
        # 場札
        h_size = (len(on_field_cards)+1) // 2
        for idx, card_num in enumerate(on_field_cards):
            self.cards[card_num].set_front_visibility(True)
            self.cards[card_num].update_pos(470+(idx%h_size)*70, 350+(-1 if idx//h_size == 0 else 1)*60)

        # 自分の持札
        for idx, (my_card_num, oppo_card_num) in enumerate(zip(my_cards, oppo_cards)):
            self.cards[my_card_num].set_front_visibility(True)
            self.cards[my_card_num].update_pos(320+idx*80, 600)
            self.cards[oppo_card_num].update_pos(320+idx*80, 120)

        # 自分の合札
        for idx, card_num in enumerate(my_collected_cards):
            self.cards[card_num].set_front_visibility(True)
            self.cards[card_num].update_pos(960+(idx%5)*50, 630-(idx//5)*60)

        # 相手の合札
        for idx, card_num in enumerate(oppo_collected_cards):
            self.cards[card_num].set_front_visibility(True)
            self.cards[card_num].update_pos(43+(idx%5)*50, 65+(idx//5*60))

    def draw(self):
        """
        札の描画の更新を行うo

        ## Returns
        - needs_udpate : アニメーションが必要な場合True
        """
        needs_more_move = False
        for card in self.cards.values():
            needs_more_move |= card.move()
        return needs_more_move

    def card_click_event(self, event):
        print(event)
