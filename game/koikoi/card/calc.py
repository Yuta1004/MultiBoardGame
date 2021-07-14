from enum import Enum


class Role(Enum):
    FiveLights = 0                       # 五光
    FourLights = 1                      # 四光
    FourLights_with_Willow =2    # 雨四光
    ThreeLights = 3                    # 三光
    Hanami_de_Ippai = 3             # 花見で一杯
    Tsukimi_de_Ippai = 4             # 月見で一杯
    Boar_Deer_Butterfly = 5       # 猪鹿蝶
    BlueSlips = 6                        # 青タン
    RedSlips = 7                         # 赤タン
    Blue_Red_Slips = 8               # 青タンと赤タンの重複
    Animals = 9                          # タネ
    Slips = 10                             # タン
    Drags = 11                           # カス


def calc_score(collected_card):
    """
    得点および出来役を集計して返す

    ## CalcOrder
    O(n)

    ## Params
    - collected_card : 集めた全てのカードについて，その番号のOR演算を行った結果

    ## Returns
    - score : 得点
    - roles : 出来役(Role)とその得点のタプルのリスト
    """
    score = 0
    roles = []

    if check_enable_bit_nums(collected_card, 0xf80000)  ==  5:       # 五光
        score += 10
        roles.append((Role.FiveLights, 10))
    elif check_enable_bit_nums(collected_card, 0xf80000) == 4:      # 四光
        if collected_card & 0x800000 > 0:
            score += 7
            roles.append((Role.FourLights_with_Willow, 7))
        else:
            score += 8
            roles.append((Role.FourLights, 8))
    elif check_enable_bit_nums(collected_card, 0x380000) == 3:      # 三光
        score += 5
        roles.append((Role.ThreeLights, 5))

    # 花見で一杯
    if check_enable_bit_nums(collected_card, 0x88000) == 2:
        score += 5
        roles.append((Role.Hanami_de_Ippai, 5))

    # 月見で一杯
    if check_enable_bit_nums(collected_card, 0x108000) == 2:
        score += 5
        roles.append((Role.Tsukimi_de_Ippai, 5))

    # 猪鹿蝶
    if check_enable_bit_nums(collected_card, 0x70000) == 3:
        surplus = check_enable_bit_nums(collected_card, 0xfc00)
        score += 5 + surplus
        roles.append((Role.Boar_Deer_Butterfly, 5+surplus))

    if check_enable_bit_nums(collected_card, 0x3f0) == 6:       # 赤短と青短の重複
        surplus = check_enable_bit_nums(collected_card, 0xf)
        score += 10 + surplus
        roles.append((Role.Blue_Red_Slips, 10+surplus))
    elif check_enable_bit_nums(collected_card, 0x70) == 3:      # 赤短
        surplus = check_enable_bit_nums(collected_card, 0x38f)
        score += 5 + surplus
        roles.append((Role.RedSlips, 5+surplus))
    elif check_enable_bit_nums(collected_card, 0x380) == 3:     # 青短
        surplus = check_enable_bit_nums(collected_card, 0x7f)
        score += 5 + surplus
        roles.append((Role.BlueSlips, 5+surplus))
    elif check_enable_bit_nums(collected_card, 0x3ff) >= 5:     # タン
        surplus = check_enable_bit_nums(collected_card, 0x3ff)
        score += 1 + surplus - 5
        roles.append((Role.Slips, 1+surplus-5))

    # タネ
    if check_enable_bit_nums(collected_card, 0x7fc00) > 5:
        surplus = check_enable_bit_nums(collected_card, 0x7fc00)
        score += 1 + surplus - 5
        roles.append((Role.Animals, 1+surplus-5))

    # カス
    if  check_enable_bit_nums(collected_card, 0xffffff008000) > 10:
        surplus = check_enable_bit_nums(collected_card, 0xffffff008000)
        score += 1 + surplus - 10
        roles.append((Role.Drags, 1+surplus-10))

    return score, roles


def check_enable_bit_nums(target, mask):
    """
    数targetについてビットマスクmaskの範囲で立っているビット数を返す

    ## Params
    - target : カウント対象となる数
    - mask : ビットマスク

    ## Results
    - count : 立っていたビット数
    """
    count = 0
    checker = target & mask
    while checker > 0:
        count +=  checker & 1
        checker >>= 1
    return count
