#-*- encoding: utf-8 -*-

import sys, string, os
import pygame
import datetime
import copy
import numpy as np
from pygame.locals import *
from ShogiGlobal import *
from ShogiMan import *
from TSAI import *

class ShogiBoard:
    '''
    ShogiBoard Class,
    Data: every grid with the shogiman
    Operator: 1, move; 2, repaint the board; 3, show the info; 4 select the shogiman
    '''
    movesteps = 1  # move steps: 0-select shogiman 1-move shogiman
    curTime = datetime.datetime.now()

    # initialize the color as up
    curStepColor = SHOGIMAN_COLOR_UP

    tipInfo = ' '

    
    def shogimanChoose(self, row, col):
        '''
        select the shogiman and the shogiman shining
        '''
        # print("ShogiBoard-shogimanChoose: %d %d %d" % (row*10+col, row, col))
        # print("ShogiBoard-shogimanChoose: keys：%s" % self.board.keys())
        if (row, col) in self.board.keys():
            if self.board[(row, col)] != None:
                self.curRow = row
                self.curCol = col
                self.curTime = datetime.datetime.now()
                self.movesteps = 1
                # print("ShogiBoard-shogimanChoose: " + self.board[(row, col)].printInfo())

    def __init__(self):
        '''
        initialization
        '''
        self.curCol = -1
        self.curRow = -1

        self.resetBoard()

    def resetBoard(self):
        '''
        reset the Board
        '''
        self.curRow = -1
        self.curCol = -1
        self.curStepColor = SHOGIMAN_COLOR_UP
        self.states = {}
        self.movesteps = 0
        self.upWangReached = 0
        self.downWangReached = 0
        self.upCatchedNum = 0
        self.downCatchedNum = 0
        self.moveCounts = 0
        self.board = {
                        (3, 0):ShogiMan(SHOGIMAN_KIND_XIANG, SHOGIMAN_COLOR_UP, 3, 0), \
                        (3, 1):ShogiMan(SHOGIMAN_KIND_WANG, SHOGIMAN_COLOR_UP, 3, 1), \
                        (3, 2):ShogiMan(SHOGIMAN_KIND_JIANG, SHOGIMAN_COLOR_UP, 3, 2), \
                        (2, 1):ShogiMan(SHOGIMAN_KIND_ZI, SHOGIMAN_COLOR_UP, 2, 1), \
                        (0, 0):ShogiMan(SHOGIMAN_KIND_JIANG, SHOGIMAN_COLOR_DOWN, 0, 0), \
                        (0, 1):ShogiMan(SHOGIMAN_KIND_WANG, SHOGIMAN_COLOR_DOWN, 0, 1), \
                        (0, 2):ShogiMan(SHOGIMAN_KIND_XIANG, SHOGIMAN_COLOR_DOWN, 0, 2), \
                        (1, 1):ShogiMan(SHOGIMAN_KIND_ZI, SHOGIMAN_COLOR_DOWN, 1, 1), \
                        }

    def printBoard(self):
        '''
        print the board on the terminal
        '''
        showBoard = np.zeros([6, 6])
        showBoard.fill(-1)
        for key in self.board.keys():
            shogiman = self.board[key]
            if shogiman == None:
                continue
            if shogiman.row <= 4 and shogiman.row >= 0:
                showBoard[shogiman.row + 1][shogiman.col] = shogiman.color * 8 + shogiman.kind
            elif shogiman.row == SHOGIBOARD_PRISON_ROW_DOWN:
                showBoard[0][shogiman.col] = shogiman.color * 8 + shogiman.kind
        print("###############")
        for i in range(6):
            for j in range(6):
                print("{}\t".format(SHOGIMAN_NAMELIST[showBoard[i][j]]), end = "")
            print("")
        print("###############")

    def redrawBoard(self, window):
        '''
        draw the board again
        '''
        window.fill((0, 0, 0))
        ground, rc = load_image("./BMP/Board.bmp", 0x000000)
        window.blit(ground, (0, 0))
        
        # show all the shogiman
        # writeErrorLog('redraw')
        # print("ShogiBoard-redrawBoard: %s" % self.board.keys())
        for key in self.board.keys():
            shogiman = self.board[key]
            if shogiman == None:
                continue;
            if shogiman.row <= 3 and shogiman.row >= 0:
                left = shogiman.col * 140 + 70
                top = shogiman.row * 125 + 80
                image, rc = shogiman.getImage()
                if None == image:
                    continue
                if self.curRow == shogiman.row and self.curCol == shogiman.col:
                    curTime = datetime.datetime.now()
                    if (curTime - self.curTime).microseconds >= 100000:
                        window.blit(image, (left, top))
                    if (curTime - self.curTime).microseconds >= 500000:
                        self.curTime = curTime
                    # writeErrorLog('load shogiman ' + shogiman.printInfo())
                else:
                    window.blit(image, (left, top))
                    # writeErrorLog('load shogiman ' + shogiman.printInfo())
            elif shogiman.row == SHOGIBOARD_PRISON_ROW_UP:             # up
                top = 593
                left = shogiman.col * 40 + 155
                image, rc = shogiman.getImage()
                # print("ShogiBoard-redrawBoard: %d %d %d" % (shogiman.kind, shogiman.row, shogiman.col))
                if None == image:
                    continue
                if self.curRow == shogiman.row and self.curCol == shogiman.col:
                    curTime = datetime.datetime.now()
                    if (curTime - self.curTime).microseconds >= 100000:
                        window.blit(image, (left, top))
                    if (curTime - self.curTime).microseconds >= 500000:
                        self.curTime = curTime
                else:
                    window.blit(image, (left, top))
            elif shogiman.row == SHOGIBOARD_PRISON_ROW_DOWN:             # down
                top = 18
                left = shogiman.col * 40 + 155
                image, rc = shogiman.getImage()
                # print("ShogiBoard-redrawBoard: %d %d" % (left, top))
                if None == image:
                    continue
                if self.curRow == shogiman.row and self.curCol == shogiman.col:
                    curTime = datetime.datetime.now()
                    if (curTime - self.curTime).microseconds >= 100000:
                        window.blit(image, (left, top))
                    if (curTime - self.curTime).microseconds >= 500000:
                        self.curTime = curTime
                else:
                    window.blit(image, (left, top))

    def showTipInfo(self, window):
        '''
        show tips under the board
        '''

        # show the text in the window
        text, textpos = load_font(self.tipInfo)
        # textpos.centerx = window.get_rect().centerx
        textpos = Rect(0, 645, 560, 28)
        window.blit(text, textpos)

    def moveShogimanColorJudge(self, row, col):
        '''
        judge whether the color is same
        '''
        if (row, col) in self.board.keys():
            shogiman = self.board[(row, col)]
            if None != shogiman:
                if shogiman.color != self.curStepColor:
                    if SHOGIMAN_COLOR_DOWN == shogiman.color:
                        self.tipInfo = ('It is up turn')
                    else:
                        self.tipInfo = ('It is down turn')
                    return 0
        return 1
    
    def resuffleBoardPrisonRow(self, row, col):
        '''
        resuffle the row of Prison after move from prison
        '''
        # print("ShogiBoard-resuffleBoardPrisonRow: %d %d" % (row, col))
        if (row, col) in self.board.keys():
            if row == SHOGIBOARD_PRISON_ROW_UP:
                for col_i in range(col + 1, self.upCatchedNum):
                    if (row, col_i) in self.board.keys():
                        self.board[(row, col_i - 1)] = self.board[(row, col_i)]
                        self.board[(row, col_i - 1)].col = col_i - 1
                        self.board[(row, col_i)] = None
                        # print("ShogiBoard-resuffleBoardPrisonRow: %d %d %d" % (self.board[(row, col_i-1)].kind, row, col_i-1))
                self.upCatchedNum = self.upCatchedNum - 1
            elif row == SHOGIBOARD_PRISON_ROW_DOWN:
                for col_i in range(col + 1, self.downCatchedNum):
                    if (row, col_i) in self.board.keys():
                        self.board[(row, col_i - 1)] = self.board[(row, col_i)]
                        self.board[(row, col_i - 1)].col = col_i - 1
                        self.board[(row, col_i)] = None
                self.downCatchedNum = self.downCatchedNum - 1

    def moveShogiman(self, rowTo, colTo):
        '''
        move the shogiman and redraw the board
        '''
        if 0 == self.moveShogimanColorJudge(rowTo, colTo) and 0 == self.movesteps:
            # it's opposite turn
            return 0
        if 0 == self.movesteps:
            self.shogimanChoose(rowTo, colTo)
            return 2
            # print('ShogiBoard-moveShogiman: choose shogiman')
        else:
            m = self.curRow * 72 + self.curCol * 12 + rowTo * 3 + colTo
            if m in self.avaliableMove():
                # print("ShogiBoard-moveShogiman: move: %d" % m)
                result = self.doMove(m)
                if result == 1:
                    self.tipInfo = ('game over, up win!')
                    print('ShogiBoard-moveShogiman: game over, up win!')
                    self.resetBoard()
                    return 3
                elif result == 2:
                    self.tipInfo = ('game over, down win!')
                    print('ShogiBoard-moveShogiman: game over, down win!')
                    self.resetBoard()
                    return 3
                elif result == 0:
                    return 1
                elif result == 3:
                    self.tipInfo = ('game over, tie!')
                    print('ShogiBoard-moveShogiman: game over, tie!')
                    self.resetBoard()
                    return 3
            elif (rowTo, colTo) in self.board.keys():
                shogimanTo = self.board[(rowTo, colTo)]
                if shogimanTo != None and self.board[(self.curRow, self.curCol)].color == shogimanTo.color:
                    self.moveSteps = 0
                    self.shogimanChoose(rowTo, colTo)
                    return 2
            return 0

    def avaliableMove(self):
        avaliables = list(range(0))     # maxrow(6) * maxcol(6) * board(12)
        # board
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # 9 10 11
        for key in self.board.keys():
            shogiman = self.board[key]
            if shogiman == None:
                continue;
            if shogiman.color != self.curStepColor:
                continue;
            # print("ShogiBoard-avaliableMove: %d %d %d %d" % (shogiman.color, shogiman.kind, shogiman.row, shogiman.col))
            for i in range(0, 4):
                for j in range(0, 3):
                    # print("ShogiBoard-avaliableMove: %d %d" % (i, j))
                    if (i, j) in self.board.keys():
                        shogimanTo = self.board[(i, j)]
                        if shogimanTo != None and shogiman.color == shogimanTo.color:
                            continue;
                    if shogiman.ShogimanMoveJudge(i, j) == 1:
                        if shogiman.kind >= SHOGIMAN_KIND_CATCHED_JIANG and (i, j) in self.board.keys() and self.board[(i, j)] != None:
                            continue;
                        avaliables.append(shogiman.row*6*12+shogiman.col*12+i*3+j)
                        # print("ShogiBoard-avaliableMove: avaliable %d %d %d %d %d %d" % (shogiman.color, shogiman.kind, shogiman.row, shogiman.col, i, j))
        return avaliables

    def doMove(self, move):
        self.curRow = int(move // 72) # 6*12
        self.curCol = int(move % 72 // 12)
        rowTo = int(move % 12 / 3)
        colTo = move % 12 % 3
        shogiman = self.board[(self.curRow, self.curCol)]
        # print("ShogiBoard-doMove: %d %d %d %d %d" % (shogiman.kind, self.curRow, self.curCol, rowTo, colTo))
        # return shogiman
        # Zi reach the bottom
        if shogiman.kind == SHOGIMAN_KIND_ZI:
            if (2 == shogiman.row and 3 == rowTo) or (1 == shogiman.row and 0 == rowTo):
                shogiman.kind = SHOGIMAN_KIND_HOU
        # Wang reach the bottom
        if shogiman.kind == SHOGIMAN_KIND_WANG:
            if (3 == rowTo and shogiman.color == SHOGIMAN_COLOR_DOWN):
                self.downWangReached = 1
            elif (0 == rowTo and shogiman.color == SHOGIMAN_COLOR_UP):
                self.upWangReached = 1
        # move Shogiman from prison
        if shogiman.kind == SHOGIMAN_KIND_CATCHED_JIANG:
            shogiman.kind = SHOGIMAN_KIND_JIANG
            self.resuffleBoardPrisonRow(shogiman.row, shogiman.col)
        if shogiman.kind == SHOGIMAN_KIND_CATCHED_XIANG:
            shogiman.kind = SHOGIMAN_KIND_XIANG
            self.resuffleBoardPrisonRow(shogiman.row, shogiman.col)
        if shogiman.kind == SHOGIMAN_KIND_CATCHED_ZI:
            shogiman.kind = SHOGIMAN_KIND_ZI
            self.resuffleBoardPrisonRow(shogiman.row, shogiman.col)

        if (rowTo, colTo) in self.board.keys():
            shogimanTo = self.board[(rowTo, colTo)]
        else:
            shogimanTo = None

        # Catch the prisoner
        if shogimanTo != None and SHOGIMAN_KIND_WANG != shogimanTo.kind:
            shogimanTo.color = self.curStepColor
            if SHOGIMAN_COLOR_UP == self.curStepColor:
                self.board[(SHOGIBOARD_PRISON_ROW_UP, self.upCatchedNum)] = shogimanTo
                shogimanTo.row = SHOGIBOARD_PRISON_ROW_UP
                shogimanTo.col = self.upCatchedNum
                self.upCatchedNum = self.upCatchedNum + 1
            elif SHOGIMAN_COLOR_DOWN == self.curStepColor:
                self.board[(SHOGIBOARD_PRISON_ROW_DOWN, self.downCatchedNum)] = shogimanTo
                shogimanTo.row = SHOGIBOARD_PRISON_ROW_DOWN
                shogimanTo.col = self.downCatchedNum
                self.downCatchedNum = self.downCatchedNum + 1
            if SHOGIMAN_KIND_JIANG == shogimanTo.kind:
                shogimanTo.kind = SHOGIMAN_KIND_CATCHED_JIANG
            elif SHOGIMAN_KIND_XIANG == shogimanTo.kind:
                shogimanTo.kind = SHOGIMAN_KIND_CATCHED_XIANG
            elif SHOGIMAN_KIND_ZI == shogimanTo.kind or SHOGIMAN_KIND_HOU == shogimanTo.kind:
                shogimanTo.kind = SHOGIMAN_KIND_CATCHED_ZI
                
        self.board[(rowTo, colTo)] = shogiman
        shogiman.row = rowTo
        shogiman.col = colTo
        if self.curRow != SHOGIBOARD_PRISON_ROW_UP and self.curRow != SHOGIBOARD_PRISON_ROW_DOWN:
            self.board[(self.curRow, self.curCol)] = None
            
        self.curRow = -1
        self.curCol = -1
        self.movesteps = 0
        # self.tipInfo = ('last moving shogiman: %s' % shogiman.printInfo()
        self.moveCounts = self.moveCounts + 1
        # print("ShogiBoard-doMove: move = %d" % self.moveCounts)
        self.states[self.moveCounts] = copy.deepcopy(self.board)

        if shogimanTo != None and SHOGIMAN_KIND_WANG == shogimanTo.kind:
            if SHOGIMAN_COLOR_UP == shogimanTo.color:
                # print('ShogiBoard-moveShogiman: game over, down win!')
                return 2
            else:
                # print('ShogiBoard-moveShogiman: game over, up win!')
                return 1
        elif SHOGIMAN_COLOR_DOWN == self.curStepColor and self.upWangReached == 1:
            # print('ShogiBoard-moveShogiman: game over, up win!')
            return 1
        elif SHOGIMAN_COLOR_UP == self.curStepColor and self.downWangReached == 1:
            # print('ShogiBoard-moveShogiman: game over, down win!')
            return 2
            
        if self.curStepColor == SHOGIMAN_COLOR_UP:
            self.curStepColor = SHOGIMAN_COLOR_DOWN
        else:
            self.curStepColor = SHOGIMAN_COLOR_UP
        if self.moveCounts >= 40:
            return 3 # tie
        return 0

    def currentState(self):
        '''
        6*6*34 = N*N*(MT+L)
        N = 6 size of board which include the prison
        M = 8*2 8 types of pieces: Wang, Jiang, Xiang, Zi, Hou, Catched_Jiang, Catched_Xiang, Catched_Zi
        T = 2 history 2 steps
        L = 2 Color 1 + Total move count 1
        '''
        curState = np.zeros((34, 6, 6))
        if self.states:
            board = self.states[self.moveCounts]
            for key in board.keys():
                shogiman = board[key]
                if shogiman == None:
                    continue
                if shogiman.color == self.curStepColor:
                    curState[shogiman.kind][shogiman.row][shogiman.col] = 1.0
                else:
                    curState[shogiman.kind+8][shogiman.row][shogiman.col] = 1.0
            if self.moveCounts - 1 > 0:
                board1 = self.states[self.moveCounts - 1]
                for key in board1.keys():
                    shogiman = board[key]
                    if shogiman == None:
                        continue
                    if shogiman.color == self.curStepColor:
                        curState[shogiman.kind+16][shogiman.row][shogiman.col] = 1.0
                    else:
                        curState[shogiman.kind+24][shogiman.row][shogiman.col] = 1.0
        if len(self.states)%2 == 0:
            curState[32][:,:] = 1.0
        curState[33][:,:] = self.moveCounts
        return curState

if __name__ == "__main__":

    # Test case
    shogiboard = ShogiBoard()
    for k in range(1,5):
        a = shogiboard.avaliableMove()
        i = 0
        for m in a:
            if i == 1:
                shogiboard.doMove(m)
                break
            i = i + 1
    cs = shogiboard.currentState()
    print(cs)
    print("______________________________________")
    board = np.zeros((6,6))
    for key in shogiboard.board.keys():
        shogiman = shogiboard.board[key]
        if shogiman == None:
            continue
        else:
            board[shogiman.row][shogiman.col] = shogiman.kind + 1
    print(board)
    print("______________________________________")
    shogiboard.resetBoard()
    shogiboard.doMove(160)             # (2, 1) to (1, 1)
    shogiboard.doMove(28)              # (0, 2) to (1, 1)
    a = shogiboard.avaliableMove()
    for m in a:
        result = shogiboard.doMove(m)
        print(result)
        shogiboard.resetBoard()
        shogiboard.doMove(160)             # (2, 1) to (1, 1)
        shogiboard.doMove(28)              # (0, 2) to (1, 1)
