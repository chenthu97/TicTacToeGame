from menuButton import MenuButton
from TicTacToe import play

import pygame
import pygame.display

pygame.init()
pygame.display.init()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

#window needs dimensions width and height, you can change this but both should be a multiple of 3 and they have to have the same value
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tic tac toe") 

BG = pygame.image.load("Background.png")

screen.blit(BG, (0, 0))

menuText = get_font(100).render("MAIN MENU", True, "#b68f40")
menuRect = menuText.get_rect(center=(60, 70))
#try displaying at 9,48

screen.blit(menuText, menuRect)

PLAY_BUTTON = MenuButton(image=pygame.image.load("Play Rect.png"), pos=(300, 200), 
                         text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

run = True

while run: #this is the game loop ensuring the display stays until x is clicked

    mouse_pos = pygame.mouse.get_pos()

    PLAY_BUTTON.changeColor(mouse_pos)
    PLAY_BUTTON.update(screen)
    
    for event in pygame.event.get(): #this is the event listener checking to see what has happened
        if event.type == pygame.QUIT: #checking if someone clicked x or they clicked on one of the rectangles
            run = False                 #in this case the person clicked x
        if event.type == pygame.MOUSEMOTION:
            print(pygame.mouse.get_pos())
            print("type of mouse position is " + str(type(pygame.mouse.get_pos())) + " \n")
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(mouse_pos):
                play(screen)

    pygame.display.update()

pygame.quit()









