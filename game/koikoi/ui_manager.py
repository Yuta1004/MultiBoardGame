from game.koikoi.card.card import Card


class KoiKoiUIManager:
    """
    ゲームUIの管理を行う (主に札の描画)
    """

    def __init__(self, canvas, notice_func):
        """
        KoiKoiUIManagerのコンストラクタ

        ## Params
        - canvas : キャンバス(tkinter)
        - notice_func : 札選択イベントを通知する先 (card_numを引数に持つ)
        """
        self.canvas = canvas
        self.notice_func = notice_func
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
            self.canvas.tag_bind("Card"+str(1<< card_num), "<Button-1>", self.card_click_event)

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
        # 場札アニメーション用に保持
        self.on_field_cards = [(card_num, None) for card_num in on_field_cards]

        # 場札
        h_size = (len(on_field_cards)+1) // 2
        for idx, card_num in enumerate(on_field_cards):
            self.cards[card_num].set_front_visibility(True)
            self.cards[card_num].update_pos(470+(idx%h_size)*80, 350+(-1 if idx//h_size == 0 else 1)*65)

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

    def replace_card_tmp_move(self, from_card_num, to_card_num):
        """
        仮移動アニメーションを発火させる
        ※使い所->ユーザが持札を選択したとき or 山札から札を選択するとき
        ※これは表示を変えているだけなので，必ず後でreplace_cardを呼び出すこと

        ## Param
        - from_card_num : 移動する札の番号
        - to_card_num : 移動する札が向かう先の札の番号 (None指定可，この場合は場の空いている場所に移動)
        """
        self.cards[from_card_num].set_front_visibility(True)
        if to_card_num is None:
            self.on_field_cards.append((from_card_num, None))
            h_size = (len(self.on_field_cards)+1) // 2
            for idx, card_num in enumerate(self.on_field_cards):
                self.cards[card_num[0]].set_front_visibility(True)
                self.cards[card_num[0]].update_pos(470+(idx%h_size)*80, 350+(-1 if idx//h_size == 0 else 1)*65)
                if card_num[1] is not None:     # 重なっていた場合
                    self.cards[card_num[1]].set_front_visibility(True)
                    self.cards[card_num[1]].update_pos(470+(idx%h_size)*80+10, 350+(-1 if idx//h_size == 0 else 1)*65+8)
        else:
            (x, y) = self.cards[to_card_num].get_pos()
            self.cards[from_card_num].update_pos(x+10, y+8)
            for idx, card_num in enumerate(self.on_field_cards):    # 重なりを反映させる
                if card_num[0] == to_card_num:
                    self.on_field_cards[idx] = (to_card_num, from_card_num)

    def set_highlight_visibility_all_cards(self, visibility=True):
        """
        全札のハイライト効果を制御する

        ## Params
        - visibility : ハイライト効果を表示する場合True
        """
        for card in self.cards.values():
            card.set_highlight_visibility(False)

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
        # クリック位置を基に実際にクリックされた札の番号を求める(重なりなどの影響でいくつか候補が存在する場合がある)
        clicked_card_num = None
        cx, cy = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        for clicked_candidate_obj in self.canvas.find_overlapping(cx, cy, cx, cy):
            tags = self.canvas.itemcget(clicked_candidate_obj, 'tags')
            if "current" in tags:
                clicked_card_num = tags.split(" ")[0].replace("Card", "")
        if clicked_card_num is None:
            return
        clicked_card_num = int(clicked_card_num)

        self.notice_func(clicked_card_num)
