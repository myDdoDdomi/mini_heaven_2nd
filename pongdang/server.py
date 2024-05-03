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
client_sockets = []
tri_ready = 0
FIELD_WIDTH, FIELD_HEIGHT = 630, 630
FIELD_X, FIELD_Y = (display_width - FIELD_WIDTH) // 2, (display_height - FIELD_HEIGHT) // 2
CAP_RADIUS = 25
MAX_CAPS = 5  # Each player has 5 caps
current_player = 0
total_players = 2
caps_set = [0, 0]  # Tracks the number of caps set by each player
# caps = []
movement_started = False
start_time = None
client_num=0
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
        self.loading_img = [pygame.image.load(f"./image/loading_img/loading{i}.png") for i in range(1,8)]
        self.loading_img = [pygame.transform.scale(image, (350, 350)) for image in self.loading_img]

        self.background_land_play = pygame.image.load("./image/land.jpg") # 플레이 배경
        self.background_land_play = pygame.transform.scale(self.background_land_play, (630, 630))

        self.play_background_top=[pygame.image.load(f"./image/play_background_top/{i}.png") for i in range(12)]
        self.play_background_top = [pygame.transform.scale(image, (650, 224)) for image in self.play_background_top]
        self.play_background_bt=[pygame.image.load(f"./image/play_background_bt/{i}.png") for i in range(12)]
        self.play_background_bt = [pygame.transform.scale(image, (650, 224)) for image in self.play_background_bt]

        self.sand_background=[pygame.image.load(f"./image/sandcrop/{i}.png") for i in range(10)]

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
        self.winner_0=pygame.image.load("image/draw.png")
        self.winner_0=pygame.transform.scale(self.winner_0, (579, 277))
        self.winner = 0
        
        self.caps = []
        
        
    def game_on(self):
        global tri_ready,start_time, server_run
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
        current_background_index_load=0

        self.font = pygame.font.Font(None, 36)
        self.player_images = [
            ('image/ball7.png', (50, 50)),  # 플레이어 1 이미지
            ('image/ball8.png', (50, 50))   # 플레이어 2 이미지
        ]
        self.draw_player_images = [
            load_scaled_image('image/ball7.png', (50, 50)),  # 플레이어 1 이미지
            load_scaled_image('image/ball8.png', (50, 50))   # 플레이어 2 이미지
        ]
        
        def end_page(winner):
            
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # if pygame.time.get_ticks() >= next_change_time:
                #     current_background_index = (current_background_index + 1) % len(background_start)
                #     next_change_time += 80  # 3초 추가
                self.gameDisplay.blit(self.background_end, (0, 0))
                if winner==0:
                    self.effect_ending.play()
                    self.gameDisplay.blit(self.winner_1, (35, 200))
                elif winner==1:
                    self.effect_ending.play()
                    self.gameDisplay.blit(self.winner_2, (35, 200))
                else:
                    self.gameDisplay.blit(self.winner_0, (35, 200))
                # gameDisplay.blit(background_start, (0, 0))
                # gameDisplay.blit(title_start,(36,240))
                pygame.display.update()
            
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

            current_background_index = (current_background_index + 1) % len(self.background_play)
            current_background_index_shark = (current_background_index_shark + 1) % len(self.sharkfin_play)
            current_background_index_load = (current_background_index_load + 1) % len(self.loading_img)

            time.sleep(0.15)
            self.gameDisplay.blit(self.background_play[current_background_index], (0, 0))
            self.gameDisplay.blit(self.sharkfin_play[current_background_index_shark], (75, 200))
            self.gameDisplay.blit(self.loading_img[current_background_index_load], (150, 650))

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

            current_background_index=0

            current_background_index = (current_background_index + 1) % len(self.background_start)

            time.sleep(0.1)
            self.gameDisplay.blit(self.background_start[current_background_index], (0, 0))
            
            self.gameDisplay.blit(self.title_start,(36,240))
            button(self.btn_start, button_x, button_y, 350, 147, self.btn_start_click, button_x, button_y, start)
            # 버튼 누를 시 tri_ready=1로 만들어서 게임 시작
            pygame.display.update()
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load('music/main_bgm_1.mp3')
        pygame.mixer.music.play()
        # 게임 화면 ----------------------------------------------------------------
        next_change_time = pygame.time.get_ticks()
        while server_run :
            while tri_ready == 1: # 대기 화면

                if pygame.time.get_ticks() >= next_change_time:
                    next_change_time += 300  # 3초 추가
                    current_background_index = (current_background_index + 1) % len(self.sand_background)
    
                self.gameDisplay.blit(self.sand_background[current_background_index], (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                
                self.handle_mouse_events()
                self.draw_caps()
                if movement_started:
                    tri_ready=2
                    
                pygame.display.update()
                pygame.time.Clock().tick(60)
                
                
            while tri_ready == 2 : #충돌화면 송 
            
                if pygame.time.get_ticks() >= next_change_time:
                    next_change_time += 300  # 3초 추가
                    current_background_index = (current_background_index + 1) % len(self.sand_background)
    
                self.gameDisplay.blit(self.sand_background[current_background_index], (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                self.draw_caps()
                if time.time() - start_time >= 3:
                    self.update_positions()
                    self.remove_out_of_bounds_caps()
                    if self.all_caps_stopped():
        
                        self.winner = self.check_game_over()
                        if self.winner is not None:
                            #print(self.winner)
                            end_page(self.winner)
                            # End game after displaying the winner
                        else:
                            self.reset_for_next_turn()  # Prepare for the next turn
                            tri_ready=1
                            
                else:
                    # Draw a countdown timer on the gameDisplay
                    countdown_timer = max(0, int(2 - (time.time() - start_time)))
                    self.gameDisplay.blit(self.moving_in[countdown_timer], (display_width // 2 - 350 // 2, display_height // 2 - 147 // 2))
                pygame.display.update()
                pygame.time.Clock().tick(60) 
                       
    def handle_mouse_events(self):
        global client_num
        if client_num == 4 :
            start_movement()
  
            
    def draw_caps(self):
        """ Draw all caps using images """
        
        for player_index, player_caps in enumerate(self.caps):
            for cap in player_caps:
                image = self.draw_player_images[cap['player']]
                rect = image.get_rect(center=(int(cap['position'][0]), int(cap['position'][1])))
                self.gameDisplay.blit(image, rect)

        
    
    def update_positions(self):
        """ Update positions of all caps based on their velocities and handle collisions """
        if not movement_started:
            return  # Do not update positions if the movement has not started
        if time.time() - start_time < 3:
            return  # Wait for 3 seconds before moving the caps
        for player_caps in self.caps:
            for cap in player_caps:
                cap['position'][0] += cap['velocity'][0]
                cap['position'][1] += cap['velocity'][1]
                cap['velocity'] = [0.98 * v for v in cap['velocity']]  # Apply friction
        self.handle_collisions()

    def handle_collisions(self):
        """ Handle collisions between caps """
        all_caps = [cap for sublist in self.caps for cap in sublist]
        for i, cap1 in enumerate(all_caps):
            for cap2 in all_caps[i+1:]:
                dx, dy = cap1['position'][0] - cap2['position'][0], cap1['position'][1] - cap2['position'][1]
                distance = math.hypot(dx, dy)
                if distance < 2 * CAP_RADIUS:
                    nx, ny = dx / distance, dy / distance
                    v1n = nx * cap1['velocity'][0] + ny * cap1['velocity'][1]
                    v2n = nx * cap2['velocity'][0] + ny * cap2['velocity'][1]
                    cap1['velocity'][0] += v2n * nx - v1n * nx
                    cap1['velocity'][1] += v2n * ny - v1n * ny
                    cap2['velocity'][0] += v1n * nx - v2n * nx
                    cap2['velocity'][1] += v1n * ny - v2n * ny
                    self.hitSound2.play()

        
    def remove_out_of_bounds_caps(self):
        """ Remove caps that have gone out of the playing field """
        for i in range(total_players):
            temp=self.caps[i]
            self.caps[i] = [cap for cap in self.caps[i] if FIELD_X <= cap['position'][0] <= FIELD_X + FIELD_WIDTH and
                    FIELD_Y <= cap['position'][1] <= FIELD_Y + FIELD_HEIGHT]
            if temp!=self.caps[i]:
                self.fallSound.play()

        
    def check_game_over(self):
        #print(self.caps)
        """ Check if the game is over and return the result """
        if not self.caps[0] and not self.caps[1]:
            return -1  # Draw
        if not self.caps[0]:
            return 1  # Player 2 wins
        if not self.caps[1]:
            return 0  # Player 1 wins
        return None  # Game is not over

    def all_caps_stopped(self):
        """ Check if all caps have stopped moving """
        for player_caps in self.caps:
            for cap in player_caps:
                if math.hypot(*cap['velocity']) > 0.01:  # If any cap is still moving (above a small threshold)
                    return False
        return True

    def reset_for_next_turn(self):
        """ Reset variables for the next turn """
        global caps_set, movement_started, start_time
        caps_set = [0, 0]
        movement_started = False
        start_time = None
        for player_caps in self.caps:
            for cap in player_caps:
                cap['active'] = False  # No cap is currently being dragged
                cap['velocity'] = [0, 0]  # Reset the velocity of all caps



                    
    def game_start(self):
        ready_bg = Thread(target= self.game_on)
        ready_bg.start()
        
    def initialize_caps(self):
        """ Initialize cap positions in a grid pattern ensuring no overlap and then shuffle """
        caps = self.caps
        grid_size = CAP_RADIUS * 2 + 5  # Grid size ensuring no overlap, add a little extra space
        cols = (FIELD_WIDTH // grid_size)
        rows = (FIELD_HEIGHT // grid_size)
        
        # Create a list of positions based on the grid
        positions = [(FIELD_X + (i % cols) * grid_size + CAP_RADIUS, FIELD_Y + (i // cols) * grid_size + CAP_RADIUS)
                    for i in range(cols * rows)]
        random.shuffle(positions)  # Shuffle the positions to get a random order

        for i in range(total_players):
            player_caps = []
            for _ in range(MAX_CAPS):
                if positions:
                    new_pos = positions.pop()
                    player_caps.append({'position': list(new_pos), 'velocity': [0, 0], 'color': self.player_images[i], 'player': i, 'active': False})
            caps.append(player_caps)

        # In the unlikely event that there's still overlap, run another check and reposition caps
        for i, cap1 in enumerate(caps[0] + caps[1]):
            for cap2 in (caps[0] + caps[1])[i+1:]:
                while math.hypot(cap1['position'][0] - cap2['position'][0], cap1['position'][1] - cap2['position'][1]) < 2 * CAP_RADIUS:
                    cap2['position'][0] = random.randint(FIELD_X + CAP_RADIUS, FIELD_X + FIELD_WIDTH - CAP_RADIUS)
                    cap2['position'][1] = random.randint(FIELD_Y + CAP_RADIUS, FIELD_Y + FIELD_HEIGHT - CAP_RADIUS)

#메인 게임 필요 변수, 함수
def load_scaled_image(filepath, new_size):
    """ 이미지를 불러와서 지정된 크기로 조정합니다. """
    image = pygame.image.load(filepath).convert_alpha()  # 이미지를 불러옵니다.
    return pygame.transform.scale(image, new_size)  # 이미지의 크기를 조정합니다.

def start_movement():
    """ Begin the movement after both players have set their caps """
    global movement_started, start_time
    movement_started = True
    start_time = time.time()



# 버튼 누를 시 tri_ready=1로 만들어서 게임 시작
def start():
    global tri_ready
    tri_ready = 1

def handle_client(client_socket, a):
    global client_sockets, tri_ready, client_num, current_player, server_run
    # 게임 준비 --------------------------------------------------------
    while tri_ready == 0 :
        ...
        
    
    client_socket.send("시작".encode('utf-8'))
    
    # 시작하기 전에 공의 랜덤 위치와 플레이어 지정 신호를 클라이언트한테 전달 해야됨---------------
    if not a.caps :
        a.initialize_caps()
        
    temp_list = []
    temp_list.append(a.caps)
    temp_list.append(str(client_sockets.index(client_socket)))
    print(temp_list)
    data_bytes = pickle.dumps(temp_list) # pickle 모듈을 활용한 데이터 직렬화
    # 딕셔너리 형태도 똑같이 진행
    client_socket.send(data_bytes) # 리스트 형태로 보내줌
    client_num += 1

    # 게임 시작 ----------------------------------------------------
    while server_run :
        if client_num == 1 :
            continue
        if client_num == 2 : 
            print(1)
            player_info = client_socket.recv(4096) #각 클라이언트한테 정보 받기
            player_list = pickle.loads(player_info)
            a.caps[client_sockets.index(client_socket)] = player_list
            client_num += 1 
        
        while tri_ready == 1 :
            ...
        
        while tri_ready == 2:
            ...
        data_bytes = pickle.dumps(a.caps)
        client_socket.send(data_bytes)
        client_num = 2 
        
        
        



def main():
    global a
    pygame.init()
    # 아이콘 이미지
    a = server_pongdang() # 이거는 화면송출 클래스
    a.game_start() # Thread 이용해서 클라이언트 관리와 화면 송출을 따로 관리함
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: #소켓 연결
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)
        print("Server started, listening on port", PORT)
        
        conn1, addr1 = server_socket.accept()
        client_sockets.append(conn1)
        print("Client connected", addr1)
        print("참가자 수 : ", len(client_sockets))
        start_new_thread(handle_client, (conn1, a))
        
        conn2, addr2 = server_socket.accept()
        client_sockets.append(conn2)
        print("Client connected", addr2)
        print("참가자 수 : ", len(client_sockets))
        start_new_thread(handle_client, (conn2, a))

    

if __name__ == "__main__":
    main()