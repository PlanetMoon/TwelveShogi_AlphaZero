#-*- encoding: utf-8 -*-

import sys, string, os
import pygame
from pygame.locals import *

# Global Definition

SHOGIBOARD_PRISON_ROW_UP = 4
SHOGIBOARD_PRISON_ROW_DOWN = 5

SHOGIMAN_COLOR_UP = 0
SHOGIMAN_COLOR_DOWN = 1

SHOGIMAN_KIND_NONE = -1
SHOGIMAN_KIND_WANG = 0
SHOGIMAN_KIND_JIANG = 1
SHOGIMAN_KIND_XIANG = 2
SHOGIMAN_KIND_ZI = 3
SHOGIMAN_KIND_HOU = 4
SHOGIMAN_KIND_CATCHED_JIANG = 5
SHOGIMAN_KIND_CATCHED_XIANG = 6
SHOGIMAN_KIND_CATCHED_ZI = 7

SHOGIMAN_NAMELIST = {-1: "0", 0:"UW", 1:"UJ", 2:"UX", 3:"UZ", 4:"UH", 5:"UCJ", 6:"UCX", 7:"UCZ",\
                     8:"DW", 9:"DJ", 10:"DX", 11:"DZ", 12:"DH", 13:"DCJ", 14:"DCX", 15:"DCZ"}

def writeErrorLog(log):
    '''
    Write error logs
    '''
    file = open('error.log', 'a')
    file.write(log + '\n')
    # print('Write Log: ' + log)
    file.close()

def writeTrainingLog(log):
    '''
    Write training logs
    '''
    file = open('training.log', 'a')
    file.write(log + '\n')
    file.close()

# Load Image for ShogiMan
def load_image(name, colorfilter=0xffffff):    
    try:
        image = pygame.image.load(name)
        writeErrorLog('success to loadimage:'+ name)
    except pygame.error as message:
        print("ShogiGlobal-load_image: Cannot load image:", name)
        writeErrorLog('Cannot load image:'+ name)
        raise SystemExit
        return None
    image = image.convert()
    if colorfilter is not None:
        if colorfilter is -1:
            colorfilter = image.get_at((0,0))
        image.set_colorkey(colorfilter, RLEACCEL)
    return image, image.get_rect()

# load the fonts
def load_font(txt):
    # create a font class, font size is 20     
    font = pygame.font.Font(u"C:\\windows\\Fonts\\simsun.ttc", 20)
    # create font
    text = font.render(txt, 1, (255, 0, 0))
    # get text position
    textpos = text.get_rect()
    
    return text, textpos
