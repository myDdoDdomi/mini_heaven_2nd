import pygame
import asyncio
import threading
from resources.network.game_network import GameNetworkClient
from resources.network.chat_network import ChatNetworkClient

pygame.init()
pygame.mixer.init()

from resources.neko_chat import ChatUI
from resources.neko_game import GameUI
from resources.assets.assets import IMAGES, SOUNDS, img_neko
from resources.components.ui_components import Button, InputBox

display_width, display_height = 1424, 768
game_width, game_height = 912, 768
chat_width, chat_height = 512, 768
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("대전 특화 2반 이벤트")
clock = pygame.time.Clock()

client_name = ""  
input_active = True  

# 폰트 설정
FONT_PATH = "./resources/assets/Font/NanumSquareRoundR.ttf"
FONT_SIZE = 26
korean_font = pygame.font.Font(FONT_PATH, FONT_SIZE)

# ✅ 각각의 asyncio 루프 생성
chat_loop = asyncio.new_event_loop()
game_loop = asyncio.new_event_loop()

# ✅ 각각의 루프를 실행하는 별도 스레드 생성
def run_chat_loop():
    asyncio.set_event_loop(chat_loop)
    chat_loop.run_forever()

def run_game_loop():
    asyncio.set_event_loop(game_loop)
    game_loop.run_forever()

chat_loop_thread = threading.Thread(target=run_chat_loop, daemon=True)
game_loop_thread = threading.Thread(target=run_game_loop, daemon=True)

chat_loop_thread.start()
game_loop_thread.start()
game_started = False  # ✅ 게임 시작 여부를 체크하는 플래그 추가
# ✅ 네트워크 클라이언트 초기화
chat_network = None
game_network = None
game_ui = None  

# 채팅 UI 생성
chat_ui = ChatUI(game_width, 0, chat_width, chat_height, korean_font, chat_network, client_name)

label_font = pygame.font.Font(None, 42)
input_box = pygame.Rect(214, display_height // 2 + 150, 200, 40)  

chat_server_url = "ws://3.35.135.31:8000"  
game_server_url = "ws://3.35.135.31:8001"  

def start_game():
    """🔥 게임 시작 버튼 눌렀을 때 실행"""
    global client_name, chat_network, chat_ui, game_network, game_ui, name_input_box, game_started, start_button

    if name_input_box:
        client_name = name_input_box.text.strip()
    else:
        # print("⚠️ 이미 게임이 시작되었습니다!")
        return  

    game_started = True  # ✅ 게임 시작 플래그 설정 (UI 전환)
    # print(f"🔥 게임이 시작됩니다! 플레이어: {client_name}")

    if client_name:  
        # ✅ 채팅 서버 연결
        chat_network = ChatNetworkClient(chat_server_url, client_name)  

        future = asyncio.run_coroutine_threadsafe(chat_network.connect(), chat_loop)
        try:
            future.result()  
        except Exception as e:
            ...# print(f"❌ 채팅 서버 연결 중 오류 발생: {e}")

        # ✅ 채팅 UI 업데이트
        chat_ui.client_name = client_name  
        chat_ui.chat_network = chat_network
        chat_ui.set_connected()  

        # ✅ 게임 UI 실행 (게임 대기화면)
        game_ui = GameUI(0, 0, game_width, game_height, pygame.font.Font(None, 26), None, game_loop, screen)

        # ✅ 게임 서버 연결
        game_network = GameNetworkClient(game_server_url, client_name, game_ui.update_players, game_ui)
        future_game = asyncio.run_coroutine_threadsafe(game_network.connect(), game_loop)
        try:
            future_game.result()
        except Exception as e:
            ...# print(f"❌ 게임 서버 연결 오류: {e}")

        # ✅ game_ui에 game_network 객체 추가
        game_ui.game_network = game_network
        game_ui.game_running = True
        # ✅ 이름 입력창 & 버튼 삭제 (게임 대기 화면으로 전환)
        name_input_box = None
        start_button = None



    else:
        ...# print("⚠️ 클라이언트 이름을 입력하세요!")

# ✅ 버튼 생성 (이벤트 방식 변경됨)
start_button = Button(
    img_normal=IMAGES["start_btn"],
    x=237, y=560,
    width=150, height=50,
    img_hover=IMAGES["start_btn_hover"],
    x_act=207, y_act=545,  
    action=start_game
)

name_input_box = InputBox(214, display_height // 2 + 150, 200, 40, korean_font, placeholder="Enter your name")

def main_loop():
    """🔥 메인 루프 실행"""
    global client_name, input_active, game_ui, name_input_box, game_network, game_started

    # ✅ 게임이 처음 실행될 때 BGM 재생
    if not hasattr(main_loop, "bgm_played"):
        SOUNDS["bgm_main"].play(-1)  # 🔥 BGM 반복 재생
        main_loop.bgm_played = True   # 🔥 중복 재생 방지

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print("🎮 게임 종료 중...")
                pygame.quit()
                chat_loop.stop()
                game_loop.stop()
                chat_loop_thread.join()
                game_loop_thread.join()
                return

            chat_ui.handle_event(event)
            if game_ui:
                game_ui.handle_event(event)

            if not game_started and name_input_box:
                result = name_input_box.handle_event(event)
                if result is not None:
                    client_name = result
                    # print(f"입력된 이름: {client_name}")

            if not game_started and start_button:
                start_button.handle_event(event)

        if game_started and game_ui:
            if game_ui.loading and not game_ui.game_running:
                # ✅ READY 상태에서 대기 화면 유지 (게임 시작 전까지)
                game_ui.draw(screen)
            
            elif game_ui.game_running:
                # ✅ 게임이 실행 중이면 게임 화면 표시
                # print(f"🔍 [DEBUG] game_running 상태: {game_ui.game_running}")
                game_ui.draw(screen)
                game_ui.update_game_state()

                # 🔥 game_logic이 None이 아닐 때만 running 확인
                if game_ui.game_logic and not game_ui.game_logic.running:
                    # print(f"⚠️ [WARN] game_ui.game_running이 False로 설정되지 않아 강제 변경")
                    game_ui.game_running = False
            
            elif not game_ui.game_running:
                # ✅ 게임이 종료되었으면 랭킹 화면 표시
                game_ui.show_ranking_screen()
                pygame.display.update()



        if not game_started:
            screen.blit(IMAGES["bg_main"], (0, 0))
            screen.blit(IMAGES["chat_bg"], (game_width, 0))

            if name_input_box:
                name_input_box.draw(screen)

            if start_button:
                start_button.draw(screen)

        chat_ui.draw(screen)

        pygame.display.update()
        clock.tick(60)




if __name__ == "__main__":
    main_loop()
