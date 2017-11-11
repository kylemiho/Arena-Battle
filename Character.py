import pygame, os.path, glob

pygame.init()


def loadSpriteImage(name):
    #fullName = os.path.join('SPRITE',name) #fixes pathway to file
    try:
        image = pygame.image.load(name) #attempts to load
    except:
        print('Image load failed:',name)
        raise SystemExit
   # image = image.convert() #creates faster blitting
    image = image.convert_alpha()
    return image #returns surface 

#ninja initializer each char is different enough to get 
#a different class
baseResoHeight = 800 #dont touch, used for sprite rendering
globSpriteLoc = ['SPRITE\INJA\Idle*','SPRITE\INJA\Run*'] #locations for files

class Ninja(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call sprite initialization
        #self.image,self.rect = loadSpriteImage('NINJA\Idle__000.png')#default animation
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() #area of map
        self.size = 0.24 #image size scaled from screen size height
        
        #animation stuff
        self.animIdle = glob.glob(globSpriteLoc[0])
        self.animIdle.sort() #sort animations correctly
        self.anim_pos = 0  #setting range
        self.currentStep = 0
        self.AniUpdate = 3
       
        self.anim_max = len(self.animIdle) -1    #max animation frames
        self.image = loadSpriteImage(self.animIdle[0])   #load default sprite animation
        self.rect = self.image.get_rect()
        self.idleSurfaces = self.loadAnimations(self.animIdle)
        #print(self.idleSurfaces)
        
        #update idle surface sizes
        for i in range(len(self.idleSurfaces)):
            self.idleSurfaces[i] = self.updateSize(self.idleSurfaces[i])
        self.rect = self.idleSurfaces[0].get_rect()
        #update walking surfaces TODO
        
    def update(self):
        #update current self.rect based on mouse
        positionM = pygame.mouse.get_pos()
        self.rect.center = positionM
        
        #update animation
        self.currentStep += 1
        if self.currentStep >= 5:
            self.currentStep = 0
            #update animation state
            if self.anim_pos >= self.anim_max:
                self.anim_pos = 0
            else:
                self.anim_pos += 1
            #print('Updated Frame:',self.anim_pos)
        #self.image,self.rect = loadSpriteImage(self.animIdle[self.anim_pos])
        self.image = self.idleSurfaces[self.anim_pos]
        #print('Sprite Size:',self.rect)
        
        
        return 
    
    def updateSize(self,spriteResize): #update size of current surface image
        spriteResize = pygame.transform.smoothscale(spriteResize,\
            (int(spriteResize.get_rect()[2]*self.size*self.area[3]/600),\
             int(spriteResize.get_rect()[3]*self.size*self.area[3]/600)))
        return spriteResize
    
    def loadAnimations(self,arrayFilePaths): #return surface object array from array of filepaths
        return [loadSpriteImage(self.animIdle[i]) for i in range(len(arrayFilePaths))]
        
    
def spawnPlayer1(characterName):
    return Ninja()