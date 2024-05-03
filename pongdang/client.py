import socket
import random,math
import pygame
from _thread import *
import sys
import time
from threading import Thread
import pickle
server_run = True
HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
display_width = 650 # 가로 사이즈
display_height = 977 # 세로 사이즈
FIELD_WIDTH, FIELD_HEIGHT = 630, 630
FIELD_X, FIELD_Y = (display_width - FIELD_WIDTH) // 2, (display_height - FIELD_HEIGHT) // 2
CAP_RADIUS = 25
MAX_CAPS = 5  # Each player has 5 caps
current_player = 0
total_players = 2
start_cnt = -1
movement_started = False
start_time = None
class client_pongdang:
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

        self.sand_background=[pygame.image.load(f"./image/sandcrop/{i}.png") for i in range(10)]
        self.player_ball=[pygame.image.load(f"./image/ball{i}.png") for i in range(7,9)]
        self.player_ball = [pygame.transform.scale(image, (50, 50)) for image in self.player_ball]

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
        
        self.caps = []
        self.me = 0
        self.caps_set = [0, 0]
        
    def game_on(self):
        global start_cnt,start_time, server_run, dragging_start_pos
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

        self.font = pygame.font.Font(None, 36)
        self.player_images = [
            ('image/ball7.png', (50, 50)),  # 플레이어 1 이미지
            ('image/ball8.png', (50, 50))   # 플레이어 2 이미지
        ]
        self.draw_player_images = [
            load_scaled_image('image/ball7.png', (50, 50)),  # 플레이어 1 이미지
            load_scaled_image('image/ball8.png', (50, 50))   # 플레이어 2 이미지
        ]
        
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
        while start_cnt == -1 :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            current_background_index = (current_background_index + 1) % len(self.background_play)
            time.sleep(0.15)
            self.gameDisplay.blit(self.background_start[current_background_index], (0, 0))
            
            self.gameDisplay.blit(self.title_start,(36,240))
            button(self.btn_start, button_x, button_y, 350, 147, self.btn_start_click, button_x, button_y, start)
            pygame.display.update()
        

        while start_cnt == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            current_background_index = (current_background_index + 1) % len(self.background_start)

            time.sleep(0.1)
            self.gameDisplay.blit(self.background_start[current_background_index], (0, 0))

            self.gameDisplay.blit(self.title_start,(36,240))
            pygame.display.update()
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/main_bgm_1.mp3')
        pygame.mixer.music.play()
        
        current_background_index = 0
        self.winner = None
        dragging_start_pos = None  # Track the start position of a drag
        # 게임 화면 ----------------------------------------------------------------
        next_change_time = pygame.time.get_ticks()
        while True :
            while start_cnt == 1 :
                # 배경 이미지 변경
            
                if pygame.time.get_ticks() >= next_change_time:
                    next_change_time += 300  # 3초 추가
                    current_background_index = (current_background_index + 1) % len(self.sand_background)
        
                self.gameDisplay.blit(self.sand_background[current_background_index], (0, 0))
        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif not movement_started and self.winner is None:
                        self.handle_mouse_events(event)
                self.draw_caps()
                
                if dragging_start_pos:
                    mouse_pos = pygame.mouse.get_pos()
                    pygame.draw.line(self.gameDisplay, (255, 255, 255), dragging_start_pos, mouse_pos, 5)

                pygame.display.update()
                
            sand_background_index = 0
            next_change_time = pygame.time.get_ticks()
            while start_cnt == 2: # 응답 대기화면
                if pygame.time.get_ticks() >= next_change_time:
                    next_change_time += 300  # 3초 추가
                    sand_background_index = (sand_background_index + 1) % len(self.sand_background)

                self.gameDisplay.blit(self.sand_background[sand_background_index], (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.draw_caps()
                pygame.display.update()
                
    def game_start(self):
        ready_bg = Thread(target= self.game_on)
        ready_bg.start()
        
    def draw_caps(self):
        """ Draw all caps using images """
        self.gameDisplay.blit(self.player_ball[self.me], (10, 10))
        for player_index, player_caps in enumerate(self.caps):
            for cap in player_caps:
                image = self.draw_player_images[cap['player']]
                rect = image.get_rect(center=(int(cap['position'][0]), int(cap['position'][1])))
                self.gameDisplay.blit(image, rect)

    def handle_mouse_events(self,event):
        """ Handle mouse events to set directions for the caps """
        global movement_started, start_time, dragging_start_pos, start_cnt

        if event.type == pygame.MOUSEBUTTONDOWN and not movement_started:
            for cap in self.caps[self.me]:
                if not cap['active'] and math.hypot(event.pos[0] - cap['position'][0], event.pos[1] - cap['position'][1]) < CAP_RADIUS:
                    cap['active'] = True
                    dragging_start_pos = cap['position']  # Set the dragging start position
                    return
        elif event.type == pygame.MOUSEBUTTONUP and any(cap['active'] for cap in self.caps[self.me]):
            for cap in self.caps[self.me]:
                if cap['active']:
                    drag_vector = [event.pos[0] - dragging_start_pos[0], event.pos[1] - dragging_start_pos[1]]
                    distance = math.hypot(*drag_vector)
                    power = min(distance / 10, 15)  # Cap the power to prevent excessively high values
                    cap['velocity'] = [-power * dim / distance for dim in drag_vector]
                    cap['active'] = False
                    self.caps_set[self.me] += 1
                    dragging_start_pos = None  # Reset dragging position

            # Check if the current player has set directions for all their caps
            if self.caps_set[self.me] >= len([cap for cap in self.caps[self.me] if FIELD_X < cap['position'][0] < FIELD_X + FIELD_WIDTH and FIELD_Y < cap['position'][1] < FIELD_Y + FIELD_HEIGHT]):
                # Move to the next player if current player is done setting caps
                # current_player = (current_player + 1) % total_players
                pickle_dic = pickle.dumps(self.caps[self.me]) # 직렬화 
                client_socket.send(pickle_dic)  # 이것도 클라이언트 관리에서 트리거로 하면 될 거 같아요 
                print('다른 플레이어가 다 옮기기를 기다리기')
                start_cnt = 2
                self.caps_set = [0,0]

def start():
    global start_cnt 
    start_cnt = 0

#메인 게임 필요 변수, 함수
def load_scaled_image(filepath, new_size):
    """ 이미지를 불러와서 지정된 크기로 조정합니다. """
    image = pygame.image.load(filepath).convert_alpha()  # 이미지를 불러옵니다.
    return pygame.transform.scale(image, new_size)  # 이미지의 크기를 조정합니다.
    
def main():
    global start_cnt, client_socket
    pygame.init()
    a = client_pongdang()
    a.game_start()
    while start_cnt == -1:
        ...
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    # print(client_socket.recv(1024).decode('utf-8'))
    
    data = client_socket.recv(1024).decode('utf-8') # 클라이언트한테 시작신호 받기
        # print(data)
    if "시작" in data: # 넘어갈 수 있게 
        received_data = client_socket.recv(4096) # 리스트 형태인 초기 setting 값 받기
        # 딕셔너리 형태도 똑같이 진행
        temp_list = pickle.loads(received_data) # 초기 setting 값 역직렬화
        a.me = int(temp_list.pop())
        a.caps = temp_list.pop()
        start_cnt = 1
        while True :
            while start_cnt == 1 :
                ...
            received_data = client_socket.recv(4096)
            a.caps = pickle.loads(received_data)
            start_cnt = 1
    
                
if __name__ == "__main__":
    main()