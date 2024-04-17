import pygame
import sys
import random
import time
from functions import coord, environ, calculation
from classes import Player, Button

pygame.init() # pygame 모듈 초기화
# 클래스 영역 ////////////////////////////////////////////////

class Player:
    
    def __init__(self, initial_position, side):
        self.position = initial_position
        self.damage = 1
        self.volume = 10
        self.side = side
        self.hp = 10

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def hit(self):
        self.hp -= (self.damage * damage_scale)

class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            gameDisplay.blit(img_in, (x, y))

# 함수 영역 ///////////////////////////////////////////////////
# 설명 부분
def explain():
    exp = True

    while exp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg_explain, (0, 0))
        Button(back, 500, 550, 230, 140, back_click, 500, 550, intro)

        pygame.display.update()
        clock.tick(15)

# 메인페이지(처음)
def intro():
    global gameDisplay
    menu = True
    clock = pygame.time.Clock()
    tmr = 0
    bg_main = [
        pygame.image.load("./img/main_page1.png"),
        pygame.image.load("./img/main_page2.png"),
        pygame.image.load("./img/main_page3.png"),
        pygame.image.load("./img/main_page4.png")
    ]
    
    while menu:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    gameDisplay = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    gameDisplay = pygame.display.set_mode((1280, 720))
        
        gameDisplay.blit(bg_main[tmr%4], [0, 0])   # 초당 프레임 수
        
        # 배경음악
        if pygame.mixer.get_busy() == False:
            # main_bgm.play()
            pass
        # 버튼만들기 Button(img, x, y , he, w , act_img,  act_x, act_y, func)
        Button(explain_back, 400, 550, 150, 80, explain_back_click, 400, 550, explain)
        Button(mainmenu_start, 700, 550, 150, 80, mainmenu_start_click, 700, 550, game)
        pygame.display.update()
        clock.tick(7)

def ready():
    global gameDisplay
    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)

    player1 = None
    player2 = None
    trigger = False

    def select1():
        if not player1:
            player 

    while not trigger:

        button1 = Button(explain_back, 400, 550, 150, 80, explain_back_click, 400, 550, select1)
        button2 = Button(mainmenu_start, 700, 550, 150, 80, mainmenu_start_click, 700, 550, select1)
        pygame.display.update()



# 게임이 끝났다면
def game_over(point):
    global cur_idx,next_level
    game_over = True
    bg_main = [pygame.image.load(f"./ending_img/{i}.png") for i in range(147)]
    # 화면에 맞게 이미지 크기 조정
    bg_main = [pygame.transform.scale(image, (display_width, display_height)) for image in bg_main]
    txt_1 = font_1.render("Your Score : " + str(point), True, WHITE)
    
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        cur_idx = (cur_idx + 1) % len(bg_main)
        time.sleep(0.1)
        next_level += 500  # 3초 추가
        gameDisplay.blit(bg_main[cur_idx], (0, 0))
        gameDisplay.blit(txt_1,[40,450])
        Button(mainmenu_start, 300, 600, 150, 80, mainmenu_start_click, 210, 535, intro)
        pygame.display.update() # 화면 업데이트
        clock.tick(15) #프레임 레이트 지정

def game():
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
        print(turn)
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

    turn += 1

# 변수 영역 //////////////////////////////////////////////////

WHITE = (255,255,255)
RED = (255, 10, 10)
BLACK = (0,0,0)
mainmenu_start = pygame.image.load("./img/start.png")
mainmenu_start_click = pygame.image.load("./img/start_click.png")
explain_back = pygame.image.load("./img/explain.png")
explain_back_click = pygame.image.load("./img/explain_click.png")
back = pygame.image.load("./img/back.png")
back_click = pygame.image.load("./img/back_click.png")
font = pygame.font.Font(None,80)
font_1 = pygame.font.Font(None,100)

cannon_body = pygame.image.load("./img/cannon-3.png")
cannon_wheel = pygame.image.load("./img/cannon-1.png") # 24
wheel = [100,300]
body = [124, 324]

player = Player(wheel, 1)
turn = 1

# 새로운 아이콘 이미지 로드
new_icon = pygame.image.load("./img/heart_icon.png")
pygame.display.set_icon(new_icon)

display_width = 1280
display_height = 720


gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("LOVE BOMB")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

bg_explain = pygame.image.load("./img/explain_bg.png")
bg = pygame.image.load("./img/neko_bg.png")
cursor =pygame.image.load("./img/neko_cursor.png")

if __name__ == "__main__":
    intro()

