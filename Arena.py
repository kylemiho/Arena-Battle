import sys, pygame
import time
import Audio, Event

#pygame initializations
FPS = 30

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('1v1 Arena Battle')

Event.gameInit()
while 1:
    clock.tick(FPS)
    Event.gameLoop()
    #quit condition
    


