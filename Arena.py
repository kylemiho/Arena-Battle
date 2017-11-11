import sys, pygame
import time
import Audio, Event

#pygame initializations
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('1v1 Arena Battle')



#game loop
Event.gameInit()
while 1:

    clock.tick(60)
    Event.gameLoop()
    #quit condition
    


