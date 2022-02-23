import sys, time
import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((500, 500))
black = (0,0,0)
white = (255,255,255)
font = pygame.font.SysFont(None, 20)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()

    time.sleep(1)
    screen.fill(black)
    letter = font.render('`', True, white)
    screen.blit(letter, (50, 50))
    avgB = 0
    for x in range(20):
        for y in range(20):
            px = screen.get_at((x+50, y+50))
            avg = px[0]+px[1]+px[2]
            avg /= 3
            avgB += avg
    avgB /= (20*20)
    print(avgB)
    pygame.display.flip()
