def get_card_month(card_num):
    """
    与えられた番号の札について何月のものなのかを返す

    ## Params
    - card_num : カード番号

    ## Returns
    - month : 月
    """
    masks = [0x3200010,         0xc000420,        0x30080040,         0xc0000801,
                  0x300001002,     0xc00010080,     0x3000020004,     0xc000102000,
                  0x30000008100, 0xc0000040200, 0x100000804008, 0xe00000400000]
    for month, mask in enumerate(masks, start=1):
        if card_num & mask > 0:
            return month
