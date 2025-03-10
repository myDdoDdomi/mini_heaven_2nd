import pygame
import asyncio
import threading
# from neko_game import GameUI
from neko_chat import ChatUI
# from network.game_network import GameNetworkClient
from network.chat_network import ChatNetworkClient

pygame.init()
pygame.mixer.init()

from assets.assets import IMAGES, SOUNDS
from components.ui_components import Button, InputBox

display_width, display_height = 1168, 768
game_width, game_height = 912, 768
chat_width, chat_height = 256, 768
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("대전 특화 2반 이벤트")
clock = pygame.time.Clock()

client_name = ""  # 클라이언트 이름 입력 변수
input_active = True  # 입력창 활성화 여부

# 폰트 설정
font = pygame.font.Font(None, 36)
FONT_PATH = "./assets/Font/NanumSquareRoundR.ttf"
FONT_SIZE = 30

korean_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
# ✅ asyncio 이벤트 루프 생성
loop = asyncio.new_event_loop()

# ✅ 루프를 실행하는 별도 스레드 생성
def run_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()  # ✅ 이벤트 루프가 계속 실행되도록 유지

# ✅ 백그라운드에서 실행할 스레드 생성
loop_thread = threading.Thread(target=run_loop, daemon=True)
loop_thread.start()

# ✅ 네트워크 클라이언트 초기화 (아직 서버 연결 안 함)
chat_network = None

# 채팅 UI 생성
chat_ui = ChatUI(game_width, 0, chat_width, chat_height, korean_font, chat_network, client_name)


label_font = pygame.font.Font(None, 42)
input_box = pygame.Rect(214, display_height // 2 + 150, 200, 40)  # 입력창 위치

def start_game():
    """버튼을 눌렀을 때 실행 (서버 연결)"""
    global client_name, chat_network, chat_ui

    # ✅ 최신 입력값 가져오기
    client_name = name_input_box.text.strip()

    print(f"게임 시작! 채팅 서버에 '{client_name}' 이름으로 연결 중...")

    if client_name:  # 이름이 입력되었는지 확인
        chat_network = ChatNetworkClient("ws://localhost:8000", client_name)  # 채팅 네트워크 생성

        # ✅ asyncio.run() 대신 비동기적으로 실행
        future = asyncio.run_coroutine_threadsafe(chat_network.connect(), loop)
        try:
            future.result()  # 실행 결과 확인 (예외 발생 시 확인 가능)
        except Exception as e:
            print(f"❌ 서버 연결 중 오류 발생: {e}")

        # ✅ 채팅 UI를 업데이트해서 새로운 chat_network 사용
        chat_ui.client_name = client_name  # 🔥 이 부분 추가
        chat_ui.chat_network = chat_network
        chat_ui.set_connected()  # 웹소켓 연결 후 입력창 활성화
    else:
        print("⚠️ 클라이언트 이름을 입력하세요!")  # 빈 값 방지

# 버튼 생성
start_button = Button(
    img_normal=IMAGES["start_btn"],
    x=237, y=560,
    width=150, height=50,
    img_hover=IMAGES["start_btn_hover"],
    x_act=207, y_act=545,  # 마우스가 올라갔을 때 이미지 위치 (변경 가능)
    action=start_game
)

name_input_box = InputBox(214, display_height // 2 + 150, 200, 40, korean_font, placeholder="Enter your name")


def main_loop():
    global client_name, input_active

    while True:
        screen.blit(IMAGES["bg_main"], (0, 0))  # 왼쪽 게임 배경
        screen.blit(IMAGES["chat_bg"], (game_width, 0))  # 오른쪽 채팅 배경

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("🎮 게임 종료 중...")
                pygame.quit()
                loop.stop()  # ✅ asyncio 이벤트 루프도 종료
                loop_thread.join()  # ✅ 스레드 종료 대기
                return

            # 입력창 이벤트 처리 (이름 입력)
            result = name_input_box.handle_event(event)
            if result is not None:  # 엔터 입력 시 값 설정
                client_name = result
                print(f"입력된 이름: {client_name}")

            # ✅ 채팅 UI 이벤트 처리 (채팅 입력 가능하도록 추가)
            chat_ui.handle_event(event)

        # ✅ UI 요소 그리기
        name_input_box.draw(screen)  # 이름 입력창
        start_button.draw(screen)  # 시작 버튼
        chat_ui.draw(screen)  # ✅ 채팅 UI 추가 (입력창 포함)

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main_loop()
