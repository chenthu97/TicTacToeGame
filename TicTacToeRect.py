import pygame
import pygame.display

class ticTacToeRect():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.symbol = ""

    def collided(self,pos): #checking if the player clicked on the reectangle during the tic tac toe game
        return self.rect.collidepoint(pos)
    
    def changeColor(self, position, screen): #if the mouse hovers of the rectangle there will be a red highlight over the rectangle
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            pygame.draw.rect(screen, (255,0,0), self.rect, 3)
        else:
            pygame.draw.rect(screen, (255,255,255), self.rect, 3)

    def drawXorO(self, screen, playerX): #drawing the actual X or O onto the rectangle as specified
        font = pygame.font.SysFont("dejavusans",100)
        text = font.render("X",True,(255,0,0)) if(playerX) else font.render("O",True,(255,0,0))

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
