import pygame
import os.path

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
 
def mainMenu():
    pygame.mixer.music.load('MUSIC\MAINMENU.wav')
    pygame.mixer.music.play(-1, 0.0)
    
def tavernMusic():
    pygame.mixer.music.load('MUSIC\Tavern.ogg')
    pygame.mixer.music.play(-1, 0.0)
    
#loads sound file and returns sound object
def loadSound(fileName):
    fileName = os.path.join('SFX',fileName)
    try:
        sound = pygame.mixer.Sound(file=fileName)
        return sound
    except pygame.error:
        print('Warning, could not load SFX file: \'', fileName,'\'',sep='')

#given a mixer.Sound object, play it once
def playSound(soundVariable):
    soundVariable.play()
    return
        
