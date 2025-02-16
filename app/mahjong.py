# title: Mahjong solitaire
# author: BouKiCHi
# desc: A Pyxel simple Mahjong solitaire
# license: MIT
# version: 1.0

import pyxel

from Card import Card
from SelectionData import SelectionData

class App:
    def __init__(self):

        pyxel.init(256, 256, title="Pyxel Mahjong solitaire")
        pyxel.load("myres.pyxres")
        pyxel.mouse(True)

        # キャラクタ座標
        chrpos_table = []
        for yi in range(4):
            for xi in range(9):
                chrpos_table.append([xi*16, yi*20])
        self.chrpos_table = chrpos_table

        # リセット
        self.reset_card()

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    # リセット
    def reset_card(self):
        self.sel_mark = [SelectionData(False,0,0,0,0), SelectionData(False,0,0,0,0)]
        self.sel_count = 0
        self.left_count = 0
        self.erase_count = 0
        self.time_count = 0
        card = Card()

        # 場に並べる
        tiles = []
        # 1段目タイル
        tile = [0] * (16*12)
        self.fill_card(3, 2, 10, 8, card, tile)
        tiles.append(tile)

        # 2段目タイル
        tile = [0] * (16*12)
        self.fill_card(5, 3, 6, 6, card, tile)
        tiles.append(tile)

        # 3段目タイル
        tile = [0] * (16*12)
        self.fill_card(6, 4, 4, 4, card, tile)
        tiles.append(tile)

        # 4段目タイル
        tile = [0] * (16*12)
        self.fill_card(7, 5, 2, 2, card, tile)
        tiles.append(tile)
        self.tiles = tiles

    # カード
    def fill_card(self, xofs:int, yofs:int, w:int, h:int, card:Card, tile):
        for yi in range(h):
            for xi in range(w):
                i = ((yi+yofs)*16)+(xi+xofs)
                ch = card.get_chr_index()+1
                self.left_count+=1
                tile[i] = ch

    # 更新
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if 0 < self.left_count:
            self.time_count+=1

        # 消去イベント
        if 0 < self.erase_count:
            self.erase_count-=1
            if self.erase_count == 0:
                for si in range(2):
                    mark = self.sel_mark[si]
                    tile = self.tiles[mark.plane_no]
                    px = mark.x
                    py = mark.y
                    pi = (py * 16)+px
                    tile[pi] = 0
                    self.sel_mark[si].visible = False

                self.left_count-=2
                self.sel_count=0
            return

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            px = int(pyxel.mouse_x / 16)
            py = int(pyxel.mouse_y / 20)
            if py == 0 and (px == 14 or px == 15):
                self.reset_card()
                return

            self.try_select(px, py)

    # 上の段のタイルを取得
    def get_select_tile(self, pi):
        for i in range(4):
            plane_no = 3-i
            tile = self.tiles[plane_no]
            if tile[pi] != 0:
                return tile, plane_no
        return None, 0

    # 選択
    def try_select(self, px, py):
        # 一番上のタイルから選択する
        pi = (py * 16)+px

        tile, plane_no = self.get_select_tile(pi)
        if tile is None:
            return

        # 選択できない
        if pi-1 < 0 or len(tile) <= pi+1:
            return
        
        # 隣が無い場合は選択できる
        if tile[pi-1] == 0 or tile[pi+1] == 0:
            tile_ch = tile[pi]
            # 1つ目の選択
            if self.sel_count == 0:
                mark = self.sel_mark[0]
                mark.set_value(True, px, py, tile_ch, plane_no)
                self.sel_count+=1
                return

            # 2つ目の選択
            if self.sel_count == 1:
                mark = self.sel_mark[0]
                if mark.x == px and mark.y == py:
                    self.sel_count-=1
                    mark.visible = False
                    return
                
                if mark.ch == tile_ch:
                    self.sel_mark[1].set_value(True, px, py, tile_ch, plane_no)
                    self.sel_count+=1
                    self.erase_count = 30

    # 描画
    def draw(self):
        pyxel.cls(3)

        tiles = self.tiles
        for plane_no in range(4):
            tile = tiles[plane_no]
            ti = 0
            for yi in range(12):
                for xi in range(16):
                    ch = tile[ti]
                    ti+=1
                    if ch == 0:
                        continue
                    u,v = self.chrpos_table[ch-1]
                    x = xi * 16
                    y = yi * 20
                    x -= (plane_no)*2
                    y -= (plane_no)*2
                    pyxel.blt(x, y, 0, u, v, 16, 20)

                    # 側面の部分
                    sx = 0
                    if plane_no != 0:
                        sx = 16
                    pyxel.blt(x, y+20, 0, sx, 80, 16, 3)

        # 選択
        for si in range(2):
            mark = self.sel_mark[si]
            if mark.visible:
                x = mark.x*16
                y = mark.y*20
                plane_no = mark.plane_no
                x -= plane_no * 2
                y -= plane_no * 2
                pyxel.rectb(x, y, 16, 20, 8)

        # 文字
        pyxel.text(5, 5, "LEFT: %d" % self.left_count, 7)
        pyxel.text(100, 5, "TIME: %d" % int(self.time_count/50), 7)
        pyxel.text(224, 5, "RESET", 7)

        if self.left_count == 0:
            pyxel.text(110, 100, "CLEAR!!", 7)



App()