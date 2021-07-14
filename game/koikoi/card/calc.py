from enum import Enum


class Role(Enum):
    Goko = 0                    # 五光
    Shiko = 1                    # 四光
    Sanko = 2                   # 三光
    HanamiDeIppai = 3      # 花見で一杯
    TsukimiDeIppai = 4      # 月見で一杯
    InoShikaCho = 5         #  猪鹿蝶
    Akatan = 6                 # 赤短
    Aotan = 7                   # 青短
    AkatanAndAotan = 8  # 赤単と青短の重複
    Tane = 9                     # タネ
    Tan = 10                     # タン
    Kasu = 11                   # カス


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
        roles.append((Role.Goko, 10))
    elif check_enable_bit_nums(collected_card, 0xf80000) == 4:      # 四光
        if collected_card & 0x800000 > 0:
            score += 7
            roles.append((Role.Shiko, 7))
        else:
            score += 8
            roles.append((Role.Shiko), 8)
    elif check_enable_bit_nums(collected_card, 0x380000) == 3:      # 三光
        score += 5
        roles.append((Role.Sanko, 5))

    # 花見で一杯
    if check_enable_bit_nums(collected_card, 0x88000) == 2:
        score += 5
        roles.append((Role.HanamiDeIppai, 5))

    # 月見で一杯
    if check_enable_bit_nums(collected_card, 0x108000) == 2:
        score += 5
        roles.append((Role.TsukimiDeIppai, 5))

    # 猪鹿蝶
    if check_enable_bit_nums(collected_card, 0x70000) == 3:
        surplus = check_enable_bit_nums(collected_card, 0xfc00)
        score += 5 + surplus
        roles.append((Role.InoShikaCho, 5+surplus))

    if check_enable_bit_nums(collected_card, 0x3f0) == 6:       # 赤短と青短の重複
        surplus = check_enable_bit_nums(collected_card, 0xf)
        score += 10 + surplus
        roles.append((Role.AkatanAndAotan, 10+surplus))
    elif check_enable_bit_nums(collected_card, 0x3ff) >= 5:     # タン
        surplus = check_enable_bit_nums(collected_card, 0x3ff)
        score += 1 + surplus - 5
        roles.append((Role.Tan, 1+surplus-5))
    elif check_enable_bit_nums(collected_card, 0x70) == 3:      # 赤短
        surplus = check_enable_bit_nums(0x38f)
        score += 5 + surplus
        roles.append((Role.Akatan, 5+surplus))
    elif check_enable_bit_nums(collected_card, 0x380) == 3:     # 青短
        surplus = check_enable_bit_nums(0x7f)
        score += 5 + surplus
        roles.append((Role.Aotan, 5+surplus))

    # タネ
    if check_enable_bit_nums(collected_card, 0x7fc00) > 5:
        surplus = check_enable_bit_nums(collected_card, 0x7fc00)
        score += 1 + surplus - 5
        roles.append((Role.Tane, 1+surplus-5))

    # カス
    if  check_enable_bit_nums(collected_card, 0xffffff008000) > 10:
        surplus = check_enable_bit_nums(collected_card, 0xffffff008000)
        score += 1 + surplus - 10
        roles.append((Role.Kasu, 1+surplus-10))

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
