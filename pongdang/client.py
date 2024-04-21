import pygame
import time
import random
import math
import sys
import socket
from _thread import *
from threading import Thread
import pickle

HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
NAME = "최봉준" #이름을 입력해주세요

pygame.init()

# 아이콘 이미지
new_icon = pygame.image.load("image/ball4.png")
new_icon=pygame.transform.scale(new_icon, (30, 30))
pygame.display.set_icon(new_icon)

# BGM 넣기

fallSound=pygame.mixer.Sound('music/effect_fall.wav')
hitSound=pygame.mixer.Sound('music/hit.wav')
hitSound2=pygame.mixer.Sound('music/hit2.wav')
effect_ending=pygame.mixer.Sound('music/effect_ending.wav')

# 스타트 페이지 이미지
background_start = [pygame.image.load(f"./image/main_background/{i}.png") for i in range(92)] # 스타트 배경
background_start = [pygame.transform.scale(image, (650, 977))for image in background_start]
title_start=pygame.image.load('image/title.png')
title_start=pygame.transform.scale(title_start, (577, 303))
btn_start = pygame.image.load("./image/start_btn.png") # 스타트 버튼
btn_start = pygame.transform.scale(btn_start, (350, 147))
btn_start_click = pygame.image.load("./image/start_btn2.png") # 클릭시 스타트 버튼
btn_start_click = pygame.transform.scale(btn_start_click, (350, 147))

# 플레이 페이지 이미지
background_play = [pygame.image.load(f"./image/background/background_{i}.png") for i in range(4)]

background_play = [pygame.transform.scale(image, (650, 977)) for image in background_play]
background_land_play = pygame.image.load("./image/land.jpg") # 플레이 배경
background_land_play = pygame.transform.scale(background_land_play, (630, 630))

play_background_top=[pygame.image.load(f"./image/play_background_top/{i}.png") for i in range(12)]
play_background_top = [pygame.transform.scale(image, (650, 224)) for image in play_background_top]
play_background_bt=[pygame.image.load(f"./image/play_background_bt/{i}.png") for i in range(12)]
play_background_bt = [pygame.transform.scale(image, (650, 224)) for image in play_background_bt]

sand_background=[pygame.image.load(f"./image/sand_crop/{i}.png") for i in range(10)]

moving_in=[pygame.image.load(f"./image/moving_in{i}.png") for i in range(1,4)]
moving_in = [pygame.transform.scale(image, (350, 147)) for image in moving_in]

# 앤드 페이지 이미지
background_end=pygame.image.load('image/ending_background.jpg')
background_end=pygame.transform.scale(background_end, (650, 977))
btn_end = pygame.image.load("./image/ending_replay_click.png") # 리플레이 버튼
btn_end = pygame.transform.scale(btn_end, (350, 147))
btn_end_click = pygame.image.load("./image/ending_replay.png") # 클릭시 리플레이 버튼
btn_end_click = pygame.transform.scale(btn_end_click, (350, 147))

winner_1=pygame.image.load("image/ending_player1_win.png")
winner_1=pygame.transform.scale(winner_1, (579, 277))
winner_2=pygame.image.load("image/ending_player2_win.png")
winner_2=pygame.transform.scale(winner_2, (579, 277))
winner=0

# 디스플레이 창 크기 설정
display_width = 650 # 가로 사이즈
display_height = 977 # 세로 사이즈

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("PONGDANG")

# 시작 버튼 스타트 배경 위에 blit
button_x = (display_width - btn_start.get_width()) // 2  # 가로 위치
button_y = (display_height - btn_start.get_height()) // 1.3  # 세로 위치
gameDisplay.blit(btn_start, (button_x, button_y)) # 버튼 built

# 배경 이미지 인덱스
current_background_index = 0
next_change_time = pygame.time.get_ticks() + 300  # 3초마다 이미지 변경

# 스타트 배경 bilt


#메인 게임 필요 변수, 함수
def load_scaled_image(filepath, new_size):
    """ 이미지를 불러와서 지정된 크기로 조정합니다. """
    image = pygame.image.load(filepath).convert_alpha()  # 이미지를 불러옵니다.
    return pygame.transform.scale(image, new_size)  # 이미지의 크기를 조정합니다.


FIELD_WIDTH, FIELD_HEIGHT = 630, 630
FIELD_X, FIELD_Y = (display_width - FIELD_WIDTH) // 2, (display_height - FIELD_HEIGHT) // 2
CAP_RADIUS = 25
MAX_CAPS = 5  # Each player has 5 caps
font = pygame.font.Font(None, 36)
player_images = [
    load_scaled_image('image/ball7.png', (50, 50)),  # 플레이어 1 이미지
    load_scaled_image('image/ball8.png', (50, 50))   # 플레이어 2 이미지
]
current_player = 0
total_players = 2
caps_set = [0, 0]  # Tracks the number of caps set by each player
caps = []
movement_started = False
start_time = None

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

def game():
    ...

def main():
    global start_cnt, client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    # print(client_socket.recv(1024).decode('utf-8'))
    start_cnt = 0
    loading_1 = Thread(target = loading) #Thread 활용해서 클라이언트 정보받기랑 로딩화면 띄우기 따로 처리
    loading_1.start()
    
    data = client_socket.recv(1024).decode('utf-8') # 클라이언트한테 시작신호 받기
        # print(data)
    if "시작" in data: # 넘어갈 수 있게 
        start_cnt = 1
        received_data = client_socket.recv(4096) # 리스트 형태인 초기 setting 값 받기
        # 딕셔너리 형태도 똑같이 진행
        received_list = pickle.loads(received_data) # 초기 setting 값 역직렬화
        game()
        
def loading():
    global start_cnt, next_change_time,current_background_index
    while start_cnt == 0 : # 신호받기 전까지 화면 송출
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = pygame.mouse.get_pos()

        # 마우스 위치 확인
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_x, mouse_y = mouse_pos
        # if pygame.time.get_ticks() >= next_change_time:
        current_background_index = (current_background_index + 1) % len(background_start)
            # next_change_time += 80  # 3초 추가
        time.sleep(0.1)
        gameDisplay.blit(background_start[current_background_index], (0, 0))
        # gameDisplay.blit(background_start, (0, 0))
        gameDisplay.blit(title_start,(36,240))
        
        pygame.display.update()


def start_page():
    global next_change_time,current_background_index
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/start_bgm_1.mp3')
    pygame.mixer.music.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = pygame.mouse.get_pos()

        # 마우스 위치 확인
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_x, mouse_y = mouse_pos
        # if pygame.time.get_ticks() >= next_change_time:
        current_background_index = (current_background_index + 1) % len(background_start)
            # next_change_time += 80  # 3초 추가
        time.sleep(0.1)
        gameDisplay.blit(background_start[current_background_index], (0, 0))
        # gameDisplay.blit(background_start, (0, 0))
        gameDisplay.blit(title_start,(36,240))
        Button(btn_start, button_x, button_y, 350, 147, btn_start_click, button_x, button_y, main)
        
        pygame.display.update()
    


if __name__ == '__main__':
    start_page()