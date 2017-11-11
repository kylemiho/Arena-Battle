import pygame

def loadStageBG(stageNum,resolution):
    stageImage = pygame.image.load('BG\Tavern.png')
    stageImage.convert()
    return pygame.transform.smoothscale(stageImage,resolution)