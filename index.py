import sys, math
import pygame
import pygame.camera
from pygame.locals import *
from brightness import sortByBrightness

pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# ascii = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{[]?-_+~<>i!lI^;,":`. '
# ascii = '1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,./<>?;:"[]\|()*&^%$#@!-=_+`~ '
# ascii = '.mM /-w'
ascii = 'MDON+ov-:/.`    '
# ascii = '    `./:-vo+NODM'
# ascii = '@#o-. '
# ascii = '\u2593\u00D8\u00B0\u00B7 '
ascii = sortByBrightness(ascii, screen)
size = width, height = screen.get_width(), screen.get_height()
pixelSize = 10
sizeWhole = int((width * height) / pixelSize)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 26)
font = pygame.font.SysFont(None, pixelSize)
offset = .5
camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0], size)
    cam.start()
    image = cam.get_image()

screen = pygame.display.set_mode((width * offset, height * offset))

def myMap(s, a1, a2, b1, b2):
    ans = s-a1
    ans *= b2-b1

    ans /= a2-a1
    return ans + b1

grow = False
shrink = False
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:sys.exit()
            if event.key == pygame.K_LEFT:
                shrink = True
                grow = False
            if event.key == pygame.K_RIGHT:
                shrink = False
                grow = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                shrink = False
            elif event.key == pygame.K_RIGHT:
                grow = False
                

    if grow and pixelSize < 150:
        pixelSize += 1
        sizeWhole = int((width * height) / pixelSize)
        font = pygame.font.SysFont(None, pixelSize)
    elif shrink and pixelSize > 10:
        pixelSize -= 1
        sizeWhole = int((width * height) / pixelSize)
        font = pygame.font.SysFont(None, pixelSize)


    if cam.query_image():
        image = cam.get_image(image)

        
    screen.fill(black)
    
    for x in range(0, width, pixelSize):
        for y in range(0, height, pixelSize):
            try:
                r, g, b, a = image.get_at((x, y))
                r += g + b
                r /= 3
                character = ascii[int(myMap(r, 0, 256, 0, len(ascii)))] #len(ascii) - 1 - 
                letter = font.render(character, True, green)
                screen.blit(letter, (x*offset, y*offset))
            except:
                1
                # print(x, y)

    pygame.display.flip()

