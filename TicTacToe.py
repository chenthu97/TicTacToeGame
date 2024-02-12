import pygame
import pygame.display
from TicTacToeRect import ticTacToeRect
from menuButton import MenuButton

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def unOccupied(rects,pos,playerX): #returns the spot that was clicked as a tuple with (row,col,whether the spot is unoccupied)
   for i in range(0,3):
      for j in range(0,3):
         if(rects[i][j].collided(pos)):
            if(rects[i][j].symbol == ""):
               rects[i][j].symbol = ("X" if(playerX) else "O")
               return (i,j,True)
            else:
               return (i,j,False)
            
def checkWin(rects,row,col,playerX):
   symbol = "X" if(playerX) else "O"
   return (checkVert(rects,col,symbol) or checkHorizontal(rects,row,symbol) or checkDiag(rects,symbol))

def checkVert(rects,col,symbol):
    for row in range(0,3):
        if(rects[row][col].symbol != symbol):
           return False
    
    return True

def checkHorizontal(rects,row,symbol):
    for col in range(0,3):
        if(rects[row][col].symbol != symbol):
           return False
      
    return True

def checkDiag(rects,symbol):
   return ((rects[0][0].symbol == symbol) and (rects[1][1].symbol == symbol) and (rects[2][2].symbol == symbol)) or ((rects[0][2].symbol == symbol) and (rects[1][1].symbol == symbol) and (rects[2][0].symbol == symbol))
   
def tie(rects):
    for i in range(0,3):
        for j in range(0,3):
            if(rects[i][j].symbol == ""):
                return False
            
    return True

def displayWin(playerX,screen):
    BG = pygame.image.load("Background.png")
    screen.blit(BG, (0, 0))
    menuText = get_font(90).render("X wins", True, "#b68f40") if(playerX) else get_font(90).render("O wins", True, "#b68f40")
    menuRect = menuText.get_rect(center=(300, 70))
    screen.blit(menuText, menuRect)
    BACK_TO_MAIN_BUTTON.update(screen)
    yaySound.play()

def displayTie(screen):
    BG = pygame.image.load("Background.png")
    screen.blit(BG, (0, 0))
    youGuysText = get_font(45).render("you guys are", True, "#b68f40")
    screen.blit(youGuysText, (5,0))
    bothLosersText = get_font(45).render("both losers", True, "#b68f40")
    screen.blit(bothLosersText, (5,60))
    BACK_TO_MAIN_BUTTON.update(screen)
    wahwahWahSound.play()

def play(screen):
    screen.fill("black")

    run = True #the variable used to track when the display should be kept and when to remove the display
    playerX = True #at the start of the game the player is x, when True mean's player x turn false mean's player o turn
    gameOver = False #used to track if a player has won or if there is a tie

    for i in range(3): #drawing the rectangles to the screen
        for j in range(3):
            pygame.draw.rect(screen, (255,255,255), myRects[i][j].rect, 3)

    while run: #this is the game loop ensuring the display stays until x is clicked or there is a winner or a tie

        pos=pygame.mouse.get_pos()

        for event in pygame.event.get(): #this is the event listener checking to see what has happened
            if event.type == pygame.QUIT: #checking if someone clicked x or they clicked on one of the rectangles
                run = False                 #in this case the person clicked x

            if(gameOver): #if someone won the game or a tie happened let's display the BACK_TO_MAIN_BUTTON
                BACK_TO_MAIN_BUTTON.changeColor(pos)
                BACK_TO_MAIN_BUTTON.update(screen)

                if event.type == pygame.MOUSEBUTTONDOWN: #if someone clickss the BACK_TO_MAIN_BUTTON go back to the menu
                    if BACK_TO_MAIN_BUTTON.checkForInput(pos):
                        reInitialize(myRects)
                        menu()
            
            if ((event.type == pygame.MOUSEBUTTONDOWN) and (not(gameOver))): #in this case the person clicked on one of the rectangles
                (row,col,not_occupied) = unOccupied(myRects,pos,playerX) #finding out if the rectangle they clicked is unoccupied

                if(not_occupied): #we need to check if a spot is occupied that way we can notify the player and it will still be the current player's turn
                    myRects[row][col].drawXorO(screen, playerX)

                    if(checkWin(myRects,row,col,playerX)):
                        gameOver = True
                        displayWin(playerX,screen)
                    elif(tie(myRects)):
                        gameOver = True
                        displayTie(screen)

                    playerX = not(playerX)
                else:
                    occupiedSpotSound.play()
            
            if((not(gameOver))):
                for i in range(0,3):
                    for j in range(0,3):
                        myRects[i][j].changeColor(pos, screen)

        pygame.display.update()

    pygame.quit()

def reInitialize(rects): #we need this menu each time we start a new game we are essentially clearing the board of all x's and o's
    for i in range(3):
        for j in range(3):
            rects[i][j].symbol = ""

def menu():
    screen.blit(BG, (0, 0))

    menuText = get_font(100).render("MAIN MENU", True, "#b68f40")
    menuRect = menuText.get_rect(center=(60, 70))

    screen.blit(menuText, menuRect)
    run = True

    while run: #this is the game loop ensuring the display stays until x is clicked

        mouse_pos = pygame.mouse.get_pos()

        PLAY_BUTTON.changeColor(mouse_pos) #if a player hovers over the play button let's change it's colour
        PLAY_BUTTON.update(screen) #once we change the colour of the button let's display it

        for event in pygame.event.get(): #this is the event listener checking to see what has happened
            if event.type == pygame.QUIT: #checking if someone clicked x or they clicked on one of the rectangles
                run = False                 #in this case the person clicked x
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos): #checking if someone clicked the play button
                    play(screen)

        pygame.display.update()

    pygame.quit()

pygame.init()
pygame.display.init()

#window needs dimensions width and height, you can change this but both should be a multiple of 3 and they have to have the same value
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#loading sounds that we will use later
occupiedSpotSound = pygame.mixer.Sound("occupied.mp3")
yaySound = pygame.mixer.Sound("yay.mp3")
wahwahWahSound = pygame.mixer.Sound("wahWahWah.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tic tac toe") 

BG = pygame.image.load("Background.png") #background image for the menu and for win and tie screens

x = 0
y = 0
rectWidth = SCREEN_WIDTH/3
rectHeight = SCREEN_HEIGHT/3

myRects = [[() for j in range(0,3)] for i in range(0,3)] #keeps track of the actual rectangles on the screen, this is useful in case a user clicks on one of the rectangless

for i in range(0,3): #this nested for loop is just to set up the rectangles, doing things like setting size and start position of each rectangle
    for j in range(0,3):
        myRects[i][j] = ticTacToeRect(x,y,rectWidth,rectHeight)
        x += rectWidth
    x = 0
    y += rectHeight

#This button will only be there once there is a winner or a tie, and is used to go back to the main menu
BACK_TO_MAIN_BUTTON = MenuButton(image=pygame.image.load("Play Rect.png"), pos=(300, 500),
                         text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

#This button will be used in the main menu
PLAY_BUTTON = MenuButton(image=pygame.image.load("Play Rect.png"), pos=(300, 200), 
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

menu()
