import pygame, Audio, MainMenu,sys, Fight, Character, Physics
 
#state (default is starting main menu)
#state options: mainmenu, fight
state = 'mainmenu'

#screen initializations
resolution = width,height = 720,480
black = 0,0,0
screen = pygame.display.set_mode(resolution)

#BG IMAGE DEFAULT LOAD
mainMenuImage = pygame.image.load('BG\MainMenu.png')
mainMenuImage = pygame.transform.smoothscale(mainMenuImage,resolution)
mainMenuImage.convert()
stageImage = pygame.image.load('BG\Tavern.png')
stageImage.convert()

#SOUNDS LOAD
cursorSound = Audio.loadSound('Cursor.wav')
selectSound = Audio.loadSound('MenuSelect.wav')
backSound = Audio.loadSound('MenuBack.wav')

#current 'Cursor Location for main menu'
cursorMain = 0
#if up/down keypad is ready for input

#SPRITES
allsprites = pygame.sprite.Group()

#update cursor location for main menu
#num options is # of choices for the cursor in total for main menu
#also returns when ENTER/BACKSPACE is pressed(not held down) as needed for state updates for mainMenuLoop()
def updateMainCursor(numOptions):
    #ensures that keyReady/cursorMain isnt redefined in this function
    global cursorMain
    currentEvents = pygame.event.get()
    for event in currentEvents:
        #move cursor depending on key pressed
        if event.type == pygame.KEYDOWN:
            ##down
            if event.key == pygame.K_DOWN:
                cursorMain += 1
                print(cursorMain)
                Audio.playSound(cursorSound)
                
            #up
            elif event.key == pygame.K_UP:
                Audio.playSound(cursorSound)
                if cursorMain == 0:
                    cursorMain += int(numOptions - 1)    
                else:
                    cursorMain -= 1
                print(cursorMain)
                
            #enter
            elif event.key == pygame.K_RETURN:
                print('ENTER PRESSED')
                Audio.playSound(selectSound)
                return 'ENTER'
            
            #backspace
            elif event.key == pygame.K_BACKSPACE:
                print('BACKSPACE PRESSED')
                Audio.playSound(backSound)
                return 'BACKSPACE'


        #quit game if ESC is pressed    
        if event.type == pygame.QUIT or \
        (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            print('Exiting')
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    return ''

MainMainOptions = 3 #SINGLE,MULTI,OPTIONS

#main menu selection text
def blitTextMain1():
    
    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 0 else False,
                'Singleplayer',resolution),(resolution[0]/3,resolution[1]/4))
    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 1 else False,
                'Multiplayer',resolution),(resolution[0]/3,resolution[1]/2))
    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 2 else False,
                'Options',resolution),(resolution[0]/3,3*resolution[1]/4))
    return
#options text 
def blitTextOptions():
 
    screen.blit(MainMenu.mainMenuText(True,
                'Resoultion',resolution),(resolution[0]/3,resolution[1]/2))
    return
#resolution text
def blitResolutionOptions():

    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 0 else False,
                '720x480',resolution),(resolution[0]/3,resolution[1]/4))
    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 1 else False,
                    '1280x720',resolution),(resolution[0]/3,resolution[1]/2))
    screen.blit(MainMenu.mainMenuText(True if (cursorMain % 3) == 2 else False,
                '1366x768',resolution),(resolution[0]/3,3*resolution[1]/4))
    return

#resolution options
#720x480
#1280x720
#1920x1080
resolution1 = width,height = 720,480
resolution2 = width,height = 1280,720
resolution3 = width,height = 1366,768
def updateResolution(cursor):
    #set resolution/mainmenu surface to global to be edited
    global mainMenuImage
    global resolution
    if cursor == 0:
        resolution = resolution1
    elif cursor == 1:
        resolution = resolution2
    elif cursor == 2:
        resolution = resolution3
    screen = pygame.display.set_mode(resolution)
    mainMenuImage = MainMenu.loadMainMenuBG(resolution)
    print('New Resolution:',resolution)
    return

#current state of main menu to determine which screen should be popped up
mainMenuState = 'MainMain'

def mainMenuLoop():
    global mainMenuState
    global cursorMain
    global state
    #main menu background image
    screen.blit(mainMenuImage,(0,0))

    #return state of updateMainCursor
    returnState = ''

    #case MainMain
    if mainMenuState == 'MainMain':
        #updates cursor location, and checks for enter/backspaces pressed
        returnState = updateMainCursor(MainMainOptions)
        if returnState == 'ENTER' and (cursorMain % 3) == 2:
            cursorMain = 0
            mainMenuState = 'Options'
        elif returnState == 'ENTER' and (cursorMain % 3) == 0:
            #single player selected. start game
            fightInit()
            state = 'fight'
        blitTextMain1()
        
    #case Options
    elif mainMenuState == 'Options':
        #temporarily hardcoded
        returnState = updateMainCursor(1)
        if returnState == 'BACKSPACE':
            cursorMain = 0
            mainMenuState = 'MainMain'
        elif returnState == 'ENTER':
            cursorMain = 0
            mainMenuState = 'Resolution'
        blitTextOptions()
        
    #case Resolution
    elif mainMenuState == 'Resolution':
        #temporarily hardcoded
        returnState = updateMainCursor(3)
        if returnState == 'BACKSPACE':
            cursorMain = 0
            mainMenuState = 'Options'
        elif returnState == 'ENTER':
            #update resolution depending on chosen setting
            updateResolution(cursorMain % 3)
        blitResolutionOptions()

    return

def charSelectLoop():
    screen.blit(mainMenuImage,(0,0))
    
    #check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print('Exiting')
                pygame.display.quit()
                pygame.quit()
                sys.exit()
    return

def fightInit():
    global stageImage
    stageImage = Fight.loadStageBG(0,resolution) #load stageImage
    Audio.tavernMusic()

    #addsprites
    character1 = Character.spawnPlayer1('Ninja')
    allsprites.add(character1)

    return

def fightLoop():
    #BG Image
    screen.blit(stageImage,(0,0))
    
    #TODO check for Keybord input for interactions


    #check for quit
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print('Exiting')
                pygame.display.quit()
                pygame.quit()
                sys.exit()
    allsprites.update(events) #update sprites with events updated

    allsprites.draw(screen) #draw sprites to screen
    return
    
def gameInit():
    #play main menu music
    Audio.mainMenu()
    # mainMenuInit()
    return

def gameLoop():
    if state == 'mainmenu':
        mainMenuLoop()
    elif state == 'charselect':
        charSelectLoop()
    elif state == 'fight':
        fightLoop()
    #update background image as needed
    pygame.display.update()
    return
