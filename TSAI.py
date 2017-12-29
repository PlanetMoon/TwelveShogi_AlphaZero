#-*- encoding: utf-8 -*-

import sys, string, os
import pygame
from pygame.locals import *

class TSAI:
    '''
    AI for twelve shogi
    '''

    def evaluate(self, board):
        moves = board.avaliableMove()
        count = 0
        for move in moves:
            count = count + 1
            if count >= 3:
                return move
        return move

    def get_action(self, board):
        return self.evaluate(board)

