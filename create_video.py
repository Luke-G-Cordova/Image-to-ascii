import sys
import pygame
import pygame.camera
import json
import numpy as np
from pygame.locals import *
from brightness import * #sortByBrightness

pygame.init()
pygame.camera.init()

camlist = pygame.camera.list_cameras()
if not camlist:
  print('no camera found')
  sys.exit()
# initialize the camera
cam = pygame.camera.Camera(camlist[0])
cam.start()
camSize = cam.get_size()
print(camSize)
# make the screen the same size as the camera
screen = pygame.display.set_mode(( camSize[0]*2, camSize[1]*2 ), 0)

# take first image
image = cam.get_image()

if camSize[0] % 10 != 0 or camSize[1] % 10 != 0:
  print('camSize is not divisible by 10')
  print(camSize)
  sys.exit()

font = pygame.font.SysFont(None, 25)

ascii = 'Luke '#'MDN+o*-:.` '
ascii = sortByBrightness(ascii, screen)
print(ascii)


def myMap(s, a1, a2, b1, b2):
  ans = s-a1
  ans *= b2-b1
  ans /= a2-a1
  return ans + b1

def kill():
  # f = open('video.json', 'w')
  # f.write(json.dumps(video))
  # f.close()
  sys.exit()


def greyscale(surface: pygame.Surface):
  arr = pygame.surfarray.array3d(surface)
  mean_arr = np.mean(arr, axis=2)
  interp_arr = np.interp(mean_arr, (90, 255), (0, len(ascii)))
  interp_arr = np.rint(interp_arr)
  group = 255/len(ascii)
  interp_arr = interp_arr * group
  interp_arr3d = interp_arr[..., np.newaxis]
  new_arr = np.repeat(interp_arr3d[:, :, :], 3, axis=2)
  return pygame.surfarray.make_surface(new_arr)

# image = cam.get_image()
# while image.get_at((0, 0)) == (0, 0, 0):
#   image = cam.get_image()
# greyscale(image)
# sys.exit()

a = np.array([])

while 1:
  for event in pygame.event.get():
    # handle exiting the program
    if event.type == pygame.QUIT: kill()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:kill()
  
  if cam.query_image():
    image = cam.get_image()
    # show the original camera input on one side
    screen.blit(image, (0, 0))

    # show the image used for filtering brightnesses
    image = greyscale(image)
    screen.blit(image, (0, camSize[1]))
        
    # show the final image
    screen.fill((0, 0, 0), (camSize[0], 0, camSize[0]*2, camSize[1]))
    for x in range(0, camSize[0], 10):
      for y in range(0, camSize[1], 10):
        # get the pixel at the current x and y
        pixel = image.get_at((x, y))
        # get the brightness of the pixel
        brightness = pixel[0] + pixel[1] + pixel[2]
        brightness /= 3

        if brightness not in a:
          a = np.append(a, brightness)
          print("brightness: " , brightness, " : ", round(brightness/(255/(len(ascii)-1))))

        # get the letter that corresponds to the brightness level
        letter = font.render(ascii[round(brightness/(255/(len(ascii)-1)))], True, (255, 255, 255))

        # draw the letter on the screen
        screen.blit(letter, ( x+camSize[0], y ))
        





  pygame.display.flip()