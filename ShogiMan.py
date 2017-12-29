#-*- encoding: utf-8 -*-

from ShogiGlobal import *
import os

class ShogiMan:
    '''
    Shogiman Base Class
    Data Member: Shogiman type(Wang, Jiang, Xiang, Zi), Shogiman Color(Black, White),
                 Shogiman current location
    Operation: 1. Judge Where Shogiman can go
               2. Get Shogiman Image
    '''

    def getImage(self):
        '''
        load image based on Shogiman type and color
        '''
        kind = ""
        if SHOGIMAN_KIND_WANG == self.kind:
            kind = 'Wang'
        if SHOGIMAN_KIND_JIANG == self.kind:
            kind = 'Jiang'
        if SHOGIMAN_KIND_XIANG == self.kind:
            kind = 'Xiang'
        if SHOGIMAN_KIND_ZI == self.kind:
            kind = 'Zi'
        if SHOGIMAN_KIND_HOU == self.kind:
            kind = 'Hou'
        if SHOGIMAN_KIND_CATCHED_JIANG == self.kind:
            kind = 'Catched_Jiang'
        if SHOGIMAN_KIND_CATCHED_XIANG == self.kind:
            kind = 'Catched_Xiang'
        if SHOGIMAN_KIND_CATCHED_ZI == self.kind:
            kind = 'Catched_Zi'

        color = 'Up'
        if SHOGIMAN_COLOR_DOWN == self.color:
            color = 'Down'

        #print(__file__
        curpath = os.path.dirname(__file__)
        #print(curpath
        curpath = curpath.replace('TwelveShogi.exe', '')
        filename = './BMP/' + kind + '_' + color + '.bmp'
        writeErrorLog(filename)
        return load_image(filename)

    def __init__(self, kind, color, row, col):
        self.kind = kind
        self.color = color
        self.row = row
        self.col = col

    def printInfo(self):
        arrKind = ('Wang', 'Jiang', 'Xiang', 'Zi', 'None')
        arrColor = ('Up', 'Down')
        info = arrColor[self.color] + arrKind[self.kind]
        info = info + " row:%d, col:%d, color:%d" % (self.row, self.col, self.color)
        print("ShogiMan-printInfo: " + info)
        return info

    def ShogimanMoveJudge(self, rowTo, colTo):
        '''
        Judge whether the shogiman can move based on type, current location
        and objective location
        '''
        isSuc = 0
        if rowTo < 0 or rowTo >3 or colTo < 0 or colTo > 2:
            return isSuc
        if SHOGIMAN_KIND_WANG == self.kind:
            if abs(rowTo - self.row) <= 1 and abs(colTo - self.col) <= 1:
                isSuc = 1
        elif SHOGIMAN_KIND_JIANG == self.kind:
            if self.row == rowTo and abs(colTo - self.col) == 1:
                isSuc = 1
            elif self.col == colTo and abs(rowTo - self.row) == 1:
                isSuc = 1
        elif SHOGIMAN_KIND_XIANG == self.kind:
            if abs(rowTo - self.row) == 1 and abs(colTo - self.col) == 1:
                isSuc = 1
        elif SHOGIMAN_KIND_ZI == self.kind:
            if colTo == self.col:
                if rowTo - self.row == 1 and self.color == SHOGIMAN_COLOR_DOWN:
                    isSuc = 1
                elif self.row - rowTo == 1 and self.color == SHOGIMAN_COLOR_UP:
                    isSuc = 1
        elif SHOGIMAN_KIND_HOU == self.kind:
            if self.row == rowTo and abs(colTo - self.col) == 1:
                isSuc = 1
            elif self.col == colTo and abs(rowTo - self.row) == 1:
                isSuc = 1
            elif self.color == SHOGIMAN_COLOR_DOWN and rowTo - self.row == 1 and abs(colTo - self.col) == 1:
                isSuc = 1
            elif self.color == SHOGIMAN_COLOR_UP and self.row - rowTo == 1 and abs(colTo - self.col) == 1:
                isSuc = 1
        elif SHOGIMAN_KIND_CATCHED_JIANG == self.kind or SHOGIMAN_KIND_CATCHED_XIANG == self.kind or SHOGIMAN_KIND_CATCHED_ZI == self.kind:
            if self.color == SHOGIMAN_COLOR_UP and rowTo >= 1 and rowTo <= 3:
                isSuc = 1
            elif self.color == SHOGIMAN_COLOR_DOWN and rowTo >=0 and rowTo <=2:
                isSuc = 1
        # print("ShogiMan-ShogimanMoveJudge: %d" % isSuc)
        return isSuc
        
        
if __name__ == "__main__":

    # Test case
    wang = ShogiMan(SHOGIMAN_KIND_WANG, SHOGIMAN_COLOR_UP, 1, 1)
    print(wang.ShogimanMoveJudge(0, 0))
    print(wang.ShogimanMoveJudge(1, 2))
    print(wang.ShogimanMoveJudge(3, 1))

    jiang = ShogiMan(SHOGIMAN_KIND_JIANG, SHOGIMAN_COLOR_UP, 1, 1)
    print(jiang.ShogimanMoveJudge(1, 2))
    print(jiang.ShogimanMoveJudge(2, 2))

    xiang = ShogiMan(SHOGIMAN_KIND_XIANG, SHOGIMAN_COLOR_UP, 1, 1)
    print(xiang.ShogimanMoveJudge(1, 2))
    print(xiang.ShogimanMoveJudge(2, 2))

    zi = ShogiMan(SHOGIMAN_KIND_ZI, SHOGIMAN_COLOR_UP, 1, 1)
    print(zi.ShogimanMoveJudge(1, 2))
    print(zi.ShogimanMoveJudge(1, 0))
    print(zi.ShogimanMoveJudge(2, 1))
    print(zi.ShogimanMoveJudge(0, 1))

    zi = ShogiMan(SHOGIMAN_KIND_ZI, SHOGIMAN_COLOR_DOWN, 1, 1)
    print(zi.ShogimanMoveJudge(1, 2))
    print(zi.ShogimanMoveJudge(1, 0))

    # o o o
    # o o o
    # o x o
    # o o o
    hou = ShogiMan(SHOGIMAN_KIND_HOU, SHOGIMAN_COLOR_UP, 2, 1)
    # o o o
    # o x o
    # o o o
    # o o o
    print(hou.ShogimanMoveJudge(1, 1))
    # o o o
    # o o o
    # o o o
    # o x o
    print(hou.ShogimanMoveJudge(3, 1))
    # o o o
    # o o o
    # x o o
    # o o o
    print(hou.ShogimanMoveJudge(2, 0))
    # o o o
    # o o o
    # o o x
    # o o o
    print(hou.ShogimanMoveJudge(2, 2))
    # o o o
    # o o o
    # o o o
    # x o o
    print(hou.ShogimanMoveJudge(3, 0))
    # o o o
    # o o o
    # o o o
    # o o x
    print(hou.ShogimanMoveJudge(3, 2))

    # o o o
    # o x o
    # o o o
    # o o o
    hou = ShogiMan(SHOGIMAN_KIND_HOU, SHOGIMAN_COLOR_DOWN, 1, 1)
    # x o o
    # o o o
    # o o o
    # o o o
    print(hou.ShogimanMoveJudge(0, 0))
    # o o o
    # o o o
    # o x o
    # o o o
    print(hou.ShogimanMoveJudge(2, 1))
    # o o o
    # o o o
    # o o o
    # x o o
    print(hou.ShogimanMoveJudge(3, 0))
