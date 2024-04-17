import pygame
import sys
import random
import time

pygame.init() # pygame 모듈 초기화

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


# 새로운 아이콘 이미지 로드
new_icon = pygame.image.load("./img/heart_icon.png")
pygame.display.set_icon(new_icon)



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


main_bgm = pygame.mixer.Sound("./bgm/Fun Kid - Quincas Moreira.mp3")

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


# 메인 시작 화면 크기 설정 셋팅
display_width = 1280
display_height = 720


bg_explain = pygame.image.load("./img/explain_bg.png")
bg = pygame.image.load("./img/neko_bg.png")
cursor =pygame.image.load("./img/neko_cursor.png")


gameDisplay = pygame.display.set_mode((display_width, display_height)) #스크린 초기화
pygame.display.set_caption("LOVE BOMB")  # 타이틀
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
                        
# 고양이 개수 확인  
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

# 고양이 떨어뜨리기
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
    tiover = 3
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
        
cur_idx=0
next_level = pygame.time.get_ticks() + 300

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
        Button(mainmenu_start, 300, 600, 150, 80, mainmenu_start_click, 210, 535, mainmenu)
        pygame.display.update() # 화면 업데이트
        clock.tick(15) #프레임 레이트 지정
        
# 설명 부분
def explain():
    exp = True

    while exp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        gameDisplay.blit(bg_explain, (0, 0))
        Button(back, 500, 550, 230, 140, back_click, 500, 550, mainmenu)

        pygame.display.update()
        clock.tick(15)

# 메인페이지(처음)
def mainmenu():
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
            main_bgm.play()
        # 버튼만들기 Button(img, x, y , he, w , act_img,  act_x, act_y, func)
        Button(explain_back, 400, 550, 150, 80, explain_back_click, 400, 550, explain)
        Button(mainmenu_start, 700, 550, 150, 80, mainmenu_start_click, 700, 550, game)
        pygame.display.update()
        clock.tick(7)
        

if __name__ == "__main__":
    mainmenu()