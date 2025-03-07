import pygame
import sys
import random
import time
import socket
from _thread import *
from threading import Thread

pygame.init() # pygame 모듈 초기화

HOST = '127.0.0.1'  # 호스트
PORT = 1111        # 포트
NAME = "최봉준" #이름을 입력해주세요


WHITE = (255,255,255)
BLACK = (0,0,0)
mainmenu_start = pygame.image.load("./img/start.png")
mainmenu_start_click = pygame.image.load("./img/start_click.png")
explain_back = pygame.image.load("./img/explain.png")
explain_back_click = pygame.image.load("./img/explain_click.png")
back = pygame.image.load("./img/back.png")
back_click = pygame.image.load("./img/back_click.png")
font = pygame.font.Font(None,80)
font_1 = pygame.font.Font(None,100)

img_neko = [ #애니팡 
    None,
    pygame.image.load("./img/neko1.png"),
    pygame.image.load("./img/neko2.png"),
    pygame.image.load("./img/neko3.png"),
    pygame.image.load("./img/neko4.png"),
    pygame.image.load("./img/neko5.png"), 
    pygame.image.load("./img/neko6.png"),
    pygame.image.load("./img/neko_niku.png")
]


main_bgm = pygame.mixer.Sound("./bgm/hot-air-balloon-flight-148232.mp3")

game_bgm = [
    pygame.mixer.Sound("./bgm/8-bit-cartoon-comedy-by-prettysleepy-art-12290.mp3"),
    pygame.mixer.Sound("./bgm/kim-lightyear-you-and-i-161104.mp3"),
    pygame.mixer.Sound("./bgm/area12-131883.mp3"),
    ]

count_bgm = pygame.mixer.Sound("./bgm/effect/countdown_bgm.mp3")

effect_bgm = [
    pygame.mixer.Sound("./bgm/effect/buble_1.mp3"),
    pygame.mixer.Sound("./bgm/effect/buble_2.mp3"),
    pygame.mixer.Sound("./bgm/effect/buble_3.mp3"),
]

point = 0
map_y = 10
map_x = 8
neko = [[] for _ in range(10)]
check = [[0 for _ in range(8)] for _ in range(10)]
search = [[0 for _ in range(8)] for _ in range(10)]
for i in range(10):
    for j in range(8):
        neko[i].append(random.choice(range(1,7)))

bg_main = pygame.image.load("./img/neko_main_bg.png")
bg_explain = pygame.image.load("./img/neko_explain_bg.png")
bg = pygame.image.load("./img/neko_bg.png")
cursor =pygame.image.load("./img/neko_cursor.png")
bg_loading = pygame.image.load("./img/neko_loading_bg.png")
display_width = 912
display_height = 768

gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("애니팡")  # 타이틀
clock = pygame.time.Clock() #Clock 오브젝트 초기화

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


class Mouse:
    def __init__(self, cursor, map_x, map_y):
        self.turn = 0
        self.map_y = map_y
        self.map_x = map_x
        self.cursor = cursor
        
    def get_move(self) :
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(self.map_y):
            for x in range(self.map_x):
                if x*72+20 < mouse[0] < (x+1)*72+20 and y*72+20 < mouse[1] < (y+1)*72+20 :
                    if self.turn == 0 :
                        gameDisplay.blit(self.cursor,(x*72+20, y*72+20))
                        if click[0] :
                            check[y][x] = 1
                            self.turn = 1
                    else :
                        if (y+1 < self.map_y and check[y+1][x] == 1) or \
                            (0 <= y-1 and check[y-1][x] == 1) or \
                            (x+1 < self.map_x and check[y][x+1] == 1) or \
                            (0<= x-1 and check[y][x-1] == 1):
                            gameDisplay.blit(self.cursor,(x*72+20, y*72+20))
                            if click[0]:
                                switch_neko(y,x)
                                if not check_switch(y,x):
                                    switch_neko(y,x)
                                cursor_set()    
                                self.turn = 0
                        if click[2] :
                            cursor_set()
                            self.turn = 0
                        
                        
def check_neko(idx):
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7
                    idx = 1

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7
                    idx = 1
    return idx

def check_switch(y,x):
    for y in range(10):
        for x in range(8):
            search[y][x] = neko[y][x]

    for y in range(1, 9):
        for x in range(8):
            if search[y][x] > 0:
                if search[y-1][x] == search[y][x] and search[y+1][x] == search[y][x]:
                    return True

    for y in range(10):
        for x in range(1, 7):
            if search[y][x] > 0:
                if search[y][x-1] == search[y][x] and search[y][x+1] == search[y][x]:
                    return True
    return False

def sweep_neko():
    cnt = 1
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                if cnt < 200 :
                    cnt *= 2
    point = 20*cnt
    return point

def drop_neko() :
    global neko
    for y in range(10):
        for x in range(8) :
            if y >= 1 :
                if neko[y][x] == 0 :
                    neko[y][x] = neko[y-1][x]
                    neko[y-1][x] = 0
            if y == 0 :
                if neko[y][x] == 0 :
                    neko[y][x] = random.choice(range(1,7))


def switch_neko(y,x):
    global check, neko
    for i in range(10):
        for j in range(8):
            if check[i][j] == 1:
                neko[i][j], neko[y][x] = neko[y][x], neko[i][j]

def draw_neko():
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                gameDisplay.blit(img_neko[neko[y][x]], (x*72+20, y*72+20))
                
def draw_cursor():
    for y in range(10):
        for x in range(8):
            if check[y][x] == 1 :
                gameDisplay.blit(cursor, (x*72+20, y*72+20))

def cursor_set() :
    global check
    check = [[0 for _ in range(8)] for _ in range(10)]

def game():
    tmr = 0 # 시간 관리 변수
    m = Mouse(cursor,map_x,map_y)
    idx = 0
    cnt = 0
    tiover = 60
    pygame.mixer.stop()
    while True:
        tmr += 1 # 매 시간 1초 증가
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg, (0,0))
        
            
        if cnt == 0 and (tmr/10) <= 5 :
            txt_1 = font_1.render(str(round(5-(tmr/10))), True, BLACK)
            if idx == 0: # 딜레이 주면서 사진 보이기
                idx = check_neko(idx)
            elif 3 > idx >= 1 :
                idx += 1
            elif idx == 3 :
                sweep_neko()
                idx = 0
            draw_neko()
            drop_neko()
            gameDisplay.blit(txt_1,[400,350])
            pygame.display.update() # 화면 업데이트
            clock.tick(10)
            if (tmr/10) == 1 :
                count_bgm.play()
            if (tmr/10) == 5 :
                tmr = 0
                point = 0
                cnt = 1
            continue
            
        if pygame.mixer.get_busy() == False:
            game_bgm[random.choice(range(0,3))].play()
        time_over = tiover - (tmr/10)
        txt = font.render(str(round(time_over, 1)), True, WHITE)
        txt_2 = font.render(str(point), True, WHITE)
        if idx == 0: # 딜레이 주면서 사진 보이기
            idx = check_neko(idx)
        elif 3 > idx >= 1 :
            idx += 1
            if idx == 2:
                effect_bgm[random.choice(range(0,3))].play()
                tiover += 0.5
        elif idx == 3 :
            point += sweep_neko()
            idx = 0
        m.get_move()
        draw_cursor()
        if time_over == 0 :
            game_over(point)
            break
        draw_neko()
        drop_neko()
        gameDisplay.blit(txt,[690,50])
        gameDisplay.blit(txt_2,[690,150])
        pygame.display.update() # 화면 업데이트
        clock.tick(10) #프레임 레이트 지정

def game_over(point):
    global client_socket
    message = f"{NAME} {point}"
    client_socket.send(message.encode('utf-8'))
    txt_1 = font_1.render("Your Score : " + str(point), True, BLACK)
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg_main, (0, 0))
        gameDisplay.blit(txt_1,[40,450])
        Button(mainmenu_start, 240, 550, 150, 80, mainmenu_start_click, 210, 535, game)
        pygame.display.update() # 화면 업데이트
        clock.tick(15) #프레임 레이트 지정
        
def explain():
    exp = True

    while exp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg_explain, (0, 0))
        Button(back, 188, 600, 230, 140, back_click, 188, 597, mainmenu)

        pygame.display.update()
        clock.tick(15)

def client():
    global start_cnt, client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    # print(client_socket.recv(1024).decode('utf-8'))
    start_cnt = 0
    loading_1 = Thread(target = loading)
    loading_1.start()
    data = client_socket.recv(1024).decode('utf-8') # 시작 받으면
        # print(data)
    if "시작" in data: # 넘어갈 수 있게 
        start_cnt = 1
        game()

def loading():
    global start_cnt
    idx = 0
    while start_cnt == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mixer.get_busy() == False :
            main_bgm.play()
        ##코드 수정 부분##
        # guess = input("Guess the number > ") # 입력 받고 
        # client_socket.send(guess.encode('utf-8')) # 이진수로 문자열 전달
        ##------------##
        gameDisplay.blit(bg_loading, (0, 0))    
        if idx < 5 :
            idx += 1 
            gameDisplay.blit(img_neko[1],(2*72+20, 8*72+20))
        elif 5 <= idx < 10 :
            idx += 1 
            gameDisplay.blit(img_neko[2],(3*72+20, 8*72+20))
        elif 10 <= idx < 15 :
            idx += 1 
            gameDisplay.blit(img_neko[3],(4*72+20, 8*72+20))
        elif 15 <= idx < 20 :
            idx += 1 
            gameDisplay.blit(img_neko[4],(5*72+20, 8*72+20))
        elif idx == 20 :
            idx = 0
        pygame.display.update()
        clock.tick(15)

def mainmenu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mixer.get_busy() == False :
            main_bgm.play()
        gameDisplay.blit(bg_main, (0, 0))
        Button(mainmenu_start, 240, 450, 150, 80, mainmenu_start_click, 210, 435, client)
        Button(explain_back, 240, 550, 150, 80, explain_back_click, 210, 535, explain)
        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":
    mainmenu()