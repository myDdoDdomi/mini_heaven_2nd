import pygame
import sys
import random
import time
import numpy as np
from functions import coord, environ, calculation, seasonal
from threading import Thread
import pickle
from _thread import *
import socket
import yaml

yaml_file = "config.yaml"
with open(yaml_file, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

HOST = config['server']['ip']  # 호스트
PORT = config['server']['port']  # 포트
NAME = config['client']['name'] #이름을 입력해주세요



WHITE = (255,255,255)
RED = (255, 10, 10)
BLACK = (0,0,0)
display_width = 1280
display_height = 720




game_trigger = 0
client_sockets = []
# 클래스 영역 ////////////////////////////////////////////////
# 화면 송출
class display_fortress:
    def __init__(self) -> None:
        self.mainmenu_start = pygame.image.load("./img/start.png")
        self.mainmenu_start_click = pygame.image.load("./img/start_click.png")
        self.explain_back = pygame.image.load("./img/explain.png")
        self.explain_back_click = pygame.image.load("./img/explain_click.png")
        self.p1_button = pygame.image.load("./img/player1.png")
        self.p1_button_click = pygame.image.load("./img/player1_click.png")
        self.p2_button = pygame.image.load("./img/player2.png")
        self.p2_button_click = pygame.image.load("./img/player2_click.png")
        self.back = pygame.image.load("./img/back.png")
        self.back_click = pygame.image.load("./img/back_click.png")

        self.font = pygame.font.Font(None,60)
        self.font_1 = pygame.font.Font(None,100)
        self.korean_font = pygame.font.Font("./font/Sagak-sagak.ttf", 30)

        self.wind_direction = pygame.transform.scale(pygame.image.load("./img/arrow2.png"), (100, 100))

        self.character1 = pygame.transform.scale(pygame.image.load("./img/character0.png"), (170, 170))
        self.character2 = pygame.transform.scale(pygame.image.load("./img/character1.png"), (170, 170))

        # 계절 이미지 변수
        self.summer_bg = pygame.image.load("./img/summer_bg.png")

        self.cannon_body1 = pygame.transform.scale(pygame.image.load("./img/cannon-3.png"), (94, 120))
        self.cannon_body2 = pygame.transform.scale(pygame.image.load("./img/cannon-4.png"), (94, 120))
        self.cannon_wheel = pygame.transform.scale(pygame.image.load("./img/cannon-1.png"), (39,39)) # 24
        self.bomb = pygame.image.load("./img/heart_bomb.png")
        # wheel = [100,300]
        self.body = [124, 324]

        self.shell = pygame.image.load("./img/heart_bomb.png")

        self.player1 = None
        self.player2 = None
        self.win = None
        self.defeated = None
        self.environment = None
        self.turn = 1
        self.bomb_sound= pygame.mixer.Sound('./bgm/bomb_bgm.mp3')
        self.player = None
        # 새로운 아이콘 이미지 로드
        self.new_icon = pygame.image.load("./img/heart_icon.png")



        self.bg_explain = pygame.image.load("./img/explain_bg.png")
        self.bg_tip = pygame.image.load("./img/intro_game_tip.png")
        self.bg = pygame.image.load("./img/neko_bg.png")
        self.bg_ready = pygame.image.load("./img/ready_bg.png")
        self.cursor =pygame.image.load("./img/neko_cursor.png")
        self.ending_bg = pygame.image.load("./img/game_over_result.png")

        self.ending_rect = self.ending_bg.get_rect(center = (640, 360))

        self.right_button = pygame.image.load("./img/intro_right_button.png")
        self.left_button = pygame.image.load("./img/intro_left_button.png")
        
        self.regame_button = pygame.image.load("./img/regame.png")
        self.regame_button_click = pygame.image.load("./img/regame_click.png")
        self.bg_main = [
            pygame.image.load("./img/main_page1.png"),
            pygame.image.load("./img/main_page2.png"),
            pygame.image.load("./img/main_page3.png"),
            pygame.image.load("./img/main_page4.png")
        ]
        
    def game_start(self):
        game_start = Thread(target = self.game_on)
        game_start.start()
        
    
    def game_on(self):
        global game_trigger, client_sockets, environment
        # 메인 bgm 적용
        pygame.display.set_icon(self.new_icon)
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("포트리스 클라이언트")
        
        pygame.mixer.music.load('./bgm/main_bgm.mp3')
        pygame.mixer.music.play(-1)    # -1: 반복 
        # 초기화
        self.player1, self.player2, self.win, self.defeated, self.environment = None, None, None, None, None
        menu = True
        self.turn = 1
        tmr = 0
        
        
        while game_trigger == 0:
            tmr = tmr + 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.gameDisplay = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                    if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                        self.gameDisplay = pygame.display.set_mode((1280, 720))
            
            self.gameDisplay.blit(self.bg_main[tmr%4], [0, 0])   # 초당 프레임 수
            
            # 배경음악
            if pygame.mixer.get_busy() == False:
                # main_bgm.play()
                pass
            # 버튼만들기 Button(img, x, y , he, w , act_img,  act_x, act_y, func)
            self.Button(self.explain_back, 320, 550, 300, 50, self.explain_back_click, 320, 550, self.gameDisplay, self.explain)
            self.Button(self.mainmenu_start, 680, 550, 300, 50, self.mainmenu_start_click, 680, 550, self.gameDisplay, self.ready)
            pygame.display.update()
            self.clock.tick(7)
            
        
        while True :
            while game_trigger == 1 : # 내 차례
                print(self.player1.position, self.player2.position)
                if self.environment.season == 'spring':
                    background = pygame.image.load("./img/spring_bg.png")
                elif self.environment.season == 'summer':
                    background = pygame.image.load("./img/summer_bg.png")
                elif self.environment.season == 'autumn':
                    background = pygame.image.load("./img/fall_bg.png")
                elif self.environment.season == 'winter':
                    background = pygame.image.load("./img/winter_bg.png")
                
                
                if self.turn % 2 == 1:
                    player = self.player1
                else:
                    player = self.player2

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                keys = pygame.key.get_pressed()

                # 방향키로 조정
                if keys[pygame.K_SPACE] :
                    player.charge(5)
                    if player.gauge >= 100 :
                        player.gauge = 100
                else :
                    if player.gauge > 0 :
                        self.shot(player)        # 현재 플레이어의 게이지가 0이 초과라면 shot 함수 실행
                    
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
                    print(f'initial : {player.initial_position[0]}')
                    print(f'position : {player.position[0]}')
                    if player.side == 1:
                        if player.initial_position[0]-50 < player.position[0]+5 < player.initial_position[0] +300:
                            player.move(5, 0)
                    elif player.side == 2:
                        if player.initial_position[0]-300 < player.position[0]+5 < player.initial_position[0]+50:
                            player.move(5, 0)
                elif keys[pygame.K_LEFT] :
                    if player.side == 1:
                        if player.initial_position[0]-50 < player.position[0]-5 < player.initial_position[0] +300:
                            player.move(-5, 0)
                    elif player.side == 2:
                        if player.initial_position[0]-300 < player.position[0]-5 < player.initial_position[0]+50:
                            player.move(-5, 0)

                # 화면 출력
                txt = self.font.render(str(player.gauge),True, BLACK)
                txt_angle_1 = self.font.render(str(self.player1.angle), True, BLACK)
                txt_angle_2 = self.font.render(str(180 - self.player2.angle), True, BLACK)
                txt_velocity = self.font.render(f'{self.environment.v_w}m/s', True, BLACK)
                
                velocity_rect = txt_velocity.get_rect(center = (640, 180))
                
                rotated_image1 = pygame.transform.rotate(self.cannon_body1, self.player1.angle)
                new_rect1 = rotated_image1.get_rect(center=self.cannon_body1.get_rect(center=[self.player1.position[0]+24,self.player1.position[1]+24]).center)

                rotated_image2 = pygame.transform.rotate(self.cannon_body2, self.player2.angle-180)
                new_rect2 = rotated_image2.get_rect(center=self.cannon_body2.get_rect(center=[self.player2.position[0]+24,self.player2.position[1]+24]).center)

                rotate_arrow = pygame.transform.rotate(self.wind_direction, -self.environment.theta_w)
                arrow_rect = rotate_arrow.get_rect(center = (640, 100))
                

                self.gameDisplay.blit(background, (0, 0))  # 배경 이미지
                # gameDisplay.fill(WHITE)   # test 용
                
                self.gameDisplay.blit(self.character1, (self.player1.position[0]-100, self.player1.position[1]-80))
                self.gameDisplay.blit(self.character2, (self.player2.position[0]-20, self.player2.position[1]-80))

                self.gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포
                self.gameDisplay.blit(self.cannon_wheel,(self.player1.position[0], self.player1.position[1]+10))  # 바퀴 이미지

                self.gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포
                self.gameDisplay.blit(self.cannon_wheel,(self.player2.position[0], self.player2.position[1]+10))  # 바퀴 이미지

                pygame.draw.rect(self.gameDisplay, RED, [player.body[0]-35, player.body[1]-120, player.gauge, 10])
                # gameDisplay.blit(txt,(0,0))
                # # gameDisplay.blit(txt_angle, (150, 0))
                # gameDisplay.blit(txt_angle_1, (player1.body[0]-10, player1.body[1]-180))
                # gameDisplay.blit(txt_angle_2, (player2.body[0]-10, player2.body[1]-180))
                self.gameDisplay.blit(txt_velocity, velocity_rect)
                
                # 풍향 표시
                self.gameDisplay.blit(rotate_arrow, arrow_rect)

                # 캐릭터 이미지 출력

                # 체력 이미지 출력 파트
                temp_1 = (self.player1.hp-1)//20
                for i in range(5):
                    # gameDisplay.blit(player11.hp_img[i], (50* (i+1), 250))
                    pos_x = 60 * (i+1)
                    if i < temp_1:
                        self.gameDisplay.blit(self.player1.img_hp[0], (pos_x, 150))
                    elif i > temp_1:
                        self.gameDisplay.blit(self.player1.img_hp[6], (pos_x, 150))
                    elif i == temp_1:
                        if self.player1.hp % 20 == 0:
                            self.gameDisplay.blit(self.player1.img_hp[0], (pos_x, 150))
                        elif self.player1.hp % 20 >= 17:
                            self.gameDisplay.blit(self.player1.img_hp[1], (pos_x, 150))
                        elif self.player1.hp % 20 >= 13:
                            self.gameDisplay.blit(self.player1.img_hp[2], (pos_x, 150))
                        elif self.player1.hp % 20 >= 9:
                            self.gameDisplay.blit(self.player1.img_hp[3], (pos_x, 150))
                        elif self.player1.hp % 20 >= 5:
                            self.gameDisplay.blit(self.player1.img_hp[4], (pos_x, 150))
                        else:
                            self.gameDisplay.blit(self.player1.img_hp[5], (pos_x, 150))
                
                temp_2 = (self.player2.hp-1)//20
                for i in range(5):
                    # gameDisplay.blit(player21.hp_img[i], (50* (i+1), 250))
                    pos_x = 1220 - 60*(i+1)
                    if i < temp_2:
                        self.gameDisplay.blit(self.player2.img_hp[0], (pos_x, 150))
                    elif i > temp_2:
                        self.gameDisplay.blit(self.player2.img_hp[6], (pos_x, 150))
                    elif i == temp_2:
                        if self.player2.hp % 20 == 0:
                            self.gameDisplay.blit(self.player2.img_hp[0], (pos_x, 150))
                        elif self.player2.hp % 20 >= 17:
                            self.gameDisplay.blit(self.player2.img_hp[1], (pos_x, 150))
                        elif self.player2.hp % 20 >= 13:
                            self.gameDisplay.blit(self.player2.img_hp[2], (pos_x, 150))
                        elif self.player2.hp % 20 >= 9:
                            self.gameDisplay.blit(self.player2.img_hp[3], (pos_x, 150))
                        elif self.player2.hp % 20 >= 5:
                            self.gameDisplay.blit(self.player2.img_hp[4], (pos_x, 150))
                        else:
                            self.gameDisplay.blit(self.player2.img_hp[5], (pos_x, 150))
                # 전역 변수의 win이 있다면 while문 종료
                pygame.display.update()
                self.clock.tick(20)
    
                
                
            while game_trigger == 2 : # 상대방 차례
                if self.environment.season == 'spring':
                    background = pygame.image.load("./img/spring_bg.png")
                elif self.environment.season == 'summer':
                    background = pygame.image.load("./img/summer_bg.png")
                elif self.environment.season == 'autumn':
                    background = pygame.image.load("./img/fall_bg.png")
                elif self.environment.season == 'winter':
                    background = pygame.image.load("./img/winter_bg.png")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                txt_angle_1 = self.font.render(str(self.player1.angle), True, BLACK)
                txt_angle_2 = self.font.render(str(180 - self.player2.angle), True, BLACK)
                txt_velocity = self.font.render(f'{self.environment.v_w}m/s', True, BLACK)
                
                velocity_rect = txt_velocity.get_rect(center = (640, 180))
                
                rotated_image1 = pygame.transform.rotate(self.cannon_body1, self.player1.angle)
                new_rect1 = rotated_image1.get_rect(center=self.cannon_body1.get_rect(center=[self.player1.position[0]+24,self.player1.position[1]+24]).center)

                rotated_image2 = pygame.transform.rotate(self.cannon_body2, self.player2.angle-180)
                new_rect2 = rotated_image2.get_rect(center=self.cannon_body2.get_rect(center=[self.player2.position[0]+24,self.player2.position[1]+24]).center)

                rotate_arrow = pygame.transform.rotate(self.wind_direction, -self.environment.theta_w)
                arrow_rect = rotate_arrow.get_rect(center = (640, 100))
                

                self.gameDisplay.blit(background, (0, 0))  # 배경 이미지
                # gameDisplay.fill(WHITE)   # test 용
                
                self.gameDisplay.blit(self.character1, (self.player1.position[0]-100, self.player1.position[1]-80))
                self.gameDisplay.blit(self.character2, (self.player2.position[0]-20, self.player2.position[1]-80))

                self.gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포
                self.gameDisplay.blit(self.cannon_wheel,(self.player1.position[0], self.player1.position[1]+10))  # 바퀴 이미지

                self.gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포
                self.gameDisplay.blit(self.cannon_wheel,(self.player2.position[0], self.player2.position[1]+10))  # 바퀴 이미지

                # gameDisplay.blit(txt,(0,0))
                # # gameDisplay.blit(txt_angle, (150, 0))
                # gameDisplay.blit(txt_angle_1, (player1.body[0]-10, player1.body[1]-180))
                # gameDisplay.blit(txt_angle_2, (player2.body[0]-10, player2.body[1]-180))
                self.gameDisplay.blit(txt_velocity, velocity_rect)
                
                # 풍향 표시
                self.gameDisplay.blit(rotate_arrow, arrow_rect)

                # 캐릭터 이미지 출력

                # 체력 이미지 출력 파트
                temp_1 = (self.player1.hp-1)//20
                for i in range(5):
                    # gameDisplay.blit(player11.hp_img[i], (50* (i+1), 250))
                    pos_x = 60 * (i+1)
                    if i < temp_1:
                        self.gameDisplay.blit(self.player1.img_hp[0], (pos_x, 150))
                    elif i > temp_1:
                        self.gameDisplay.blit(self.player1.img_hp[6], (pos_x, 150))
                    elif i == temp_1:
                        if self.player1.hp % 20 == 0:
                            self.gameDisplay.blit(self.player1.img_hp[0], (pos_x, 150))
                        elif self.player1.hp % 20 >= 17:
                            self.gameDisplay.blit(self.player1.img_hp[1], (pos_x, 150))
                        elif self.player1.hp % 20 >= 13:
                            self.gameDisplay.blit(self.player1.img_hp[2], (pos_x, 150))
                        elif self.player1.hp % 20 >= 9:
                            self.gameDisplay.blit(self.player1.img_hp[3], (pos_x, 150))
                        elif self.player1.hp % 20 >= 5:
                            self.gameDisplay.blit(self.player1.img_hp[4], (pos_x, 150))
                        else:
                            self.gameDisplay.blit(self.player1.img_hp[5], (pos_x, 150))
                
                temp_2 = (self.player2.hp-1)//20
                for i in range(5):
                    # gameDisplay.blit(player21.hp_img[i], (50* (i+1), 250))
                    pos_x = 1220 - 60*(i+1)
                    if i < temp_2:
                        self.gameDisplay.blit(self.player2.img_hp[0], (pos_x, 150))
                    elif i > temp_2:
                        self.gameDisplay.blit(self.player2.img_hp[6], (pos_x, 150))
                    elif i == temp_2:
                        if self.player2.hp % 20 == 0:
                            self.gameDisplay.blit(self.player2.img_hp[0], (pos_x, 150))
                        elif self.player2.hp % 20 >= 17:
                            self.gameDisplay.blit(self.player2.img_hp[1], (pos_x, 150))
                        elif self.player2.hp % 20 >= 13:
                            self.gameDisplay.blit(self.player2.img_hp[2], (pos_x, 150))
                        elif self.player2.hp % 20 >= 9:
                            self.gameDisplay.blit(self.player2.img_hp[3], (pos_x, 150))
                        elif self.player2.hp % 20 >= 5:
                            self.gameDisplay.blit(self.player2.img_hp[4], (pos_x, 150))
                        else:
                            self.gameDisplay.blit(self.player2.img_hp[5], (pos_x, 150))
                # 전역 변수의 win이 있다면 while문 종료
                pygame.display.update()
                self.clock.tick(20)

            while game_trigger == 3 : # 클라이언트 대기 부분
                tmr = tmr + 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F1:
                            self.gameDisplay = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                        if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                            self.gameDisplay = pygame.display.set_mode((1280, 720))
                
                self.gameDisplay.blit(self.bg_main[tmr%4], [0, 0])   # 초당 프레임 수
                
                # 배경음악
                if pygame.mixer.get_busy() == False:
                    # main_bgm.play()
                    pass
                # 버튼만들기 Button(img, x, y , he, w , act_img,  act_x, act_y, func)
                pygame.display.update()
                self.clock.tick(7)
            
        
    
    def explain(self):
        exp = True
        tip = False
        def switch():
            # 로컬 변수로 tip 받아서 반대로 변환
            nonlocal tip
            if tip:
                tip = False
            else:
                tip = True
            return tip
        while exp:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # tip이 켜지면 tip 페이지로, 아니면 설명 페이지로 출력
            if not tip:
                self.gameDisplay.blit(self.bg_explain, (0, 0))
                self.Button(self.right_button, 1150, 350, 100, 100, self.right_button, 1150, 350, self.gameDisplay,switch)
            else:
                self.gameDisplay.blit(self.bg_tip, (0, 0))
                self.Button(self.left_button, 50, 350, 100, 100, self.left_button, 50, 350, self.gameDisplay,switch)
                
            self.Button(self.back, 300, 600, 230, 140, self.back_click, 300, 600, self.gameDisplay, self.game_on)
            
            pygame.display.update()
            self.clock.tick(15)


    def ready(self):
        global game_trigger
        game_trigger = 3
        self.player1 = self.Player([100, 550], 1)
        self.player2 = self.Player([1100, 550], 2)
        
    def shot(self, player):
        global client_socket, game_trigger
        temp_list = [player.position, player.angle, player.gauge]
        data_bytes = pickle.dumps(temp_list)
        client_socket.send(data_bytes)
        game_trigger = 2
        player.gauge = 0
        # self.player.position
        # self.player.angle
        # self.player.gauge

# 플레이어 클래스
    class Player:
        
        def __init__(self, initial_position, side):
            self.img_hp = [
            pygame.transform.scale(pygame.image.load("./hp_img/hp_6.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_5.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_4.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_3.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_2.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_1.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_0.png"), (50, 50)),
        ]
            self.initial_position = initial_position[:]
            self.position = initial_position
            self.name = 'player' + str(side)
            self.damage = 20
            self.volume = 125  #74
            self.side = side
            self.hp = 100
            self.gauge = 0
            self.body = [initial_position[0]+24, initial_position[1]+24]
            if side == 1:
                self.angle = 0
            elif side == 2:
                self.angle = 180
            self.hp_img = [self.img_hp[0]]*5

        def move(self, dx, dy):
            self.position[0] += dx
            self.position[1] += dy
            self.body[0] += dx
            self.body[1] += dy
            
        def hit(self, damage, scale):
            self.hp = round(self.hp - (damage * scale))
            idx = self.hp // 20
            # if self.hp % 20 != 0:
            #     self.hp_img[idx] = img_hp[5-(self.hp % 20)//6]
            # else:
            #     self.hp_img[idx] = img_hp[6]

        
        def angle_move(self, theta):
            if self.side == 1:
                self.angle += theta
            elif self.side == 2:
                self.angle -= theta

        def charge(self, power):
            self.gauge += power
        

# 환경 클래스
    class Environment:
        season = 'spring'
        def __init__(self):
            self.element(self.season)
        
        #turn을 인자로 받아 계절 계산
        def season_check(self, turn):
            if 1 <= turn < 5:
                self.season = 'spring'
            elif 5 <= turn < 8:
                self.season = 'summer'
            elif 8 <= turn < 12:
                self.season = 'autumn'
            else:
                self.season = 'winter'
            self.element(self.season)
            
        # 계절을 인자로 받아 풍속, 풍향, 저항, 데미지 스케일 조정
        def element(self, season):
            if season == 'spring':
                wind_velocity = list(range(11))
                wind_angle = list(range(0, 190, 10))
                self.resistance = 0
                self.damage_scale = 1
            elif season == 'summer':
                wind_velocity = list(range(21))
                wind_angle = list(range(0, 190, 10))
                self.resistance = 0.2
                self.damage_scale = 0.7
            elif season == 'autumn':
                wind_velocity = list(range(11))
                wind_angle = list(range(0, 190, 10))
                self.resistance = 0
                self.damage_scale = 2
            elif season == 'winter':
                wind_velocity = list(range(21))
                wind_angle = list(range(0, 190, 10))
                self.resistance = 0.1
                self.damage_scale = 1.2
                
            self.v_w = wind_velocity[np.random.randint(0, len(wind_velocity)-1)]
            self.theta_w = wind_angle[np.random.randint(0, len(wind_angle)-1)]

# 버튼 클래스
    class Button:  # 버튼
        def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, gameDisplay, action=None):
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


    
def client_start():
    global game_trigger, client_socket
    pygame.init()
    client = display_fortress()
    client.game_start()
    while game_trigger == 0 :
        ...
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))    
    
    data = client_socket.recv(1024).decode('utf-8') # 클라이언트한테 시작신호 받기
        
    if "시작" in data :
        player_num = client_socket.recv(4096)
        temp_list = pickle.loads(player_num)
        
        client.player = int(temp_list.pop())
        client.environment = temp_list.pop()
        client.turn = temp_list.pop()
        
        while True :
            if client.player == (2-(client.turn%2)) :
                print(1)
                game_trigger = 1
                while game_trigger == 1 :
                    ...
            else :
                print(2)
                game_trigger = 2
            recv_data = client_socket.recv(4096)
            print("난 받았어")
            result_data = pickle.loads(recv_data)
            client.player1.position = result_data[0][0]
            client.player1.angle = result_data[0][1]
            client.player1.hp = result_data[0][2]
            
            client.player2.position = result_data[1][0]
            client.player2.angle = result_data[1][1]
            client.player2.hp = result_data[1][2]
            
            client.turn = result_data[2]
            client.environment = result_data[3]
        
        
'''
result_list = [
            [server.player1.position, server.player1.angle, server.player1.hp],
            [server.player2.position, server.player2.angle, server.player2.hp],
            server.turn,
            server.environment,
            ]
'''

# 실행 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    client_start()

