import socket
import random
import pygame
from _thread import *
import sys
import time
from threading import Thread
import pickle

HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
display_width = 650 # 가로 사이즈
display_height = 977 # 세로 사이즈
client_sockets = []
tri_ready = 0

class server_pongdang:
    def __init__(self) -> None:
        # 아이콘 이미지
        self.new_icon = pygame.image.load("image/ball4.png")
        self.new_icon=pygame.transform.scale(self.new_icon, (30, 30))

        # BGM 넣기
        self.fallSound=pygame.mixer.Sound('music/effect_fall.wav')
        self.hitSound=pygame.mixer.Sound('music/hit.wav')
        self.hitSound2=pygame.mixer.Sound('music/hit2.wav')
        self.effect_ending=pygame.mixer.Sound('music/effect_ending.wav')
        
        # 스타트 페이지 이미지
        self.background_start = [pygame.image.load(f"./image/main_background/{i}.png") for i in range(92)] # 스타트 배경
        self.background_start = [pygame.transform.scale(image, (650, 977))for image in self.background_start]
        self.title_start=pygame.image.load('image/title.png')
        self.title_start=pygame.transform.scale(self.title_start, (577, 303))
        self.btn_start = pygame.image.load("./image/start_btn.png") # 스타트 버튼
        self.btn_start = pygame.transform.scale(self.btn_start, (350, 147))
        self.btn_start_click = pygame.image.load("./image/start_btn2.png") # 클릭시 스타트 버튼
        self.btn_start_click = pygame.transform.scale(self.btn_start_click, (350, 147))
        
        # 플레이 페이지 이미지
        self.background_play = [pygame.image.load(f"./image/background/background_{i}.png") for i in range(4)]
        self.background_play = [pygame.transform.scale(image, (650, 977)) for image in self.background_play]
        self.sharkfin_play = [pygame.image.load(f"./image/sharkfin/{i}.png") for i in range(10)]

        self.background_land_play = pygame.image.load("./image/land.jpg") # 플레이 배경
        self.background_land_play = pygame.transform.scale(self.background_land_play, (630, 630))

        self.play_background_top=[pygame.image.load(f"./image/play_background_top/{i}.png") for i in range(12)]
        self.play_background_top = [pygame.transform.scale(image, (650, 224)) for image in self.play_background_top]
        self.play_background_bt=[pygame.image.load(f"./image/play_background_bt/{i}.png") for i in range(12)]
        self.play_background_bt = [pygame.transform.scale(image, (650, 224)) for image in self.play_background_bt]

        self.sand_background=[pygame.image.load(f"./image/sand_crop/{i}.png") for i in range(10)]

        self.moving_in=[pygame.image.load(f"./image/moving_in{i}.png") for i in range(1,4)]
        self.moving_in = [pygame.transform.scale(image, (350, 147)) for image in self.moving_in]

        # 앤드 페이지 이미지
        self.background_end=pygame.image.load('image/ending_background.jpg')
        self.background_end=pygame.transform.scale(self.background_end, (650, 977))
        self.btn_end = pygame.image.load("./image/ending_replay_click.png") # 리플레이 버튼
        self.btn_end = pygame.transform.scale(self.btn_end, (350, 147))
        self.btn_end_click = pygame.image.load("./image/ending_replay.png") # 클릭시 리플레이 버튼
        self.btn_end_click = pygame.transform.scale(self.btn_end_click, (350, 147))

        self.winner_1=pygame.image.load("image/ending_player1_win.png")
        self.winner_1=pygame.transform.scale(self.winner_1, (579, 277))
        self.winner_2=pygame.image.load("image/ending_player2_win.png")
        self.winner_2=pygame.transform.scale(self.winner_2, (579, 277))
        self.winner = 0
        
    def game_on(self):
        pygame.display.set_icon(self.new_icon)
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("PONGDANG")
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/start_bgm_1.mp3')
        pygame.mixer.music.play()
        
        
        button_x = (display_width - self.btn_start.get_width()) // 2  # 가로 위치
        button_y = (display_height - self.btn_start.get_height()) // 1.3  # 세로 위치
        
        current_background_index = 0
        current_background_index_shark=0

        
        
        def button(img_in, x, y, width, height, img_act, x_act, y_act, action=None):
            mouse = pygame.mouse.get_pos()  # 마우스 좌표
            click = pygame.mouse.get_pressed()  # 클릭여부
            if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
                self.gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
                if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                    time.sleep(0.2)
                    action()
            else:
                self.gameDisplay.blit(img_in, (x, y))

        # 대기 화면 ---------------------------------------------------
        while len(client_sockets) < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                    # mouse_pos = pygame.mouse.get_pos()

            # 마우스 위치 확인
            # mouse_pos = pygame.mouse.get_pos()
            # mouse_x, mouse_y = mouse_pos
            # if pygame.time.get_ticks() >= next_change_time:
            current_background_index = (current_background_index + 1) % len(self.background_play)
            current_background_index_shark = (current_background_index_shark + 1) % len(self.sharkfin_play)
                # next_change_time += 80  # 3초 추가
            time.sleep(0.15)
            self.gameDisplay.blit(self.background_play[current_background_index], (0, 0))
            self.gameDisplay.blit(self.sharkfin_play[current_background_index_shark], (75, 200))
            # gameDisplay.blit(background_start, (0, 0))
            # self.gameDisplay.blit(self.title_start,(36,240))
            # button(self.btn_start, button_x, button_y, 350, 147, self.btn_start_click, button_x, button_y, main)
            # 버튼 누를 시 tri_ready=1로 만들어서 게임 시작
            pygame.display.update()
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/start_bgm_1.mp3')
        pygame.mixer.music.play()
        # 게임 화면 ----------------------------------------------------------------
        while tri_ready == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                    # mouse_pos = pygame.mouse.get_pos()

            # 마우스 위치 확인
            # mouse_pos = pygame.mouse.get_pos()
            # mouse_x, mouse_y = mouse_pos
            current_background_index=0
            # if pygame.time.get_ticks() >= next_change_time:
            current_background_index = (current_background_index + 1) % len(self.background_start)
                # next_change_time += 80  # 3초 추가
            time.sleep(0.1)
            self.gameDisplay.blit(self.background_start[current_background_index], (0, 0))
            
            self.gameDisplay.blit(self.title_start,(36,240))
            button(self.btn_start, button_x, button_y, 350, 147, self.btn_start_click, button_x, button_y, main)
            # 버튼 누를 시 tri_ready=1로 만들어서 게임 시작
            pygame.display.update()
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/main_bgm_1.mp3')
        pygame.mixer.music.play()
        # 게임 화면 ----------------------------------------------------------------
        while tri_ready == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
    def game_start(self):
        ready_bg = Thread(target= self.game_on)
        ready_bg.start()
        
# 버튼 누를 시 tri_ready=1로 만들어서 게임 시작
def start():
    global tri_ready
    tri_ready = 1

def handle_client(client_socket, _):
    global client_sockets, tri_ready
    # 게임 준비 --------------------------------------------------------
    while tri_ready == 0 :
        if tri_ready == 1 : # 모든 클라이언트들한테 시작 신호전달
            for client in client_sockets:
                client.send("시작".encode('utf-8'))
    
    # 시작하기 전에 공의 랜덤 위치와 플레이어 지정 신호를 클라이언트한테 전달 해야됨---------------
    # info_settings = [공의위치, 플레이어 지정 및 등등]
    # data_bytes = pickle.dumps(info_settings) # pickle 모듈을 활용한 데이터 직렬화
    # 딕셔너리 형태도 똑같이 진행
    # for client in client_sockets:
    #   client_socket.send(data_bytes) # 리스트 형태로 보내줌
    
    # 게임 시작 ----------------------------------------------------
    while tri_ready == 1 :
        player_info = client_socket.recv(1024).decode('utf-8') #각 클라이언트한테 정보 받기


def main():
    pygame.init()
    # 아이콘 이미지
    a = server_pongdang() # 이거는 화면송출 클래스
    a.game_start() # Thread 이용해서 클라이언트 관리와 화면 송출을 따로 관리함

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #소켓 연결
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started, listening on port", PORT)
        while len(client_sockets) < 2 :
            client_socket, _ = server_socket.accept()
            client_sockets.append(client_socket)
            print("Client connected")
            print("참가자 수 : ", len(client_sockets))
            start_new_thread(handle_client, (client_socket, _))

    

if __name__ == "__main__":
    main()