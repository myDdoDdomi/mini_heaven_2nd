import pygame
import asyncio
from resources.assets.assets import IMAGES, SOUNDS, img_neko, yaong  # img_neko 가져오기
from resources.components.ui_components import Button
from resources.neko_logic import GameLogic
import random

class GameUI:
    def __init__(self, x, y, width, height, font, game_network, game_loop, screen):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.game_network = game_network
        self.game_loop = game_loop
        self.ready = False  # ✅ 준비 상태 추가
        self.players = []  # ✅ 플레이어 목록
        self.loading = False  # ✅ 로딩 상태 추가
        self.loading_idx = 0  # ✅ 로딩 애니메이션 인덱스
        self.loading_counter = 0  # ✅ 프레임 카운터
        self.screen = screen  # ✅ 화면 객체 저장
        self.game_logic = None  # ✅ 게임 로직 클래스 인스턴스
        self.game_running = False # 🔥 게임 실행 상태 추가
        self.img_neko = img_neko
        self.game_logic = None
        # ✅ 리소스 활용 (배경 이미지, 사운드)
        self.bg_image = IMAGES["bg_game"]  # 🔥 기본 배경 설정
        self.count_bgm = SOUNDS["countdown"]  # 🔥 카운트다운 효과음
        self.ranking_scores = []
        # ✅ READY 버튼 생성
        self.ready_button = Button(
            img_normal=IMAGES["start_btn"],
            x=237, y=560,
            width=150, height=50,
            img_hover=IMAGES["start_btn_hover"],
            x_act=207, y_act=545,
            action=self.toggle_ready
        )

    def handle_event(self, event):
        """🔥 게임 UI에서 이벤트 처리"""
        if self.ready_button is not None:
            self.ready_button.handle_event(event)  # 🔥 버튼 클릭 이벤트 추가

    def toggle_ready(self):
        """🔥 READY 상태 변경 및 서버로 전송"""
        self.ready = True  # 🔥 READY 상태를 True로 변경
        # print(f"🎮 준비 상태 변경됨: {self.ready}")

        if self.game_network is None:
            # print("❌ game_network가 None입니다! send_ready 실행 불가")
            return

        if not self.game_network.connected:
            # print("❌ game_network가 아직 서버에 연결되지 않았습니다!")
            return

        # print("🚀 send_ready 실행 시도...")
        # print(f"🔍 game_network 상태 확인: {self.game_network}, connected: {self.game_network.connected}")

        try:
            future = asyncio.run_coroutine_threadsafe(
                self.game_network.send_ready(self.ready), self.game_loop
            )
            future.result(timeout=5)  
            # print("✅ send_ready 실행 완료!")
        except Exception as e:
            ...# print(f"❌ send_ready 실행 중 오류 발생: {e}")


        # ✅ READY 버튼 누르면 배경 변경 & 버튼 숨김
        self.bg_image = IMAGES["bg_loading"]  
        self.ready_button = None  
        self.loading = True 
 


    def draw(self, screen):
        """🔥 게임 UI 그리기"""
        screen.blit(self.bg_image, self.rect.topleft)

        # ✅ READY 버튼이 있을 때만 그리기
        if self.ready_button is not None:
            self.ready_button.draw(screen)

        # 🔥 READY를 누르지 않은 상태에서만 플레이어 목록 그림
        if not self.ready:
            start_x, start_y = 20, 20  
            spacing_x, spacing_y = 72, 72  
            max_cols = 8  

            for i, player in enumerate(self.players):
                row = i // max_cols  
                col = i % max_cols  
                neko_img = img_neko[(i % 6) + 1]  
                screen.blit(neko_img, (start_x + (col * spacing_x), start_y + (row * spacing_y)))

        # ✅ 블록 상태에 따라 렌더링 실행
        if self.game_logic:
            self.game_logic.draw_neko()
            self.game_logic.draw_cursor()  # 🔥 커서를 그림
        # ✅ 로딩 애니메이션 실행 (게임이 시작되지 않은 경우)
        if self.loading:
            self.loading_animation(screen)

    def update_players(self, players):
        """🔥 서버에서 받은 플레이어 목록 업데이트"""
        self.players = players
        yaong[random.choice(range(0,7))].play()
        # print(f"📜 [update_players()] 현재 플레이어 목록: {self.players}")  # ✅ 디버깅용

    def update_game_state(self):
        """🔥 게임 상태 업데이트"""
        if self.game_logic and self.game_logic.running:
            self.game_logic.update_game_state()

    def update_ranking(self, ranking_scores):
        """🔥 서버에서 받은 랭킹 정보를 저장"""
        self.ranking_scores = ranking_scores
        self.show_ranking_screen()

    def show_ranking_screen(self):
        """🔥 게임 종료 후 랭킹 화면 표시 (상위 5명)"""
        self.screen.blit(IMAGES["neko_ranking"], (0, 0))  # ✅ 랭킹 배경 설정
        FONT_PATH = "./resources/assets/Font/NanumSquareRoundR.ttf"
        font = pygame.font.Font(FONT_PATH, 60)  # ✅ 랭킹 폰트 크기 설정
        text_color = (0, 0, 0)  # 🔥 검정색 텍스트

        if self.ranking_scores:
            rank = 1
            for player_data in self.ranking_scores[:5]:  # ✅ 상위 5명만 표시
                player_name = player_data["player_name"]
                score = player_data["score"]

                txt = font.render(f"{player_name} : {score} pts", True, text_color)
                self.screen.blit(txt, (295, 130 + 100 * rank))  # ✅ 위치 조정
                rank += 1

    def loading_animation(self, screen):
        """🔥 로딩 애니메이션 (순차적으로 캐릭터 나타나고 사라짐)"""
        self.loading_counter += 1

        # ✅ 5프레임마다 이미지 변경
        if self.loading_counter % 5 == 0:
            self.loading_idx = (self.loading_idx + 1) % 4  # 0~3 반복

        # ✅ 캐릭터 등장 위치
        loading_positions = [
            (2 * 72 + 20, 8 * 72 + 20),
            (3 * 72 + 20, 8 * 72 + 20),
            (4 * 72 + 20, 8 * 72 + 20),
            (5 * 72 + 20, 8 * 72 + 20)
        ]

        # ✅ 현재 인덱스에 해당하는 캐릭터만 표시
        screen.blit(img_neko[self.loading_idx + 1], loading_positions[self.loading_idx])

    async def start_game(self):
        """🔥 게임 시작 (비동기 함수로 변경)"""
        # print("🔥 게임이 시작됩니다!")
        self.loading = False  
        self.bg_image = IMAGES["bg_game"]  
        self.game_logic = GameLogic(self)  

        # 🔥 비동기 함수이므로, game_logic.start_game()도 await으로 실행해야 함
        await self.game_logic.start_game()

