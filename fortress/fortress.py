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
        self.gauge = 0
        self.body = [initial_position[0]+24, initial_position[1]+24]
        if side == 1:
            self.angle = 0
        elif side == 2:
            self.angle = 180

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy
        self.body[0] += dx
        self.body[1] += dy
    def hit(self):
        self.hp -= (self.damage * damage_scale)
    
    def angle_move(self, theta):
        if self.side == 1:
            self.angle += theta
        elif self.side == 2:
            self.angle -= theta

    def charge(self, power):
        self.gauge += power

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
        Button(explain_back, 320, 550, 300, 50, explain_back_click, 320, 550, explain)
        Button(mainmenu_start, 680, 550, 250, 50, mainmenu_start_click, 680, 550, ready)
        pygame.display.update()
        clock.tick(7)

def ready():
    global gameDisplay
    global player1
    global player2

    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)

    trigger = False
    while not trigger:
        gameDisplay.blit(bg_ready, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Button(p1_button, 350, 550, 250, 50, p1_button_click, 350, 550, select1)
        Button(p2_button, 630, 550, 250, 50, p2_button_click, 630, 550, select2)
        if player1 and player2:
            trigger = True

        if trigger:
            game(player1, player2)
        pygame.display.update()
        clock.tick(7)
        print('-')
    

def select1():
    global player1
    if not player1:
        player1 = Player([100, 500], 1)
        print(f'player1 ready : {player1.position}')

def select2():
    global player2
    if not player2:
        player2 = Player([1080, 500], 2)
        print(f'player2 ready : {player2.position}')


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

def game(player1, player2):
    global turn
    pygame.init()
    print(player1.position, player2.position)
    
    font = pygame.font.Font(None, 80)
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("대포 움직이기")
    clock = pygame.time.Clock()
    menu = True
    while menu:
        print(turn)
        if turn % 2 == 1:
            player = player1
        else:
            player = player2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] :
            player.charge(5)
            if player.gauge >= 100 :
                player.gauge = 100
        else :
            if player.gauge != 0 :
                shot(player)
            player.gauge = 0
        if keys[pygame.K_UP]:
            if player.side == 1 and player.angle < 90:
                player.angle_move(1)
            elif player.side == 2 and player.angle > 90:
                player.angle_move(1)
        elif keys[pygame.K_DOWN]:
            if player.side ==1 and player.angle > 0:
                player.angle_move(-1)
            elif player.side == 2 and player.angle < 180:
                player.angle_move(-1)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        elif keys[pygame.K_LEFT] :
            player.move(-1, 0)

        txt = font.render(str(player.gauge),True, BLACK)
        if player.side == 1:
            txt_angle = font.render(str(player.angle), True, BLACK)
        elif player.side == 2:
            txt_angle = font.render(str(180 - player.angle), True, BLACK)

        rotated_image1 = pygame.transform.rotate(cannon_body1, player1.angle)
        new_rect1 = rotated_image1.get_rect(center=cannon_body1.get_rect(center=player1.body).center)

        rotated_image2 = pygame.transform.rotate(cannon_body2, player2.angle - 180)
        new_rect2 = rotated_image2.get_rect(center=cannon_body2.get_rect(center=player2.body).center)

        gameDisplay.blit(summer_bg, (0, 0))  # 배경 이미지

        gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,player1.position)  # 바퀴 이미지

        gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,player2.position)  # 바퀴 이미지

        pygame.draw.rect(gameDisplay, RED, [player.body[0]-35, player.body[1]-150, player.gauge, 10])
        gameDisplay.blit(txt,(0,0))
        gameDisplay.blit(txt_angle, (150, 0))
        pygame.display.update()
        clock.tick(20)

def shot(player):
    global turn
    global font
    global player1
    global player2
    print('//////////////////////////////////////////////////////')
    v_s, theta_s = player.gauge, player.angle
    init_pos = player.position
    v_w, theta_w, k, scale = environ(turn)
    x_coord, y_coord = coord(v_s, theta_s, v_w, theta_w, k, init_pos[0], init_pos[1])
    print(f'x_coord : {len(x_coord)}')
    print(f'y_coord : {len(y_coord)}')

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()

    shell = pygame.image.load("./img/cannon-1.png")
    font = pygame.font.Font(None, 80)
    txt = font.render(str(player.gauge),True, BLACK)
    if player.side == 1:
        txt_angle = font.render(str(player.angle), True, BLACK)
    elif player.side == 2:
        txt_angle = font.render(str(180 - player.angle), True, BLACK)

    rotated_image1 = pygame.transform.rotate(cannon_body1, player1.angle)
    new_rect1 = rotated_image1.get_rect(center=cannon_body1.get_rect(center=player1.body).center)

    rotated_image2 = pygame.transform.rotate(cannon_body2, player2.angle - 180)
    new_rect2 = rotated_image2.get_rect(center=cannon_body2.get_rect(center=player2.body).center)

    # 좌표에 따른 이미지 출력 부분
    idx = 0
    while idx < len(x_coord):
        # 발사
        # 배경 -> 대포 -> 포탄 순으로 출력하면서 이전 포탄을 덮는 느낌으로 ㄱㄱ
        
        gameDisplay.fill(WHITE)  # 배경 이미지
        gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포1
        gameDisplay.blit(cannon_wheel,player1.position)  # 바퀴 이미지
        gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포2
        gameDisplay.blit(cannon_wheel,player2.position)  # 바퀴 이미지


        gameDisplay.blit(shell, (x_coord[idx], y_coord[idx]))
        pygame.draw.rect(gameDisplay, RED, [player.body[0]-35, player.body[1]-150, player.gauge, 10])
        gameDisplay.blit(txt,(0,0))
        gameDisplay.blit(txt_angle, (150, 0))
        pygame.display.update()
        idx += 1
        clock.tick(120)

    turn += 1

# 변수 영역 //////////////////////////////////////////////////

WHITE = (255,255,255)
RED = (255, 10, 10)
BLACK = (0,0,0)
mainmenu_start = pygame.image.load("./img/start.png")
mainmenu_start_click = pygame.image.load("./img/start_click.png")
explain_back = pygame.image.load("./img/explain.png")
explain_back_click = pygame.image.load("./img/explain_click.png")
p1_button = pygame.image.load("./img/player1.png")
p1_button_click = pygame.image.load("./img/player1_click.png")
p2_button = pygame.image.load("./img/player2.png")
p2_button_click = pygame.image.load("./img/player2_click.png")
back = pygame.image.load("./img/back.png")
back_click = pygame.image.load("./img/back_click.png")
font = pygame.font.Font(None,80)
font_1 = pygame.font.Font(None,100)

# 계절 이미지 변수
summer_bg = pygame.image.load("./img/summer_bg.png")

cannon_body1 = pygame.image.load("./img/cannon-3.png")
cannon_body2 = pygame.image.load("./img/cannon-4.png")
cannon_wheel = pygame.image.load("./img/cannon-1.png") # 24
bomb = pygame.image.load("./img/heart_bomb.png") 
# wheel = [100,300]
body = [124, 324]

player1 = None
player2 = None
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
bg_ready = pygame.image.load("./img/ready_bg.png")
cursor =pygame.image.load("./img/neko_cursor.png")

if __name__ == "__main__":
    intro()

