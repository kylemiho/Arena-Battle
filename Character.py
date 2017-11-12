import pygame, os.path, glob

pygame.init()


def loadSpriteImage(name):
    #fullName = os.path.join('SPRITE',name) #fixes pathway to file
    try:
        image = pygame.image.load(name) #attempts to load
    except:
        raise SystemExit
    image = image.convert_alpha() #faster blitting
    return image #returns surface 

#ninja initializer each char is different enough to get 
#a different class

rectX = 0        #location of x in rect
rectY = 1        #location of y in rect
rectWidth = 2    #location of width in rect
rectHeight = 3   #location of height in rect
characterMoveSpeed = 5
baseResoHeight = 800 #dont touch, used for sprite rendering
globSpriteLoc = ['SPRITE\INJA\Idle*','SPRITE\INJA\Run*'] #locations for files

class Character(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call sprite initialization

        #area of map
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.size = 0.20               #sprite size
        self.velocity = [0,0]          #sprite speed
        self.currentAnimation = 'idle'
        self.currentDirection = 'right'

        #animation stuff
        self.anim_pos = 0  #ranger marker for animation frame
        self.currentStep = 0 #current step for character in frame

        #load animations
        self.idleSurfaces = self.loadAnimations(0)
        self.walkingSurfaces = self.loadAnimations(1)

        self.anim_max = len(self.idleSurfaces) -1    #max animation frames
        self.image = self.idleSurfaces[0]            #load default sprite animation
        self.rect = self.image.get_rect()            #boundaries of sprite

        #update surface sizes
        self.idleSurfaces = self.updateSize(self.idleSurfaces)
        self.walkingSurfaces = self.updateSize(self.walkingSurfaces)
        self.rect = self.idleSurfaces[0].get_rect() #update rect to new size


    def update(self,events):

        self.updateAnimationFrame() #update animation frame

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.velocity = [characterMoveSpeed,0]
                    self.changeAnimation("walking")
                    self.changeDirection("right")
                if event.key == pygame.K_UP:
                    self.velocity = [0,-characterMoveSpeed]
                    self.changeAnimation("walking")
                if event.key == pygame.K_DOWN:
                    self.velocity = [0,characterMoveSpeed]
                    self.changeAnimation("walking")
                if event.key == pygame.K_LEFT:
                    self.velocity = [-characterMoveSpeed,0]
                    self.changeAnimation("walking")
                    self.changeDirection("left")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or pygame.K_LEFT\
                    or pygame.K_DOWN or pygame.K_UP:
                    self.velocity = [0,0]
                self.changeAnimation("idle")
        #update sprite rect based off of velocity
        self.rect[rectX] += self.velocity[rectX]
        self.rect[rectY] += self.velocity[rectY]
        #update image based off of current animation
        if self.currentAnimation == "walking":
            self.image = self.walkingSurfaces[self.anim_pos]
        elif self.currentAnimation == "idle":
            self.image = self.idleSurfaces[self.anim_pos]

        #flip image if direction is left
        if self.currentDirection == "left":
            self.image = pygame.transform.flip(self.image,True,False)
        
        return

    def changeAnimation(self,newAnim): #changes animation to new
        if self.currentAnimation == newAnim:
            return
        else:
            self.anim_pos = 0 #reset animation
            self.currentAnimation = newAnim
            return

    def changeDirection(self,newDirection):
        if self.currentDirection == newDirection:
            return
        else:
            self.anim_pos = 0
            self.currentDirection = newDirection
            return

    def updateAnimationFrame(self):
        #update animation
        self.currentStep += 1
        if self.currentStep >= 2:
            self.currentStep = 0
            #update animation state
            if self.anim_pos >= self.anim_max:
                self.anim_pos = 0
            else:
                self.anim_pos += 1
        return

    def updateSize(self,spriteResize): #update size of list of sprite surfaces
        constantMult = self.size * self.area[3] / 600 #constant created used to resize
        for i in range(0,len(spriteResize)):
            spriteResize[i] = pygame.transform.smoothscale(spriteResize[i],
            (int(constantMult*spriteResize[i].get_rect()[2]),
             int(constantMult * spriteResize[i].get_rect()[3])))
        return spriteResize
    
    def loadAnimations(self,index): #return surface object array based on globSpriteLoc index
        filePaths = glob.glob(globSpriteLoc[index]) #get filepaths
        filePaths.sort() #sort filepaths
        return [loadSpriteImage(filePaths[i]) for i in range(len(filePaths))]
        
    
def spawnPlayer1(characterName):
    return Character()