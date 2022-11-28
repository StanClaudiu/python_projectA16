import pygame 
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

sky_surface = pygame.image.load("ChessPieces/wQ.png")

test_font = pygame.font.Font(None,50)

text_surface = test_font.render("U LOST",False,'Green')

player_surf = pygame.image.load("ChessPieces/wB.png").convert_alpha()
player_rect = player_surf.get_rect(topleft = (80,200))

aux = 0
while True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            pygame.quit()
            exit()
    screen.blit(sky_surface,(200,100)) # put the surface there
    screen.blit(text_surface,(300 + aux,50))
    screen.blit(player_surf,player_rect)
    pygame.draw.rect(screen,'Blue',pygame.Rect(50,100,100,200))
    aux = aux + 1
    pygame.display.update() 
    clock.tick(60) # not faster than 60 whiles per sec, nu ai hit pe mine mai mare de 60 de ori per sec
