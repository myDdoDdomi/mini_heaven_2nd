import socket
import random
import pygame
from _thread import *
import sys
import time
from threading import Thread

HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
display_width = 912
display_height = 768
client_sockets = []
tri_ready = 0
final_tri = 0
point_dict = {}
BLACK = (0,0,0)



class ready_neko:
    def __init__(self) -> None:
        
        
        

        self.img_neko = [ #애니팡 
            None,
            pygame.image.load("./img/neko1.png"),
            pygame.image.load("./img/neko2.png"),
            pygame.image.load("./img/neko3.png"),
            pygame.image.load("./img/neko4.png"),
            pygame.image.load("./img/neko5.png"), 
            pygame.image.load("./img/neko6.png"),
            pygame.image.load("./img/neko_niku.png")
        ]
        


        self.bg = pygame.image.load("./img/neko_bg.png")
        self.ranking_bg = pygame.image.load("./img/neko_ranking_bg.png")
        self.mainmenu_start = pygame.image.load("./img/start.png")
        self.mainmenu_start_click = pygame.image.load("./img/start_click.png")
        
        st_g = ''
        
        point_dict = {}

        self.neko = [[0 for _ in range(8)] for _ in range(10)]

    def gameOn(self) :
        global tri_ready, point_fin, final_tri, point_dict
        pygame.init()
        font_1 = pygame.font.SysFont("malgungothic",53)
        pygame.display.set_caption("애니팡 서버")  # 타이틀
        self.clock = pygame.time.Clock() #Clock 오브젝트 초기화
        self.gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
        
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
                    
        while tri_ready == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.gameDisplay.blit(self.bg,(0,0))
            for x in range(len(client_sockets)):
                        y = x//8
                        x = x%8
                        if self.neko[y][x] == 0 :
                            self.neko[y][x] = random.choice(range(1,7))

            for i in range(10):
                for j in range(8):
                    if self.neko[i][j] > 0:
                        self.gameDisplay.blit(self.img_neko[self.neko[i][j]], (j*72+20, i*72+20))
            
            button(self.mainmenu_start, 240, 550, 150, 80, self.mainmenu_start_click, 210, 535, start)
            pygame.display.update()
            self.clock.tick(15)
        #--------------------------
        while tri_ready == 1 :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.gameDisplay.blit(self.ranking_bg,(0,0))
            if final_tri == 1 :
                key_rank = point_fin.keys()
                rank = 1
                for i in key_rank :
                    txt = font_1.render(f"{i} : {point_dict[i]} point", True, BLACK)
                    self.gameDisplay.blit(txt,(283,120+100*rank))
                    rank += 1
                    if rank == 6:
                        break
            pygame.display.update()
            self.clock.tick(15)
     
     
        
    def game_start(self) :
        ready_bg = Thread(target = self.gameOn)
        ready_bg.start()

def start():
    global tri_ready
    tri_ready = 1


    

def handle_client(client_socket, _): # 클라이언트들 관리 함수 
    global client_sockets, tri_ready, point_dict, point_fin, final_tri # global로 클라리언트 리스트 통해서 클라이언트 관리
    while tri_ready == 0 :
        if tri_ready == 1 : # 트리거 이용하여 조건 만족 시 클라이언트 들에게 시작 문자 send
            for client in client_sockets: # for문 이용하여 리스튼 안 있던 모든 클라이언트들에게 메세지 send
                client.send("시작".encode('utf-8')) 
                
    point = client_socket.recv(1024).decode('utf-8') # 각 클라이언트들이 보내는 포인트 및 이름 메시지 recv 받기 메시지 유형은 f"{NAME} {point}""
    NAME, point = point.split() # 스트링 각각 변수로 잘라줘서 젖아하기
    point_dict[NAME] = int(point) # 딕셔너리 형태로 이름 각각에 담기
    point_fin = sorted(point_dict.items(), key=lambda x: x[1], reverse=True)  # value 값으로 내림차순 정렬하기
    point_fin = dict(point_fin) 
    final_tri = 1
        # else :
        #     tri_ready = 1


def main():
    pygame.init()
    yaong = [
        pygame.mixer.Sound("./bgm/server/yaong_1.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_2.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_3.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_4.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_5.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_6.mp3"),
        pygame.mixer.Sound("./bgm/server/yaong_7.mp3"),
        ]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Server started, listening on port", PORT)
        
        a = ready_neko()
        a.game_start() # 게임 화면이랑 클라이언트 관리 함수를 쓰레드 이용하여 따로 관리
        while True:
            client_socket, _ = server_socket.accept() # 클라이언트 서버에 연결 
            yaong[random.choice(range(7))].play()
            client_sockets.append(client_socket)  # 연결한 클라이언트들 한꺼번에 관리하기 위해 리스트안에 클라이언트들 append 
            print("Client connected")
            print("참가자 수 : ", len(client_sockets))
            start_new_thread(handle_client, (client_socket, _)) # 순차적으로 들어온 클라이언트들 다음 함수로 쓰레드를 통해 각각 넣어줌
            

if __name__ == "__main__":
    main()