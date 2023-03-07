import sys
import pygame
import pygame.camera
import json
from pygame.locals import *
from brightness import * #sortByBrightness

pygame.init()
pygame.camera.init()

camlist = pygame.camera.list_cameras()
if not camlist:
    print('no camera found')
    sys.exit()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_width(), screen.get_height()

# initializing the camera
cam = pygame.camera.Camera(camlist[0], size)
cam.start()

# instantiating the used asciii characters and sorting them based on brightness
# ascii = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{[]?-_+~<>i!lI^;,":`.       '
ascii = 'MDON+ov-:/.`    '
# ascii = '    `./:-vo+NODM'
ascii = sortByBrightness(ascii, screen)

print(ascii)

# setting initial values of some global variables
pixelSize = 20
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.SysFont(None, pixelSize)
offset = .6 
grow = False
shrink = False

# resetting the screen to the needed size based off of the offset of each character
if offset != 1:
    width = int(width * offset)
    height = int(width * offset)
    # size = width, height
    screen = pygame.display.set_mode((width, height))
    
image = cam.get_image()

video = []
def kill():
    f = open('video.json', 'w')
    f.write(json.dumps(video))
    f.close()
    sys.exit()

# main loop
while 1:
    for event in pygame.event.get():
        # handle exiting the program
        if event.type == pygame.QUIT: kill()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:kill()
                
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
    # get a new image from the camera
    if cam.query_image():
        image = cam.get_image(image)

    if grow and pixelSize < 150:
        pixelSize += 1
        font = pygame.font.SysFont(None, pixelSize)
    elif shrink and pixelSize > 10:
        pixelSize -= 1
        font = pygame.font.SysFont(None, pixelSize)


    # fill the screen black
    screen.fill(black)
    
    frameData = []
    # add characters based on brightness of every pixelSize pixel in image
    for x in range(0, width, pixelSize):
        frameData.append([])
        for y in range(0, height, pixelSize):
            r, g, b, a = image.get_at((x, y))
            bness = 0
            bness += r + g + b
            bness /= 3
            frameData[len(frameData)-1].append(bness)
            character = ascii[int(myMap(bness, 0, 256, 0, len(ascii)))] #len(ascii) - 1 - 

            letter = font.render(character, True, white)

            # letter = font.render(character, True, white)
            screen.blit(letter, (x*offset, y*offset))

    video.append(frameData)

    pygame.display.flip()

