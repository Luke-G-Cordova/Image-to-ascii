import numpy as np
import pygame
from pygame.locals import *

# calculates the brightness of a character
# takes a string character and a screen to
# be used to draw on too
def calcBrightness(character, screen):
    font = pygame.font.SysFont(None, 20)
    letter = font.render(character, True, (255, 255, 255))
    screen.blit(letter, (0, 0))
    avgB = 0
    for x in range(20):
        for y in range(20):
            px = screen.get_at((x, y))
            avg = px[0]+px[1]+px[2]
            avg /= 3
            avgB += avg
    avgB /= (20*20)
    return avgB


# uses calcBrightness() to sort a string ascii
# characters by brightness
def sortByBrightness(ascii, screen):
    dtype = [('character', 'S10'), ('brightness', float)]
    holdArr = []
    for letter in ascii:
        screen.fill((0,0,0))
        holdArr.append((letter, calcBrightness(letter, screen)))
    bArr = np.array(holdArr, dtype=dtype)
    bArr = np.sort(bArr, order="brightness")
    retStr = ''
    for tup in bArr:
        retStr += tup[0].decode("utf-8")
    return retStr