import pygame
import pygame.display

from TicTacToeRect import ticTacToeRect
from menuButton import MenuButton

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Fonts/font.ttf", size)

def unOccupied(rects,pos,playerX): #returns the spot that was clicked as a tuple with (row,col,whether the spot is unoccupied)
   for i in range(0,3):
      for j in range(0,3):
         if(rects[i][j].collided(pos)):
            if(rects[i][j].symbol == ""):
               rects[i][j].symbol = ("X" if(playerX) else "O")
               return (i,j,True)
            else:
               return (i,j,False)
            
def minimax(rects,playerX): #the algorithm the cpu will use to choose it's move, the CPU will always be O
    if(playerX): #our base case for player X
        if(checkWin(rects,playerX)):
            return (0,0,-1,0)
        elif(checkWin(rects,not(playerX))):
            return (0,0,1,0)
        
    if(not(playerX)): #our base case for player O
        if(checkWin(rects,not(playerX))):
            return (0,0,-1,0)
        elif(checkWin(rects,playerX)):
            return (0,0,1,0)
    
    if(tie(rects)): #our base case for player O or X
        return (0,0,0,0)
    
    bestRow = 0
    bestCol = 0
    bestScore = -234567975642 if not(playerX) else 234567975642
    minMoves = 234567975642 #if two outcomes give the best score we always want to take the outcome that used the least number of moves

    for row in range(0,3): #go through all of the potentail moves see what states that leads to and pick the best move based on the score recieved
        for col in range(0,3):
            if(rects[row][col].symbol == ""):
                rects[row][col].symbol = "X" if playerX else "O"
                (someRow,someCol,score,currMinMoves) = minimax(rects,not(playerX))

                if(not(playerX)): #player 0 (the CPU) will always bee the maximizer, maximizer is a concept in the minimax algorithm
                    if(score > bestScore):
                        bestScore = score
                        bestRow = row
                        bestCol = col
                        minMoves = currMinMoves
                    elif(score == bestScore and currMinMoves < minMoves):
                        bestRow = row
                        bestCol = col
                        minMoves = currMinMoves
                else:
                    if(score < bestScore):
                        bestScore = score
                        bestRow = row
                        bestCol = col
                        minMoves = currMinMoves
                    elif(score == bestScore and currMinMoves < minMoves):
                        bestRow = row
                        bestCol = col
                        minMoves = currMinMoves

                rects[row][col].symbol = ""

    return (bestRow,bestCol,bestScore,minMoves+1)
            
def checkWin(rects,playerX):
   symbol = "X" if(playerX) else "O"
   return (checkVertWin(rects,symbol) or checkHorizontalWin(rects,symbol) or checkDiagWin(rects,symbol))

def checkVertWin(rects,symbol): 
    for col in range(0,3):
        if(rects[0][col].symbol == symbol and rects[1][col].symbol == symbol and rects[2][col].symbol == symbol):
            return True
        
    return False

def checkHorizontalWin(rects,symbol): 
    for row in range(0,3):
        if(rects[row][0].symbol == symbol and rects[row][1].symbol == symbol and rects[row][2].symbol == symbol):
            return True
      
    return False

def checkDiagWin(rects,symbol):
   return ((rects[0][0].symbol == symbol) and (rects[1][1].symbol == symbol) and (rects[2][2].symbol == symbol)) or ((rects[0][2].symbol == symbol) and (rects[1][1].symbol == symbol) and (rects[2][0].symbol == symbol))
   
def tie(rects):
    for i in range(0,3):
        for j in range(0,3):
            if(rects[i][j].symbol == ""):
                return False
            
    return True

def displayWin(playerX,screen):
    BG = pygame.image.load("Images/Background.png")
    screen.blit(BG, (0, 0))
    menuText = get_font(90).render("X wins", True, "#b68f40") if(playerX) else get_font(90).render("O wins", True, "#b68f40")
    menuRect = menuText.get_rect(center=(300, 70))
    screen.blit(menuText, menuRect)
    BACK_TO_MAIN_BUTTON.update(screen)
    yaySound.play()

def displayTie(screen):
    BG = pygame.image.load("Images/Background.png")
    screen.blit(BG, (0, 0))
    youGuysText = get_font(45).render("you guys are", True, "#b68f40")
    screen.blit(youGuysText, (5,0))
    bothLosersText = get_font(45).render("both losers", True, "#b68f40")
    screen.blit(bothLosersText, (5,60))
    BACK_TO_MAIN_BUTTON.update(screen)
    wahwahWahSound.play()

def displayInstructions(screen):
    BG = pygame.image.load("Images/Instructions.png")
    screen.blit(BG, (10, 10))

    run = True

    while run: #this is the game loop ensuring the display stays until x is clicked

        mouse_pos = pygame.mouse.get_pos()

        BACK_FROM_INSTRUCTIONS_BUTTON.changeColor(mouse_pos) #if a player hovers over the play button let's change it's colour
        BACK_FROM_INSTRUCTIONS_BUTTON.update(screen) #once we change the colour of the button let's display it

        for event in pygame.event.get(): #this is the event listener checking to see what has happened
            if event.type == pygame.QUIT: #checking if someone clicked x or they clicked on one of the rectangles
                run = False                 #in this case the person clicked x
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_FROM_INSTRUCTIONS_BUTTON.checkForInput(mouse_pos): #checking if someone clicked the play button
                    menu()

        pygame.display.update()

    pygame.quit()

def finished(rects,playerX,screen): #check if a player won or a tie happened
    if(checkWin(rects,playerX)):
        displayWin(playerX,screen)
        return True
    elif(tie(rects)):
        displayTie(screen)
        return True
    
    return False

def play(screen,cpuPlayer):
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

                if event.type == pygame.MOUSEBUTTONDOWN: #if someone clicks the BACK_TO_MAIN_BUTTON go back to the menu
                    if BACK_TO_MAIN_BUTTON.checkForInput(pos):
                        reInitialize(myRects)
                        menu()
            
            if ((event.type == pygame.MOUSEBUTTONDOWN) and (not(gameOver))): #in this case the person clicked on one of the rectangles
                (row,col,not_occupied) = unOccupied(myRects,pos,playerX) #finding out if the rectangle they clicked is unoccupied

                if(not_occupied): #we need to check if a spot is occupied that way we can notify the player and it will still be the current player's turn
                    myRects[row][col].drawXorO(screen, playerX)

                    gameOver = finished(myRects,playerX,screen)

                    if(cpuPlayer and not(gameOver)): #if there is only one player every player turn the computer has to do a move too
                        global theCount
                        theCount += 1
                        (row,col,score,numMoves) = minimax(myRects,False)
                        myRects[row][col].symbol = "O"

                        myRects[row][col].drawXorO(screen, False)

                        gameOver = finished(myRects,False,screen)
                    else: #there are two players so switch the player turn
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

    menuText = get_font(50).render("TIC TAC TOE", True, "#b68f40")
    menuRect = menuText.get_rect(center=(300, 70))

    screen.blit(menuText, menuRect)
    run = True

    while run: #this is the game loop ensuring the display stays until x is clicked

        mouse_pos = pygame.mouse.get_pos()

        TWO_PLAYER_BUTTON.changeColor(mouse_pos) #if a player hovers over the play button let's change it's colour
        TWO_PLAYER_BUTTON.update(screen) #once we change the colour of the button let's display it

        ONE_PLAYER_BUTTON.changeColor(mouse_pos) #if a player hovers over the play button let's change it's colour
        ONE_PLAYER_BUTTON.update(screen) #once we change the colour of the button let's display it

        INSTRUCTIONS_BUTTON.changeColor(mouse_pos) #if a player hovers over the play button let's change it's colour
        INSTRUCTIONS_BUTTON.update(screen) #once we change the colour of the button let's display it

        for event in pygame.event.get(): #this is the event listener checking to see what has happened
            if event.type == pygame.QUIT: #checking if someone clicked x or they clicked on one of the rectangles
                run = False                 #in this case the person clicked x
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TWO_PLAYER_BUTTON.checkForInput(mouse_pos): #checking if someone clicked the play button
                    play(screen,False)
                if ONE_PLAYER_BUTTON.checkForInput(mouse_pos): #checking if someone clicked the two player button
                    play(screen,True) #if we have one player we will be using the cpu as the second player
                if INSTRUCTIONS_BUTTON.checkForInput(mouse_pos): #checking if some confused person clicked on instructions
                    displayInstructions(screen) 

        pygame.display.update()

    pygame.quit()

pygame.init()
pygame.display.init()

#window needs dimensions width and height, you can change this but both should be a multiple of 3 and they have to have the same value
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#loading sounds that we will use later
occupiedSpotSound = pygame.mixer.Sound("soundEffects/occupied.mp3")
yaySound = pygame.mixer.Sound("soundEffects/yay.mp3")
wahwahWahSound = pygame.mixer.Sound("soundEffects/wahWahWah.mp3")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tic tac toe") 

BG = pygame.image.load("Images/Background.png") #background image for the menu and for win and tie screens

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
BACK_TO_MAIN_BUTTON = MenuButton(image=pygame.image.load("Images/Play Rect.png"), pos=(300, 500),
                         text_input="MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

#This button will be used in the main menu
TWO_PLAYER_BUTTON = MenuButton(image=pygame.image.load("Images/Play Rect.png"), pos=(300, 200), 
                         text_input="TWO PLAYER", font=get_font(36), base_color="#d7fcd4", hovering_color="White")

#This button will also be used in the main menu
ONE_PLAYER_BUTTON = MenuButton(image=pygame.image.load("Images/Play Rect.png"), pos=(300, 350), 
                         text_input="ONE PLAYER", font=get_font(36), base_color="#d7fcd4", hovering_color="White")

#This button will also be used in the main menu, for the confused people
INSTRUCTIONS_BUTTON = MenuButton(image=pygame.image.load("Images/Play Rect.png"), pos=(300, 500), 
                         text_input="INSTRUCTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

#This button will be displayed in the instructions page it will be used to go back to the main menu
BACK_FROM_INSTRUCTIONS_BUTTON = MenuButton(image=pygame.image.load("Images/back to main instructions.png"), pos=(110, 40), 
                         text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")


theCount = 0

menu()

