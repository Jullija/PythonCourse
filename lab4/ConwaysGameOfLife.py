import pygame
import random
from copy import deepcopy
import threading 

CELL = 30
FPS = 6
HEIGHT = 700
WIDTH = 1000

W = WIDTH//CELL
H = HEIGHT//CELL


pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background = [[0 for i in range (W)] for j in range (H)]
foreground = [[0 for i in range (W)] for j in range (H)]

for i in range (W):
    for j in range (H):
        foreground[j][i] = random.randint(0, 1)


def checkCell(foreground, background, x, y):
    count = 0
    for j in range (y-1, y+2):
        for i in range (x-1, x+2):
            if foreground[j][i]:
                count += 1

    if foreground[y][x]:
        count -= 1
        if count == 2 or count == 3:
            background[y][x] = 1
        else:
            background[y][x] = 0
    else:
        if count == 3:
            background[y][x] = 1
        else:
            background[y][x] = 0


while True:
    surface.fill(pygame.Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    
    [pygame.draw.line(surface, pygame.Color('pink'), (x, 0), (x,HEIGHT)) for x in range (0, WIDTH, CELL)]
    [pygame.draw.line(surface, pygame.Color('pink'), (0, y), (WIDTH,y)) for y in range (0, HEIGHT, CELL)]

    threads = [] 

    for x in range (1, W-1):
        for y in range (1, H-1):
            if foreground[y][x]:
                pygame.draw.rect(surface, pygame.Color('violet'), (x * CELL + 2, y * CELL + 2, CELL - 2, CELL - 2))
            
            #thread
            t = threading.Thread(target=checkCell, args=[foreground, background, x, y])
            threads.append(t) 
            t.start()

    for thread in threads: 
        thread.join() 

    foreground = deepcopy(background)
    pygame.display.flip()
    clock.tick(FPS)
