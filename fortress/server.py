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
# 변수 영역 //////////////////////////////////////////////////
game_trigger = 0
WHITE = (255,255,255)
RED = (255, 10, 10)
BLACK = (0,0,0)
display_width = 1280
display_height = 720
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
        self.cannon_effect_sound = [
            pygame.mixer.Sound('./bgm/cannon_fire_0.mp3'),
            pygame.mixer.Sound('./bgm/cannon_fire_1.mp3'),
        ]

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

        # 새로운 아이콘 이미지 로드
        self.new_icon = pygame.image.load("./img/heart_icon.png")

        
        self.img_hp = [
            pygame.transform.scale(pygame.image.load("./hp_img/hp_6.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_5.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_4.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_3.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_2.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_1.png"), (50, 50)),
            pygame.transform.scale(pygame.image.load("./hp_img/hp_0.png"), (50, 50)),
        ]



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
        global game_trigger, client_sockets
        # 메인 bgm 적용
        pygame.display.set_icon(self.new_icon)
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("LOVEBOMB")
        
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
            if len(client_sockets) > 1:
                self.Button(self.mainmenu_start, 680, 550, 300, 50, self.mainmenu_start_click, 680, 550, self.gameDisplay, self.ready)
            pygame.display.update()
            self.clock.tick(7)
            
        while True :
            while game_trigger == 1 : # 1P가 발사하는 부분
                if self.turn % 2 == 1:
                    player = self.player1
                else:
                    player = self.player2
                v_w, theta_w, k, scale = self.environment.v_w, self.environment.theta_w, self.environment.resistance, self.environment.damage_scale
                print(player.gauge, player.angle)
                # 플레이어 클래스의 게이지, 각도와 풍속, 풍향, 저항을 사용하여 x 좌표 리스트와 y좌표 리스트 추출
                x_coord, y_coord = coord(player, v_w, theta_w, k)

                txt_angle_1 = self.font.render(str(self.player1.angle), True, BLACK)
                txt_angle_2 = self.font.render(str(180 - self.player2.angle), True, BLACK)
                txt_velocity = self.font.render(f'{self.environment.v_w}m/s', True, BLACK)
                velocity_rect = txt_velocity.get_rect(center = (640, 180))

                # 배경이미지
                if self.environment.season == 'spring':
                    background = pygame.image.load("./img/spring_bg.png")
                elif self.environment.season == 'summer':
                    background = pygame.image.load("./img/summer_bg.png")
                elif self.environment.season == 'autumn':
                    background = pygame.image.load("./img/fall_bg.png")
                elif self.environment.season == 'winter':
                    background = pygame.image.load("./img/winter_bg.png")

            
                rotated_image1 = pygame.transform.rotate(self.cannon_body1, self.player1.angle)
                new_rect1 = rotated_image1.get_rect(center=self.cannon_body1.get_rect(center=[self.player1.position[0]+24,self.player1.position[1]+24]).center)

                rotated_image2 = pygame.transform.rotate(self.cannon_body2, self.player2.angle-180)
                new_rect2 = rotated_image2.get_rect(center=self.cannon_body2.get_rect(center=[self.player2.position[0]+24,self.player2.position[1]+24]).center)
                
                rotate_arrow = pygame.transform.rotate(self.wind_direction, -self.environment.theta_w)
                arrow_rect = rotate_arrow.get_rect(center = (640, 100))

                # 좌표에 따른 이미지 출력 부분
                # idx를 하나씩 올리며 포탄 이미지 출력
                idx = 0
                self.cannon_effect_sound[random.choice(range(0,2))].play()
                while idx < len(x_coord):
                    # 발사
                    
                    # 배경 -> 대포 -> 포탄 순으로 출력하면서 이전 포탄을 덮는 느낌으로 ㄱㄱ
                    
                    self.gameDisplay.blit(background, (0, 0))  # 배경 이미지
                    # gameDisplay.fill(WHITE)
                    
                    self.gameDisplay.blit(self.shell, (x_coord[idx], y_coord[idx]))
                    
                    self.gameDisplay.blit(self.character1, (self.player1.position[0]-100, self.player1.position[1]-80))
                    self.gameDisplay.blit(self.character2, (self.player2.position[0]-20, self.player2.position[1]-80))
                    
                    self.gameDisplay.blit(rotated_image1, new_rect1)  # 회전한 대포1
                    self.gameDisplay.blit(self.cannon_wheel,(self.player1.position[0], self.player1.position[1]+10))  # 바퀴 이미지
                    self.gameDisplay.blit(rotated_image2, new_rect2)  # 회전한 대포2
                    self.gameDisplay.blit(self.cannon_wheel,(self.player2.position[0], self.player2.position[1]+10))  # 바퀴 이미지
                    

                    # gameDisplay.blit(txt,(0,0))
                    
                    # 캐릭터 이미지 출력
                    
                    # 풍향 출력
                    
                    self.gameDisplay.blit(rotate_arrow, arrow_rect)
                    
                    self.gameDisplay.blit(txt_velocity, velocity_rect)
                    
                    # 체력 이미지 출력 파트self.
                    temp_1 = (self.player1.hp-1)//20
                    for i in range(5):
                        pos_x = 60 * (i+1)
                        if i < temp_1:
                            self.gameDisplay.blit(self.img_hp[0], (pos_x, 150))
                        elif i > temp_1:
                            self.gameDisplay.blit(self.img_hp[6], (pos_x, 150))
                        elif i == temp_1:
                            if self.player1.hp % 20 == 0:
                                self.gameDisplay.blit(self.img_hp[0], (pos_x, 150))
                            elif self.player1.hp % 20 >= 17:
                                self.gameDisplay.blit(self.img_hp[1], (pos_x, 150))
                            elif self.player1.hp % 20 >= 13:
                                self.gameDisplay.blit(self.img_hp[2], (pos_x, 150))
                            elif self.player1.hp % 20 >= 9:
                                self.gameDisplay.blit(self.img_hp[3], (pos_x, 150))
                            elif self.player1.hp % 20 >= 5:
                                self.gameDisplay.blit(self.img_hp[4], (pos_x, 150))
                            else:
                                self.gameDisplay.blit(self.img_hp[5], (pos_x, 150))
                    
                    temp_2 = (self.player2.hp-1)//20
                    for i in range(5):
                        pos_x = 1220 - 60*(i+1)
                        if i < temp_2:
                            self.gameDisplay.blit(self.img_hp[0], (pos_x, 150))
                        elif i > temp_2:
                            self.gameDisplay.blit(self.img_hp[6], (pos_x, 150))
                        elif i == temp_2:
                            if self.player2.hp % 20 == 0:
                                self.gameDisplay.blit(self.img_hp[0], (pos_x, 150))
                            elif self.player2.hp % 20 >= 17:
                                self.gameDisplay.blit(self.img_hp[1], (pos_x, 150))
                            elif self.player2.hp % 20 >= 13:
                                self.gameDisplay.blit(self.img_hp[2], (pos_x, 150))
                            elif self.player2.hp % 20 >= 9:
                                self.gameDisplay.blit(self.img_hp[3], (pos_x, 150))
                            elif self.player2.hp % 20 >= 5:
                                self.gameDisplay.blit(self.img_hp[4], (pos_x, 150))
                            else:
                                self.gameDisplay.blit(self.img_hp[5], (pos_x, 150))
                    pygame.display.update()
                    idx += 1
                    self.clock.tick(200)
                
                # 마지막 x 좌표와 y 좌표가 impact
                impact = (x_coord[idx-1], y_coord[idx-1])
                print(f'position : {player.position}')
                print(f'start : {(x_coord[0], y_coord[0])}')
                print(f'impact : {impact}')

                
                # 현재 플레이어와 impact, 계절의 데미지 스케일로 피격 판정
                self.calculate(player, impact, scale)
                game_trigger = 3
                # 그 후 턴 증가
                self.turn += 1
                # 턴에 따라 환경의 계절 조정
                self.environment.season_check(self.turn)
                # 플레이어가 움직였던 거리 초기화

            while game_trigger == 3 : # 클라이언트 대기 부분
                
                if self.win:
                    break
                
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
            
            if self.win :
                self.game_over(self.win, self.defeated)
                
            
        
    
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
        
    def calculate(self, player, impact, scale):

        # 현재 플레이어의 side에 따라 상대 지정
        if player.side == 1:
            enemy = self.player2
        elif player.side == 2:
            enemy = self.player1
        
        # 충돌 판정
        if impact[0] - enemy.volume <= enemy.position[0] <= impact[0] + enemy.volume:
            enemy.hit(player.damage, scale)
            # 충돌시 bgm
            self.bomb_sound.play()
            
            # 맞고 hp가 0 이하가 되면 승자와 패자 결정
            if enemy.hp <= 0:
                self.win = player.name
                self.defeated = enemy.name
        
    def game_over(self, win, defeated):
        game_over = True
        bg_main = [pygame.image.load(f"./ending_img/{i}.png") for i in range(147)]
        # 화면에 맞게 이미지 크기 조정
        bg_main = [pygame.transform.scale(image, (display_width, display_height)) for image in bg_main]
        
        # 엔딩 bgm
        pygame.mixer.music.load('./bgm/ending_bgm.mp3')
        pygame.mixer.music.play()
        
        # 문구 출력용
        text_1 = f'마침내 {win}의 진심이 통했다...'
        text_2 = f'{win}의 열렬한 구애에 {defeated}의 철벽은 속절없이 함락당하고 말았다.'
        text_3 = f'영원한 사랑의 노예가 되어버린 {defeated}...'
        text_4 = f'하지만 걱정 마라. 사랑은 이기고 지는 게 아니니까.'

        win_text_1 = self.korean_font.render(text_1, True, WHITE)
        win_text_2 = self.korean_font.render(text_2, True, WHITE)
        win_text_3 = self.korean_font.render(text_3, True, WHITE)
        win_text_4 = self.korean_font.render(text_4, True, WHITE)
        
        win_rect_1 = win_text_1.get_rect(center = (640, 200))
        win_rect_2 = win_text_2.get_rect(center = (640, 300))
        win_rect_3 = win_text_3.get_rect(center = (640, 400))
        win_rect_4 = win_text_4.get_rect(center = (640, 500))
        
        
        cur_idx = 0
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            display_idx = cur_idx % len(bg_main)
            time.sleep(0.1)
            # next_level += 500  # 3초 추가
            self.gameDisplay.blit(bg_main[display_idx], (0, 0))
            self.gameDisplay.blit(self.ending_bg, self.ending_rect)
            self.gameDisplay.blit(win_text_1, win_rect_1)
            self.gameDisplay.blit(win_text_2, win_rect_2)
            self.gameDisplay.blit(win_text_3, win_rect_3)
            self.gameDisplay.blit(win_text_4, win_rect_4)
            pygame.display.update() # 화면 업데이트
            cur_idx += 1
            self.clock.tick(15) #프레임 레이트 지정

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
            self.body = [self.position[0]+24, self.position[1]+24]
            if side == 1:
                self.angle = 0
            elif side == 2:
                self.angle = 180
            self.hp_img = [self.img_hp[0]]*5
            
        # def get_body(self) :
        #     return [x+self.body for x in self.position]
        
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




    

    

def handle_client(client_socket, server):
    global client_sockets, game_trigger
    while game_trigger == 0 :
        ...
    
    client_socket.sendall("시작".encode('utf-8'))
    
    
    if not server.environment :
        server.environment = server.Environment()
    
    temp_setting = []
    temp_setting.append(server.turn)
    temp_setting.append(server.environment)
    temp_setting.append(str(client_sockets.index(client_socket)+1))
    
    data_bytes = pickle.dumps(temp_setting)
    client_socket.send(data_bytes)
    while True :
        if client_socket == client_sockets[1-(server.turn%2)]:
            print("한번만 나오셈")
            recv_info = client_socket.recv(4096)
            recv_list = pickle.loads(recv_info)
            if 1 == (2-(server.turn%2)):
                server.player1.position = recv_list[0]
                server.player1.angle = recv_list[1]
                server.player1.gauge = recv_list[2]
                game_trigger = 1
            else :
                server.player2.position = recv_list[0]
                server.player2.angle = recv_list[1]
                server.player2.gauge = recv_list[2]
                game_trigger = 1
        
        if game_trigger == 3 :
            continue
        
        while game_trigger == 1 :
            ...
        
        
        

        result_list = [
            [server.player1.position, server.player1.angle, server.player1.hp],
            [server.player2.position, server.player2.angle, server.player2.hp],
            server.turn,
            server.environment,
            ]
        
        result_data = pickle.dumps(result_list)
        client_socket.sendall(result_data)
        
    
    
    
def server_start():
    pygame.init()
    server = display_fortress()
    server.game_start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #소켓 연결
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print("Server started, listening on port", PORT)
        
        conn1, addr1 = server_socket.accept()
        client_sockets.append(conn1)
        print("Client connected", addr1)
        print("참가자 수 : ", len(client_sockets))
        start_new_thread(handle_client, (conn1, server))
        
        conn2, addr2 = server_socket.accept()
        client_sockets.append(conn2)
        print("Client connected", addr2)
        print("참가자 수 : ", len(client_sockets))
        start_new_thread(handle_client, (conn2, server))

# 실행 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    server_start()

