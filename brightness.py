import numpy as np
import pygame
from pygame.locals import *

def myMap(s, a1, a2, b1, b2):
    ans = s-a1
    ans *= b2-b1

    ans /= a2-a1
    return ans + b1

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


def getVibrantColorFromBrightness(brightness):
    col = myMap(brightness, 0, 255, 0, 1529)
    if col >= 0 and col < 255:
        col -= 0
        return (255, 0, col)
    elif col >= 255 and col < 510:
        col -= 255
        return (255, col, 0)
    elif col >= 510 and col < 765:
        col -= 510
        return (col, 255, 0)
    elif col >= 765 and col < 1020:
        col -= 765
        return (0, 255, col)
    elif col >= 1020 and col < 1275:
        col -= 1020
        return (col, 0, 255)
    elif col >= 1275 and col < 1530:
        col -= 1275
        return (0, col, 255)
        