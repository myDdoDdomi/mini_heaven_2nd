import pygame
import sys
import random
import time
from functions import coord, environ, shot, calculation
from classes import Player

WHITE = (255, 255, 255)
RED = (255, 10, 10)
BLACK = (0, 0, 0)
display_width = 912
display_height = 768

cannon_body = pygame.image.load("./img/cannon-3.png")
cannon_wheel = pygame.image.load("./img/cannon-1.png") # 24
wheel = [100,300]
body = [124, 324]

player = Player(wheel, 1)

def mainmenu():
    pygame.init()
    
    font = pygame.font.Font(None, 80)
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("대포 움직이기")
    clock = pygame.time.Clock()
    menu = True
    angle = 0
    space = 0
    gauge = 0
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] :
            space += 5
            if space >= 100 :
                space = 100
        else :
            gauge = space
            if gauge != 0 :
                shot(gauge,angle)
            space = 0
        if keys[pygame.K_UP] and angle <= 90:
            angle += 1
        elif keys[pygame.K_DOWN] and angle >= 0:
            angle -= 1
        if keys[pygame.K_RIGHT]:
            wheel[0] += 1
            body[0] += 1
            player.move(1, 0)
        elif keys[pygame.K_LEFT] :
            wheel[0] -= 1
            body[0] -= 1
            player.move(-1, 0)

        txt = font.render(str(space),True, BLACK)
        rotated_image = pygame.transform.rotate(cannon_body, angle)
        new_rect = rotated_image.get_rect(center=cannon_body.get_rect(center=body).center)
        gameDisplay.fill(WHITE)
        gameDisplay.blit(rotated_image, new_rect)
        gameDisplay.blit(cannon_wheel,wheel)
        pygame.draw.rect(gameDisplay, RED, [body[0]-35, 200, space, 10])
        gameDisplay.blit(txt,(0,0))
        pygame.display.update()
        clock.tick(20)
        
        
if __name__ == "__main__":
    mainmenu()
    




