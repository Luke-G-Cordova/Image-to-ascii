import sys, time
import numpy as np
import pygame
from pygame.locals import *


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
def sortByBrightness(ascii, screen):
    dtype = [('character', 'S10'), ('brightness', float)]
    holdArr = []
    for letter in ascii:
        screen.fill((0,0,0))
        holdArr.append((letter, calcBrightness(letter, screen)))
    bArr = np.array(holdArr, dtype=dtype)
    bArr = np.sort(bArr, order="brightness")
    for tup in bArr:
        print(tup[0])
    return bArr

pygame.init()

screen = pygame.display.set_mode((500, 500))
black = (0,0,0)
white = (255,255,255)
font = pygame.font.SysFont(None, 20)
ascii = 'diso3-2;` '
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()

    time.sleep(1)
    screen.fill(black)
    print(sortByBrightness(ascii, screen))
    pygame.display.flip()
