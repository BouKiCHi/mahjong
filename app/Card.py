import pyxel


class Card:
    def __init__(self):
        # キャラクタインデックス
        chr_index = []
        for chi in range(9*4):
            if chi == 7 or chi == 8:
                continue
            chr_index.append(chi)

        chr_max = len(chr_index)

        # 残りカウント
        left_chr = [4] * chr_max

        self._chr_index = chr_index
        self._chr_max = chr_max
        self._left_chr = left_chr
        self._left_count = 4 * chr_max

    # 取得
    def get_chr_index(self):
        if self._left_count <= 0:
            raise ValueError("no left")

        chi = pyxel.rndi(0, self._chr_max-1)
        while True:
            if 0 < self._left_chr[chi]:
                self._left_count -= 1
                self._left_chr[chi] -=1
                return self._chr_index[chi]
            chi= (chi+1) % self._chr_max