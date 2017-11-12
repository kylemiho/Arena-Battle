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

FPS = 30
tick = 0
rectX = 0        #location of x in rect
rectY = 1        #location of y in rect
rectWidth = 2    #location of width in rect
rectHeight = 3   #location of height in rect
characterMoveSpeed = 200
characterJumpStrength = 800
baseResoHeight = 800 #dont touch, used for sprite rendering
globSpriteLoc = ['SPRITE\INJA\Idle*','SPRITE\INJA\Run*','SPRITE\INJA\Jump__*'] #locations for files

class Character(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call sprite initialization

        #area of map
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        self.size = 0.20               #sprite size
        self.position = [0.0,0.0]
        self.velocity = [0.0,0.0]          #sprite speed
        self.accel = [0.0,0.0]
        self.inAir = True
        self.currentAnimation = 'idle'
        self.currentDirection = 'right'

        #animation stuff
        self.anim_pos = 0  #ranger marker for animation frame
        self.currentStep = 0 #current step for character in frame

        #load animations
        self.idleSurfaces = self.loadAnimations(0)
        self.walkingSurfaces = self.loadAnimations(1)
        self.jumpSurfaces = self.loadAnimations(2)

        self.anim_max = len(self.idleSurfaces) -1    #max animation frames
        self.image = self.idleSurfaces[0]            #load default sprite animation
        self.rect = self.image.get_rect()            #boundaries of sprite

        #update surface sizes
        self.idleSurfaces = self.updateSize(self.idleSurfaces)
        self.walkingSurfaces = self.updateSize(self.walkingSurfaces)
        self.jumpSurfaces = self.updateSize(self.jumpSurfaces)
        self.rect = self.idleSurfaces[0].get_rect() #update rect to new size


    def update(self,events):

        self.updateAnimationFrame() #update animation frame

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.velocity[0] = characterMoveSpeed
                    if self.inAir == False:
                        self.changeAnimation("walking")
                    self.changeDirection("right")
                if event.key == pygame.K_LEFT:
                    self.velocity[0] = -characterMoveSpeed
                    if self.inAir == False:
                        self.changeAnimation("walking")
                    self.changeDirection("left")
                elif event.key == pygame.K_SPACE:
                    self.velocity[1] = -characterJumpStrength
                    self.changeAnimation("jump")
                    self.inAir = True
                    print('Jump')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.currentDirection == "right":
                    self.velocity[0] = 0
                    if self.inAir == False:
                        self.changeAnimation("idle")
                if event.key == pygame.K_LEFT and self.currentDirection == "left":
                    self.velocity[0] = 0
                    if self.inAir == False:
                        self.changeAnimation("idle")
        #update physics
        self.updatePhysics()
        #update sprite rect based off of velocity
        self.rect[rectX] += int(self.velocity[rectX]/FPS)
        self.rect[rectY] += int(self.velocity[rectY]/FPS)
        #update image based off of current animation
        if self.currentAnimation == "walking":
            self.image = self.walkingSurfaces[self.anim_pos]
        elif self.currentAnimation == "idle":
            self.image = self.idleSurfaces[self.anim_pos]
        elif self.currentAnimation == "jump":
            self.image = self.jumpSurfaces[self.anim_pos]

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

    def touchingGround(self):
        if self.velocity[1] < 0: #if moving up, skip check
            return False
        screen = pygame.display.get_surface()
        screenRect = screen.get_rect()
        bottomY = screenRect[rectHeight]
        if self.rect[rectY]+self.rect[rectHeight] >= bottomY:
         #   print(self.rect[rectY],'+',self.rect[rectHeight],'>',bottomY)
            self.rect[rectY]=bottomY-self.rect[rectHeight]
            self.resetGravity()
            self.inAir = False
            #update animation depending on movement
            if self.velocity[0] == 0:
                self.changeAnimation("idle")
            else:
                self.changeAnimation("walking")
            return True
        return False

    def applyGravity(self):
        self.accel[1] = 45.0
        return
    def resetGravity(self):
        self.accel[1] = 0.0
        self.velocity[1] = 0.0
        return
    def updateVelocity(self):
        self.velocity[0] += self.accel[0]
        self.velocity[1] += self.accel[1]
        #print(self.velocity[1])
        return

    def updatePhysics(self):
        if not self.touchingGround():
            self.applyGravity()
        self.updateVelocity()
        return

def spawnPlayer1(characterName):
    return Character()