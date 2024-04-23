import pygame
import sys
import random
import time
import numpy as np
from functions import coord, environ, calculation, seasonal
from classes import Player, Button

pygame.init() # pygame 모듈 초기화
# 클래스 영역 ////////////////////////////////////////////////

class Player:
    
    def __init__(self, initial_position, side):
        self.position = initial_position
        self.name = 'player' + str(side)
        self.damage = 100
        self.volume = 200  #74
        self.side = side
        self.hp = 100
        self.gauge = 0
        self.body = [initial_position[0]+24, initial_position[1]+24]
        self.moved = 0
        if side == 1:
            self.angle = 0
        elif side == 2:
            self.angle = 180
        self.hp_img = [img_hp[0]]*5

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy
        self.body[0] += dx
        self.body[1] += dy
        self.moved += abs(dx)
    def hit(self, damage, scale):
        self.hp = round(self.hp - (damage * scale))
        idx = self.hp // 20
        if self.hp % 20 != 0:
            self.hp_img[idx] = img_hp[5-(self.hp % 20)//6]
        else:
            self.hp_img[idx] = img_hp[6]

    
    def angle_move(self, theta):
        if self.side == 1:
            self.angle += theta
        elif self.side == 2:
            self.angle -= theta

    def charge(self, power):
        self.gauge += power
    
    def moved_init(self):
        self.moved = 0
class Environment:
    season = 'spring'
    def __init__(self):
        self.element(self.season)
        
    def season_check(self, turn):
        if 1 <= turn < 4:
            self.season = 'spring'
        elif 4 <= turn < 7:
            self.season = 'summer'
        elif 7 <= turn < 10:
            self.season = 'autumn'
        else:
            self.season = 'winter'
        self.element(self.season)
    def element(self, season):
        if season == 'spring':
            wind_velocity = list(range(10))
            wind_angle = list(range(0, 190, 10))
            self.resistance = 0
            self.damage_scale = 1
        elif season == 'summer':
            wind_velocity = list(range(20))
            wind_angle = list(range(0, 190, 10))
            self.resistance = 0.2
            self.damage_scale = 0.7
        elif season == 'autumn':
            wind_velocity = list(range(10))
            wind_angle = list(range(0, 190, 10))
            self.resistance = 0
            self.damage_scale = 2
        elif season == 'winter':
            wind_velocity = list(range(20))
            wind_angle = list(range(0, 190, 10))
            self.resistance = 0.1
            self.damage_scale = 1.2
            
        self.v_w = wind_velocity[np.random.randint(0, len(wind_velocity)-1)]
        self.theta_w = wind_angle[np.random.randint(0, len(wind_angle)-1)]
    
    
    
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
    global gameDisplay, player1, player2, winner, turn, environment
    # 초기화
    player1, player2, winner, environment = None, None, None, None
    menu = True
    turn = 1
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
        Button(mainmenu_start, 680, 550, 300, 50, mainmenu_start_click, 680, 550, ready)
        pygame.display.update()
        clock.tick(7)

# 준비 화면
def ready():
    global gameDisplay, player1, player2

    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)

    trigger = False
    while not trigger:
        gameDisplay.blit(bg_ready, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        Button(p1_button, 350, 550, 300, 50, p1_button_click, 350, 550, select1)
        Button(p2_button, 630, 550, 300, 50, p2_button_click, 630, 550, select2)
        if player1 and player2:
            trigger = True

        if trigger:
            game(player1, player2)
        pygame.display.update()
        clock.tick(7)
        if not player1 and not player2:
            print('----------------------------------------------')
        elif player1:
            print('player1 is ready')
        elif player2:
            print('player2 is ready')
    
# player 1 선택
def select1():
    global player1
    if not player1:
        player1 = Player([100, 550], 1)
        print(f'player1 ready : {player1.position}')

# player 2 선택
def select2():
    global player2
    if not player2:
        player2 = Player([1100, 550], 2)
        print(f'player2 ready : {player2.position}')


# 게임이 끝났다면
def game_over(winner):
    game_over = True
    bg_main = [pygame.image.load(f"./ending_img/{i}.png") for i in range(147)]
    # 화면에 맞게 이미지 크기 조정
    bg_main = [pygame.transform.scale(image, (display_width, display_height)) for image in bg_main]
    txt_1 = font_1.render(winner, True, WHITE)
    cur_idx = 0
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        display_idx = cur_idx % len(bg_main)
        time.sleep(0.1)
        # next_level += 500  # 3초 추가
        gameDisplay.blit(bg_main[display_idx], (0, 0))
        gameDisplay.blit(txt_1,[40,450])
        Button(mainmenu_start, 300, 600, 150, 80, mainmenu_start_click, 300, 600, intro)
        pygame.display.update() # 화면 업데이트
        cur_idx += 1
        clock.tick(15) #프레임 레이트 지정

# 게임 실행 함수
def game(player1, player2):
    global turn, environment
    pygame.init()
    print(player1.position, player2.position)
    
    environment = Environment()
    print(environment.v_w)
    # font = pygame.font.Font(None, 40)
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("대포 움직이기")
    clock = pygame.time.Clock()
    menu = True
    while menu:
        if environment.season == 'spring':
            background = pygame.image.load("./img/spring_bg.png")
        elif environment.season == 'summer':
            background = pygame.image.load("./img/summer_bg.png")
        elif environment.season == 'autumn':
            background = pygame.image.load("./img/fall_bg.png")
        elif environment.season == 'winter':
            background = pygame.image.load("./img/winter_bg.png")
        
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
            if player.moved < 100:
                player.move(5, 0)
        elif keys[pygame.K_LEFT] :
            if player.moved < 100:
                player.move(-5, 0)

        txt = font.render(str(player.gauge),True, BLACK)
        txt_angle_1 = font.render(str(player1.angle), True, BLACK)
        txt_angle_2 = font.render(str(180 - player2.angle), True, BLACK)
        txt_velocity = font.render(f'{environment.v_w}m/s', True, BLACK)
        
        velocity_rect = txt_velocity.get_rect(center = (640, 180))
        
        rotated_image1 = pygame.transform.rotate(cannon_body1, player1.angle)
        new_rect1 = rotated_image1.get_rect(center=cannon_body1.get_rect(center=player1.body).center)

        rotated_image2 = pygame.transform.rotate(cannon_body2, player2.angle-180)
        new_rect2 = rotated_image2.get_rect(center=cannon_body2.get_rect(center=player2.body).center)

        rotate_arrow = pygame.transform.rotate(wind_direction, -environment.theta_w)
        arrow_rect = rotate_arrow.get_rect(center = (640, 100))
        

        gameDisplay.blit(background, (0, 0))  # 배경 이미지
        # gameDisplay.fill(WHITE)   # test 용

        gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,player1.position)  # 바퀴 이미지

        gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포
        gameDisplay.blit(cannon_wheel,player2.position)  # 바퀴 이미지

        pygame.draw.rect(gameDisplay, RED, [player.body[0]-35, player.body[1]-120, player.gauge, 10])
        gameDisplay.blit(txt,(0,0))
        # gameDisplay.blit(txt_angle, (150, 0))
        gameDisplay.blit(txt_angle_1, (player1.body[0]-10, player1.body[1]-180))
        gameDisplay.blit(txt_angle_2, (player2.body[0]-10, player2.body[1]-180))
        gameDisplay.blit(txt_velocity, velocity_rect)
        
        # 풍향 표시
        gameDisplay.blit(rotate_arrow, arrow_rect)

        # 캐릭터 이미지 출력
        gameDisplay.blit(character1, (player1.position[0]-70, player1.position[1]-65))
        gameDisplay.blit(character2, (player2.position[0]-30, player2.position[1]-65))

        # 체력 이미지 출력 파트
        temp_1 = (player1.hp-1)//20
        for i in range(5):
            # gameDisplay.blit(player11.hp_img[i], (50* (i+1), 250))
            pos_x = 60 * (i+1)
            if i < temp_1:
                gameDisplay.blit(img_hp[0], (pos_x, 100))
            elif i > temp_1:
                gameDisplay.blit(img_hp[6], (pos_x, 100))
            elif i == temp_1:
                if player1.hp % 20 == 0:
                    gameDisplay.blit(img_hp[0], (pos_x, 100))
                elif player1.hp % 20 >= 17:
                    gameDisplay.blit(img_hp[1], (pos_x, 100))
                elif player1.hp % 20 >= 13:
                    gameDisplay.blit(img_hp[2], (pos_x, 100))
                elif player1.hp % 20 >= 9:
                    gameDisplay.blit(img_hp[3], (pos_x, 100))
                elif player1.hp % 20 >= 5:
                    gameDisplay.blit(img_hp[4], (pos_x, 100))
                else:
                    gameDisplay.blit(img_hp[5], (pos_x, 100))
        
        temp_2 = (player2.hp-1)//20
        for i in range(5):
            # gameDisplay.blit(player21.hp_img[i], (50* (i+1), 250))
            pos_x = 1220 - 60*(i+1)
            if i < temp_2:
                gameDisplay.blit(img_hp[0], (pos_x, 100))
            elif i > temp_2:
                gameDisplay.blit(img_hp[6], (pos_x, 100))
            elif i == temp_2:
                if player2.hp % 20 == 0:
                    gameDisplay.blit(img_hp[0], (pos_x, 100))
                elif player2.hp % 20 >= 17:
                    gameDisplay.blit(img_hp[1], (pos_x, 100))
                elif player2.hp % 20 >= 13:
                    gameDisplay.blit(img_hp[2], (pos_x, 100))
                elif player2.hp % 20 >= 9:
                    gameDisplay.blit(img_hp[3], (pos_x, 100))
                elif player2.hp % 20 >= 5:
                    gameDisplay.blit(img_hp[4], (pos_x, 100))
                else:
                    gameDisplay.blit(img_hp[5], (pos_x, 100))
        if winner:
            break
        pygame.display.update()
        clock.tick(20)

    game_over(winner)

# 발사 이미지 출력 함수
def shot(player):
    global turn, font, player1, player2, environment
    
    v_w, theta_w, k, scale = environment.v_w, environment.theta_w, environment.resistance, environment.damage_scale
    x_coord, y_coord = coord(player, v_w, theta_w, k)

    txt_angle_1 = font.render(str(player1.angle), True, BLACK)
    txt_angle_2 = font.render(str(180 - player2.angle), True, BLACK)
    txt_velocity = font.render(f'{environment.v_w}m/s', True, BLACK)
    velocity_rect = txt_velocity.get_rect(center = (640, 180))
    
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    print(f'position : {player.position}')
    print(f'{x_coord[0], y_coord[0]}')
    
    season = seasonal(turn)
    if season == 'spring':
        background = pygame.image.load("./img/spring_bg.png")
    elif season == 'summer':
        background = pygame.image.load("./img/summer_bg.png")
    elif season == 'autumn':
        background = pygame.image.load("./img/fall_bg.png")
    elif season == 'winter':
        background = pygame.image.load("./img/winter_bg.png")

    shell = pygame.image.load("./img/neko6.png")
    # font = pygame.font.Font(None, 40)
    txt = font.render(str(player.gauge),True, BLACK)
    if player.side == 1:
        txt_angle = font.render(str(player.angle), True, BLACK)
    elif player.side == 2:
        txt_angle = font.render(str(180-player.angle), True, BLACK)

    rotated_image1 = pygame.transform.rotate(cannon_body1, player1.angle)
    new_rect1 = rotated_image1.get_rect(center=cannon_body1.get_rect(center=player1.body).center)

    rotated_image2 = pygame.transform.rotate(cannon_body2, player2.angle-180)
    new_rect2 = rotated_image2.get_rect(center=cannon_body2.get_rect(center=player2.body).center)

    # 좌표에 따른 이미지 출력 부분
    idx = 0
    while idx < len(x_coord):
        # 발사
        # 배경 -> 대포 -> 포탄 순으로 출력하면서 이전 포탄을 덮는 느낌으로 ㄱㄱ
        
        gameDisplay.blit(background, (0, 0))  # 배경 이미지
        # gameDisplay.fill(WHITE)
        
        gameDisplay.blit(shell, (x_coord[idx], y_coord[idx]))
        
        gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포1
        gameDisplay.blit(cannon_wheel,player1.position)  # 바퀴 이미지
        gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포2
        gameDisplay.blit(cannon_wheel,player2.position)  # 바퀴 이미지
        
        gameDisplay.blit(txt_angle_1, (player1.body[0]-10, player1.body[1]-180))
        gameDisplay.blit(txt_angle_2, (player2.body[0]-10, player2.body[1]-180))
        
        pygame.draw.rect(gameDisplay, RED, [player.body[0]-35, player.body[1]-120, player.gauge, 10])
        gameDisplay.blit(txt,(0,0))
        
        # 캐릭터 이미지 출력
        gameDisplay.blit(character1, (player1.position[0]-70, player1.position[1]-65))
        gameDisplay.blit(character2, (player2.position[0]-30, player2.position[1]-65))
        
        # 풍향 출력
        rotate_arrow = pygame.transform.rotate(wind_direction, -environment.theta_w)
        arrow_rect = rotate_arrow.get_rect(center = (640, 100))
        gameDisplay.blit(rotate_arrow, arrow_rect)
        
        gameDisplay.blit(txt_velocity, velocity_rect)
        
        # 체력 이미지 출력 파트
        temp_1 = (player1.hp-1)//20
        for i in range(5):
            pos_x = 60 * (i+1)
            if i < temp_1:
                gameDisplay.blit(img_hp[0], (pos_x, 100))
            elif i > temp_1:
                gameDisplay.blit(img_hp[6], (pos_x, 100))
            elif i == temp_1:
                if player1.hp % 20 == 0:
                    gameDisplay.blit(img_hp[0], (pos_x, 100))
                elif player1.hp % 20 >= 17:
                    gameDisplay.blit(img_hp[1], (pos_x, 100))
                elif player1.hp % 20 >= 13:
                    gameDisplay.blit(img_hp[2], (pos_x, 100))
                elif player1.hp % 20 >= 9:
                    gameDisplay.blit(img_hp[3], (pos_x, 100))
                elif player1.hp % 20 >= 5:
                    gameDisplay.blit(img_hp[4], (pos_x, 100))
                else:
                    gameDisplay.blit(img_hp[5], (pos_x, 100))
        
        temp_2 = (player2.hp-1)//20
        for i in range(5):
            pos_x = 1220 - 60*(i+1)
            if i < temp_2:
                gameDisplay.blit(img_hp[0], (pos_x, 100))
            elif i > temp_2:
                gameDisplay.blit(img_hp[6], (pos_x, 100))
            elif i == temp_2:
                if player2.hp % 20 == 0:
                    gameDisplay.blit(img_hp[0], (pos_x, 100))
                elif player2.hp % 20 >= 17:
                    gameDisplay.blit(img_hp[1], (pos_x, 100))
                elif player2.hp % 20 >= 13:
                    gameDisplay.blit(img_hp[2], (pos_x, 100))
                elif player2.hp % 20 >= 9:
                    gameDisplay.blit(img_hp[3], (pos_x, 100))
                elif player2.hp % 20 >= 5:
                    gameDisplay.blit(img_hp[4], (pos_x, 100))
                else:
                    gameDisplay.blit(img_hp[5], (pos_x, 100))
        pygame.display.update()
        idx += 1
        clock.tick(200)
    impact = (x_coord[idx-1], y_coord[idx-1])
    
    calculate(player, impact, scale)
    turn += 1
    environment.season_check(turn)
    player.moved_init()
    
    

# 피격 판정 계산 함수
def calculate(player, impact, scale):
    global player1
    global player2
    global winner
    
    if player.side == 1:
        enemy = player2
    elif player.side == 2:
        enemy = player1
    
    if impact[0] - enemy.volume <= enemy.position[0] <= impact[0] + enemy.volume:
        enemy.hit(player.damage, scale)
        if enemy.hp <= 0:
            winner = player.name


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

font = pygame.font.Font(None,60)
font_1 = pygame.font.Font(None,100)

wind_direction = pygame.transform.scale(pygame.image.load("./img/arrow.png"), (100, 100))

character1 = pygame.transform.scale(pygame.image.load("./img/character0.png"), (150, 150))
character2 = pygame.transform.scale(pygame.image.load("./img/character1.png"), (150, 150))

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
winner = None
environment = None
turn = 1

# 새로운 아이콘 이미지 로드
new_icon = pygame.image.load("./img/heart_icon.png")
pygame.display.set_icon(new_icon)

display_width = 1280
display_height = 720
img_hp = [
    pygame.transform.scale(pygame.image.load("./hp_img/hp_6.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_5.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_4.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_3.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_2.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_1.png"), (50, 50)),
    pygame.transform.scale(pygame.image.load("./hp_img/hp_0.png"), (50, 50)),
][::-1]



gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("LOVE BOMB")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

bg_explain = pygame.image.load("./img/explain_bg.png")
bg = pygame.image.load("./img/neko_bg.png")
bg_ready = pygame.image.load("./img/ready_bg.png")
cursor =pygame.image.load("./img/neko_cursor.png")

# 실행 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    intro()

