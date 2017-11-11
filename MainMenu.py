import pygame

#initializes fonts to be used
pygame.init()
pygame.font.init()

#given a text to print, return a surface object to be blitted to screen
def mainMenuText(bolded,text,resolution):
    #font size designed off of 720 width, so will rescale
    additionalSize = 10*(resolution[0]/720)
    defaultFontSize = 35*(resolution[0]/720)
    finalSize = defaultFontSize + (additionalSize if bolded else 0)
    #initializes font, adds additionalSize if bolded is true
    menuFont = pygame.font.SysFont('Comic Sans MS',int(finalSize))
    #create surfaces / render
    fontSurface1 = menuFont.render(text,False,(255,255,255))
    return fontSurface1
    
    
#load main menu background, return a surface of given resolution
def loadMainMenuBG(resolution):
    mainMenuImage = pygame.image.load('BG\MainMenu.png')
    return pygame.transform.smoothscale(mainMenuImage,resolution)
