import pygame
import sys
import random
import time
from functions import coord, environ, calculation
from classes import Player

WHITE = (255, 255, 255)
RED = (255, 10, 10)
BLACK = (0, 0, 0)
display_width = 1280
display_height = 720

cannon_body = pygame.image.load("./img/cannon-3.png")
cannon_wheel = pygame.image.load("./img/cannon-1.png") # 24
wheel = [100,300]
body = [124, 324]

player = Player(wheel, 1)
turn = 1
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
                shot(angle, gauge, gameDisplay, clock, player)
            space = 0
        if keys[pygame.K_UP] and angle <= 90:
            angle += 1
        elif keys[pygame.K_DOWN] and angle >= 0:
            angle -= 1
        if keys[pygame.K_RIGHT]:
            body[0] += 1
            player.move(1, 0)
        elif keys[pygame.K_LEFT] :
            body[0] -= 1
            player.move(-1, 0)

        txt = font.render(str(space),True, BLACK)
        txt_angle = font.render(str(angle), True, BLACK)
        rotated_image = pygame.transform.rotate(cannon_body, angle)
        new_rect = rotated_image.get_rect(center=cannon_body.get_rect(center=body).center)
        gameDisplay.fill(WHITE)  # 배경 이미지
        gameDisplay.blit(rotated_image, new_rect)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,wheel)  # 바퀴 이미지
        pygame.draw.rect(gameDisplay, RED, [body[0]-35, 200, space, 10])
        gameDisplay.blit(txt,(0,0))
        gameDisplay.blit(txt_angle, (100, 0))
        pygame.display.update()
        clock.tick(20)

def shot(angle, gauge, gameDisplay, clock, player):
    global turn # 1p 좌표, 2p 좌표 
    global font
    print('//////////////////////////////////////////////////////')
    v_s, theta_s = gauge, angle
    init_pos = player.position
    v_w, theta_w, k, scale = environ(turn)
    x_coord, y_coord = coord(v_s, theta_s, v_w, theta_w, k, init_pos[0], init_pos[1])
    print(f'x_coord : {len(x_coord)}')
    print(f'y_coord : {len(y_coord)}')

    shell = pygame.image.load("./img/cannon-1.png")
    font = pygame.font.Font(None, 80)
    txt = font.render(str(gauge),True, BLACK)
    txt_angle = font.render(str(angle), True, BLACK)
    rotated_image = pygame.transform.rotate(cannon_body, angle)
    new_rect = rotated_image.get_rect(center=cannon_body.get_rect(center=body).center)

    # 좌표에 따른 이미지 출력 부분
    idx = 0
    while idx < len(x_coord):
        # 발사
        # 배경 -> 대포 -> 포탄 순으로 출력하면서 이전 포탄을 덮는 느낌으로 ㄱㄱ
        
        gameDisplay.fill(WHITE)  # 배경 이미지
        gameDisplay.blit(rotated_image, new_rect)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,wheel)  # 바퀴 이미지
        gameDisplay.blit(shell, (x_coord[idx], y_coord[idx]))
        pygame.draw.rect(gameDisplay, RED, [body[0]-35, 200, gauge, 10])
        gameDisplay.blit(txt,(0,0))
        gameDisplay.blit(txt_angle, (100, 0))
        pygame.display.update()
        idx += 1
        clock.tick(60)
    print(f'v_s : {gauge}')
    print(f'theta_s : {angle}')
    print(f'v_w : {v_w}')
    print(f'theta_w : {theta_w}')
    print(f'resistance : {k}')
    print(f'init coord : {x_coord[0], y_coord[0]}')
    turn += 1
        
if __name__ == "__main__":
    mainmenu()
    




