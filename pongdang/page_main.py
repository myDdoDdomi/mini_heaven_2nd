import pygame
import time

# 스타트 페이지 이미지
background_start = pygame.image.load("./image/main_background.jpg") # 스타트 배경
background_start = pygame.transform.scale(background_start, (650, 977))
btn_start = pygame.image.load("./image/start_btn.png") # 스타트 버튼
btn_start = pygame.transform.scale(btn_start, (350, 147))
btn_start_click = pygame.image.load("./image/start_btn2.png") # 클릭시 스타트 버튼
btn_start_click = pygame.transform.scale(btn_start_click, (350, 147))

# 플레이 페이지 이미지
background_play = [pygame.image.load(f"./image/background_{i}.png") for i in range(4)]

background_land_play = pygame.image.load("./image/land.jpg") # 플레이 배경
background_play = [pygame.transform.scale(image, (650, 977)) for image in background_play]
background_land_play = pygame.transform.scale(background_land_play, (630, 630))

# 디스플레이 창 크기 설정
display_width = 650 # 가로 사이즈
display_height = 977 # 세로 사이즈

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("PONGDANG")

# 스타트 배경 bilt
gameDisplay.blit(background_start, (0, 0))

# 시작 버튼 스타트 배경 위에 blit
button_x = (display_width - btn_start.get_width()) // 2  # 가로 위치
button_y = (display_height - btn_start.get_height()) // 1.3  # 세로 위치
gameDisplay.blit(btn_start, (button_x, button_y)) # 버튼 built

# 배경 이미지 인덱스
current_background_index = 0
next_change_time = pygame.time.get_ticks() + 300  # 3초마다 이미지 변경


# 디스플레이 업데이트
pygame.display.update()

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

def main():
    global next_change_time,current_background_index
    running = True
    while running:
        # 배경 이미지 변경
        
        if pygame.time.get_ticks() >= next_change_time:
            current_background_index = (current_background_index + 1) % len(background_play)
            next_change_time += 300  # 3초 추가
            
        gameDisplay.blit(background_play[current_background_index], (0, 0))
        gameDisplay.blit(background_land_play, (10,175))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.draw.rect(gameDisplay, (255, 0, 0), (200, 200, 60, 60))
        pygame.display.update()

# 이벤트 루프
def start_page():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = pygame.mouse.get_pos()

        # 마우스 위치 확인
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_x, mouse_y = mouse_pos
        gameDisplay.blit(background_start, (0, 0))

        Button(btn_start, button_x, button_y, 350, 147, btn_start_click, button_x, button_y, main)
        
        pygame.display.update()
    


if __name__ == '__main__':
    start_page()