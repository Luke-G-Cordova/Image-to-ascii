import sys, math
import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# ascii = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{[]?-_+~<>i!lI;:,"^`. '
# ascii = 'MNDO+ov-:/.`    '
ascii = 'MO.   '
size = width, height = screen.get_width(), screen.get_height()
pixelSize = 10
sizeWhole = int((width * height) / pixelSize)
black = (0,0,0)
white = (255, 255, 255)
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

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:sys.exit()

    if cam.query_image():
        image = cam.get_image(image)

        
    screen.fill(black)
    
    for x in range(0, width, pixelSize):
        for y in range(0, height, pixelSize):
            try:
                r, g, b, a = image.get_at((x, y))
                r += g + b
                r /= 3
                character = ascii[len(ascii) - 1 - int(myMap(r, 0, 256, 0, len(ascii)))]
                letter = font.render(character, True, white)
                screen.blit(letter, (x*offset, y*offset))
            except:
                1
                # print(x, y)

    pygame.display.flip()

