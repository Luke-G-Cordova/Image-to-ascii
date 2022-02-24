import sys
import pygame
import pygame.camera
from pygame.locals import *
from brightness import sortByBrightness

pygame.init()
pygame.camera.init()

# move this to the top to exit the program before
# carying out other computations if no camera is found
camlist = pygame.camera.list_cameras()
if not camlist:
    print('no camera found')
    sys.exit()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_width(), screen.get_height()

# instantiating the used asciii characters and sorting them based on brightness
# ascii = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{[]?-_+~<>i!lI^;,":`. '
ascii = 'MDON+ov-:/.`    '
ascii = sortByBrightness(ascii, screen)

# setting initial values of some global variables
pixelSize = 10
sizeWhole = int((width * height) / pixelSize)
colors = black, white, green = (0, 0, 0), (255, 255, 255), (0, 255, 26)
font = pygame.font.SysFont(None, pixelSize)
offset = .5
grow = False
shrink = False

# initializing the camera
cam = pygame.camera.Camera(camlist[0], size)
cam.start()
image = cam.get_image()

# resetting the screen to the needed size based off of the offset of each character
screen = pygame.display.set_mode((width * offset, height * offset))

# myMap maps a number s in range a1-a2 to a range b1-b2
def myMap(s, a1, a2, b1, b2):
    ans = s-a1
    ans *= b2-b1

    ans /= a2-a1
    return ans + b1

# main loop
while 1:
    for event in pygame.event.get():
        # handle exiting the program
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:sys.exit()

            # handle key inputs for growing and shrinking characters
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
                
    # handle growing and shrinking characters depending on keyboard inputs
    if grow and pixelSize < 150:
        pixelSize += 1
        sizeWhole = int((width * height) / pixelSize)
        font = pygame.font.SysFont(None, pixelSize)
    elif shrink and pixelSize > 10:
        pixelSize -= 1
        sizeWhole = int((width * height) / pixelSize)
        font = pygame.font.SysFont(None, pixelSize)

    # get a new image from the camera
    if cam.query_image():
        image = cam.get_image(image)

    # fill the screen black
    screen.fill(black)
    
    # add characters based on brightness of every pixelSize pixel in image
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
                # this try except is for some testing procedures
                # for some reason on different devices pygame will create
                # a bigger display box than needed causing the program
                # to error when there it goes outside the images pixels
                1
                # print(x, y)

    pygame.display.flip()

