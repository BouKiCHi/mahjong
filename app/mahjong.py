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
            mx = pyxel.mouse_x
            my = pyxel.mouse_y

            # リセット
            if (224 <= mx and mx <= 242) and (5 <= my and my <= 10):
                self.reset_card()
                return

            self.try_select(mx, my)

    # タイル選択インデックス
    def get_tile_selected_index(self, px, py):
        return (py * 16)+px

    # 上の段のタイルを取得
    def get_select_tile(self, mx, my):
        for i in range(4):
            plane_no = 3-i
            x = mx + (plane_no * 2)
            y = my + (plane_no * 2)
            px = int(x / 16)
            py = int(y / 20)
            pi = self.get_tile_selected_index(px, py)
            tile = self.tiles[plane_no]
            if tile[pi] != 0:
                return tile, plane_no, px, py, pi
        return None, 0, 0, 0, 0

    # 選択
    def try_select(self, mx, my):
        # 一番上のタイルから選択する
        tile, plane_no, px, py, pi = self.get_select_tile(mx, my)

        # 選択できなかった
        if tile is None:
            pyxel.play(1,3)
            return

        # 選択できない
        if pi-1 < 0 or len(tile) <= pi+1:
            pyxel.play(1,3)
            return
        
        # 両隣がある場合は選択できない
        if tile[pi-1] != 0 and tile[pi+1] != 0:
            pyxel.play(1,3)
            return

        tile_ch = tile[pi]
        # 1つ目の選択
        if self.sel_count == 0:
            mark = self.sel_mark[0]
            mark.set_value(True, px, py, tile_ch, plane_no)
            self.sel_count+=1
            pyxel.play(1,2)
            return

        # 2つ目の選択
        if self.sel_count == 1:
            mark = self.sel_mark[0]
            if mark.x == px and mark.y == py:
                self.sel_count-=1
                mark.visible = False
                return

            # 選択が一致しない
            if mark.ch != tile_ch:
                pyxel.play(1,3)
                return

            self.sel_mark[1].set_value(True, px, py, tile_ch, plane_no)
            self.sel_count+=1
            self.erase_count = 30
            pyxel.play(1,4)

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

                    pyxel.line(x, y, x+13, y, 13)
                    pyxel.line(x-1, y, x-1, y + 20, 13)


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