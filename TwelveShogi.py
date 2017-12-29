#-*- encoding: utf-8 -*-
import sys, string, os, getopt
import pygame
from pygame.locals import *
from ShogiBoard import *
from mcts import *
from mcts_pure import MCTSPlayer as MCTS_Pure
from TSAI import *
import time
    
#initialization
pygame.init()
# Set the window size, the figure size is 569*643，
window = pygame.display.set_mode((569, 670)) 
# analyze the arguments
startColor = SHOGIMAN_COLOR_UP
mode = 0    # 0 People vs People
            # 1 People vs Computer
            # 2 Computer vs Computer
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:m:")
except getopt.GetoptError:
    print('TwelveShogi.py -c <startColor(0 or 1)> -m <mode(0 or 1 or 2)>')
    sys.exit()
for opt, arg in opts:
    if opt == '-c':
        startColor = int(arg)
    elif opt == '-m':
        mode = int(arg)
shogiboard = ShogiBoard()
shogiboard.curStepColor = startColor
shogiboard.redrawBoard(window)

if mode == 1:
    # AIPlayer = TSAI()
    AIPlayer = MCTS_Pure()
    # AIPlayer = MCTSPlayer()
elif mode == 2:
    # AIPlayer = TSAI()
    AIPlayer = MCTS_Pure()
    trainCounts = 0
    # AIPlayer = MCTSPlayer(is_selfplay = 1)

top = 80
left = 70
yGap = 125
xGap = 140

curRow = 3
curCol = 0

#current mouse position
curPos, rc = load_image("./BMP/curPos.bmp", 0xffffff)
window.blit(curPos, (curCol * xGap + left, curRow * yGap + top))

# event loop
while True:  
    # show update
    pygame.display.update()
    for event in pygame.event.get():
        moveResult = 0
        if event.type == pygame.QUIT: # Quit if window closed
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:# Quit if ESC pressed
                sys.exit()  
        if mode == 0 or mode == 1:  
            # mouse control
            leftMouseButton = pygame.mouse.get_pressed()[0]
            if leftMouseButton:
                (xPos, yPos) = pygame.mouse.get_pos()
                # print("TwelveShogi: xPos:%f, yPos:%f" % (xPos, yPos))
                # Down prison
                if yPos > 18.0000 and yPos < 53.0000:
                    curRow = SHOGIBOARD_PRISON_ROW_DOWN
                    curCol = int((xPos - 155) / 40)

                # Up prison
                elif yPos > 593.000 and yPos < 628.000:
                    curRow = SHOGIBOARD_PRISON_ROW_UP
                    curCol = int((xPos - 155) / 40)
                else:
                    curRow = int((yPos - top) / yGap)
                    curCol = int((xPos - left) / xGap)
                # print("TwelveShogi: curRow:%d, curCol:%d" % (curRow, curCol))
                moveResult = shogiboard.moveShogiman(curRow, curCol)
                if moveResult == 1 and mode == 1:
                    shogiboard.redrawBoard(window)
                    shogiboard.showTipInfo(window)

                    window.blit(curPos,(curCol * xGap + left, curRow * yGap + top))
                    move = AIPlayer.get_action(board=shogiboard)
                    result = shogiboard.doMove(move)
                    if result == 1:
                        shogiboard.tipInfo = ('game over, up win!')
                        print('ShogiBoard-moveShogiman: game over, up win!')
                        shogiboard.resetBoard()
                    elif result == 2:
                        shogiboard.tipInfo = ('game over, down win!')
                        print('ShogiBoard-moveShogiman: game over, down win!')
                        shogiboard.resetBoard()
                    elif result == 3:
                        shogiboard.tipInfo = ('game over, tie!')
                        print('ShogiBoard-moveShogiman: game over, tie!')
                        shogiboard.resetBoard()
                elif moveResult == 0:
                    pass
            shogiboard.redrawBoard(window)
            shogiboard.showTipInfo(window)
            window.blit(curPos,(curCol * xGap + left, curRow * yGap + top))
            #show update
            pygame.display.update()
    if mode == 2:
        move = AIPlayer.get_action(board=shogiboard)
        result = shogiboard.doMove(move)
        if result != 0:
            if result == 1:
                shogiboard.tipInfo = ('game over, up win!')
                print('ShogihogiBoard-moveShogiman: game over, up win! train counts: %d' % trainCounts)
                shogiboard.resetBoard()
            elif result == 2:
                shogiboard.tipInfo = ('game over, down win!')
                print('ShogiBoard-moveShogiman: game over, down win! train counts: %d' % trainCounts)
                shogiboard.resetBoard()
            elif result == 3:
                shogiboard.tipInfo = ('game over, tie!')
                print('ShogiBoard-moveShogiman: game over, tie! train counts: %d' % trainCounts)
                shogiboard.resetBoard()
            trainCounts = trainCounts + 1
            shogiboard.redrawBoard(window)
            shogiboard.showTipInfo(window)
            window.blit(curPos,(curCol * xGap + left, curRow * yGap + top))
