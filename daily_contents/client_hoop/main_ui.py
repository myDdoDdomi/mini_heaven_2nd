import pygame
# from neko_game import GameUI
# from neko_chat import ChatUI
# from network.game_network import GameNetworkClient
# from network.chat_network import ChatNetworkClient

pygame.init()
pygame.mixer.init()

from assets.assets import IMAGES, SOUNDS
from components.ui_components import Button


display_width, display_height = 1168, 768
game_width, game_height = 912, 768
chat_width, chat_height = 256, 768
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("대전 특화 2반 이벤트")
clock = pygame.time.Clock()

client_name = ""  # 클라이언트 이름 입력 변수
input_active = True  # 입력창 활성화 여부

# 폰트 설정
font = pygame.font.Font(None, 36)
label_font = pygame.font.Font(None, 42)
input_box = pygame.Rect(214, display_height // 2 + 150, 200, 40)  # 입력창 위치


# 버튼 클릭 이벤트
def start_game():
    print("게임 시작!")

# 버튼 생성
start_button = Button(
    img_normal=IMAGES["start_btn"],  
    x=214, y=display_height // 2 + 200,  
    width=150, height=50,  
    img_hover=IMAGES["start_btn_hover"],  
    action=start_game  
)

def main_loop():
    global client_name, input_active

    while True:
        screen.blit(IMAGES["bg_main"], (0, 0))  # 왼쪽 게임 배경
        screen.blit(IMAGES["chat_bg"], (game_width, 0))  # 오른쪽 채팅 배경

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # 이름 입력 처리
            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # 엔터 키 입력 시
                        input_active = False
                        print(f"입력된 이름: {client_name}")
                    elif event.key == pygame.K_BACKSPACE:  # 백스페이스 키 입력 시
                        client_name = client_name[:-1]
                    else:
                        client_name += event.unicode

        # UI 요소 그리기
        if input_active:
            label_surface = label_font.render("YOUR NAME", True, (0, 0, 0))  # 흰색 텍스트
            screen.blit(label_surface, (input_box.x + 14, input_box.y - 30))  # 입력창 위에 표시

            pygame.draw.rect(screen, (200, 200, 200), input_box)  # 입력창 배경
            text_surface = font.render(client_name, True, (0, 0, 0))
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
            
        start_button.draw(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main_loop()