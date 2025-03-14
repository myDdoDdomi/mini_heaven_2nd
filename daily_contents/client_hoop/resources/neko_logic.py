import pygame
import random
import time
from resources.assets.assets import IMAGES, SOUNDS, img_neko
import asyncio

class GameLogic:
    def __init__(self, game_ui):
        self.game_ui = game_ui
        self.screen = game_ui.screen
        self.map_y = 10
        self.map_x = 8
        self.point = 0
        self.tiover = 64
        self.neko = [[random.choice(range(1, 7)) for _ in range(8)] for _ in range(10)]
        self.check = [[0 for _ in range(8)] for _ in range(10)]
        self.search = [[0 for _ in range(8)] for _ in range(10)]
        self.cursor = IMAGES["cursor"]
        self.clock = pygame.time.Clock()
        self.running = False  
        self.timer = 0  
        self.mouse = Mouse(self, self.cursor, self.map_x, self.map_y)  
        self.idx = 0  
        self.state_timer = 0  
        self.font_countdown = pygame.font.Font(None, 160)
        self.my_ten = pygame.font.Font(None, 80)

    async def start_game(self):
        """🔥 게임 시작"""
        # print("🔥 게임 시작!")

        # ✅ 게임 시작 시 bgm_main 정지
        if "bgm_main" in SOUNDS:
            SOUNDS["bgm_main"].stop()  # 🔥 배경음악 중지
        self.running = True
        self.timer = time.time()

    def update_game_state(self):
        """🔥 게임 상태 업데이트 (시간, 점수, 블록 검사 등)"""
        if not self.running:
            return

        elapsed_time = time.time() - self.timer
        time_remaining = max(0, self.tiover - elapsed_time)

        # ✅ 3초 카운트다운 (게임 시작 전 대기)
        if elapsed_time < 4:
            countdown = 4 - int(elapsed_time)
            txt_countdown = self.font_countdown.render(str(countdown), True, (0, 0, 0))
            self.screen.blit(txt_countdown, [400, 350])

            # ✅ 카운트다운이 처음 시작될 때 효과음 재생
            if countdown == 4 and not hasattr(self, "countdown_played"):
                SOUNDS["countdown"].play()
                self.countdown_played = True  # ✅ 중복 재생 방지

            # 🔥 3초 동안 블록 제거 로직 실행 (점수에는 반영하지 않음)
            if self.idx == 0:
                """🔹 블록 검사 (초기 블록 제거)"""
                if self.check_neko(0) > 0:
                    self.idx = 1  

            elif self.idx == 1:
                """🔹 블록 변환 (7로 변환)"""
                self.check_neko(1)
                self.state_timer = time.time()
                self.idx = 2  

            elif self.idx == 2:
                """🔹 변환된 블록 제거 (7을 0으로 바꾸기)"""
                if time.time() - self.state_timer > 0.3:
                    self.sweep_neko()  # 🔥 점수는 증가시키지 않음
                    self.idx = 0

            self.drop_neko()
            return  # 🔥 마우스 입력은 받지 않음 (3초 동안)

        # ✅ 게임이 시작되었을 때 배경 음악(BGM) 플레이 (랜덤 선택)
        if not hasattr(self, "bgm_played"):
            bgm_key = random.choice(["bgm_game1", "bgm_game2", "bgm_game3"])
            SOUNDS[bgm_key].play(-1)  # 🔥 -1을 넣으면 반복 재생됨
            self.bgm_played = True

        if time_remaining <= 0:
            self.game_over()  # 🔥 시간 초과 시 게임 종료
            return  # ✅ 종료 후 추가 로직 실행하지 않도록 return
            
        # ✅ 블록이 채워질 때까지 drop_neko() 반복 실행
        if self.has_empty_spaces():
            self.drop_neko()  # 🔥 빈 공간이 있으면 drop_neko

            # 🔥 블록이 내려오는 모습이 보이도록 대기 시간 추가
            self.state_timer = time.time()  
            while time.time() - self.state_timer < 0.1:  # 🔥 0.5초 동안 대기
                self.screen.blit(IMAGES["bg_game"],[0,0])
                txt = self.my_ten.render(str(round(time_remaining, 1)), True, (255, 255, 255))
                txt_2 = self.my_ten.render(str(self.point), True, (255, 255, 255))
                self.screen.blit(txt, [690, 50])
                self.screen.blit(txt_2, [690, 150])
                self.draw_neko()  # 🔥 현재 블록 상태 갱신
                pygame.display.update()
            else :
                self.mouse.cursor_reset()
                self.mouse.turn = 0
            return  


        # ✅ 3초 이후 정상적인 게임 진행
        if self.idx == 0:
            """🔹 기본 상태: 마우스 입력 가능"""
            self.idx = self.check_neko(0)  # 🔥 블록 검사 후 변경 (일치하는 블록이 있으면 idx 변경)

        elif self.idx == 1:
            """🔹 블록 검사 (3개 이상 일치하는지 체크)"""
            if self.check_neko(0) > 0:
                self.idx = 2  # 🔥 블록 변환 단계로 이동
            else:
                self.idx = 0  # 🔄 일치하는 블록이 없으면 기본 상태로 돌아감

        elif self.idx == 2:
            """🔹 블록 변환 (7로 변환)"""
            self.check_neko(1)
            self.state_timer = time.time()
            SOUNDS[random.choice(["effect1", "effect2", "effect3"])].play()  # 🔥 효과음 랜덤 재생
            self.idx = 3  

        elif self.idx == 3:
            """🔹 변환된 블록 제거 (7을 0으로 바꾸기)"""
            if time.time() - self.state_timer > 0.3:
                self.point += self.sweep_neko()  # 🔥 이제는 점수 반영
                self.idx = 0  # 🔥 다시 기본 상태로 돌아감
            # 🔥 점수 & 남은 시간 표시
            txt = self.my_ten.render(str(round(time_remaining, 1)), True, (255, 255, 255))
            txt_2 = self.my_ten.render(str(self.point), True, (255, 255, 255))
            self.screen.blit(txt, [690, 50])
            self.screen.blit(txt_2, [690, 150])
            return


        self.mouse.get_move()
        self.draw_cursor()

        # 🔥 점수 & 남은 시간 표시
        txt = self.my_ten.render(str(round(time_remaining, 1)), True, (255, 255, 255))
        txt_2 = self.my_ten.render(str(self.point), True, (255, 255, 255))
        self.screen.blit(txt, [690, 50])
        self.screen.blit(txt_2, [690, 150])

    def game_over(self):
        """🔥 게임 종료 처리"""
        # print(f"🎯 게임 종료! 점수: {self.point}")
        # ✅ 게임 루프 종료
        self.running = False
        self.game_ui.game_running = False  # 🔥 게임이 종료되었음을 표시
        # print(f"🔍 [DEBUG] game_running 상태 변경됨: {self.game_ui.game_running}")

        # ✅ 서버에 게임 종료 상태 전송
        if self.game_ui.game_network:
            asyncio.run_coroutine_threadsafe(
                self.game_ui.game_network.send_finish(self.point),
                self.game_ui.game_loop
            )


    def has_empty_spaces(self):
        """🔥 빈 공간이 있는지 확인"""
        for y in range(10):
            for x in range(8):
                if self.neko[y][x] == 0:
                    return True  # 🔥 빈 공간이 있으면 True 반환
        return False  # 🔥 모든 칸이 채워졌으면 False 반환

    def check_neko(self, idx):
        """🔥 블록 검사 (같은 블록 3개 이상 있는지 체크)"""
        for y in range(10):
            for x in range(8):
                self.search[y][x] = self.neko[y][x]

        # ✅ 세로 방향 검사 (상하)
        for y in range(1, 9):
            for x in range(8):
                if self.search[y][x] > 0:
                    if self.search[y - 1][x] == self.search[y][x] and self.search[y + 1][x] == self.search[y][x]:
                        self.neko[y - 1][x] = 7
                        self.neko[y][x] = 7
                        self.neko[y + 1][x] = 7
                        idx = 1  # 🔥 매칭된 경우

        # ✅ 가로 방향 검사 (좌우) 추가
        for y in range(10):
            for x in range(1, 7):
                if self.search[y][x] > 0:
                    if self.search[y][x - 1] == self.search[y][x] and self.search[y][x + 1] == self.search[y][x]:
                        self.neko[y][x - 1] = 7
                        self.neko[y][x] = 7
                        self.neko[y][x + 1] = 7
                        idx = 1  # 🔥 매칭된 경우

        return idx  # ✅ 수정된 check_neko 함수 (좌우 검사 포함)

    def sweep_neko(self):
        """🔥 블록 제거 및 점수 합산"""
        self.tiover += 0.5
        cnt = 1
        for y in range(10):
            for x in range(8):
                if self.neko[y][x] == 7:
                    self.neko[y][x] = 0
                    if cnt < 200:
                        cnt *= 2
        return 20 * cnt

    def drop_neko(self):
        """🔥 블록 떨어뜨리기"""
        for y in range(10):
            for x in range(8):
                if y >= 1 and self.neko[y][x] == 0:
                    self.neko[y][x] = self.neko[y - 1][x]
                    self.neko[y - 1][x] = 0
                if y == 0 and self.neko[y][x] == 0:
                    self.neko[y][x] = random.choice(range(1, 7))

    def draw_neko(self):
        """🔥 블록 그리기"""
        for y in range(10):
            for x in range(8):
                if self.neko[y][x] > 0:
                    self.screen.blit(self.game_ui.img_neko[self.neko[y][x]], (x * 72 + 20, y * 72 + 20))

    def draw_cursor(self):
        """🔥 선택된 블록과 마우스 위치에 커서를 표시"""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for y in range(self.map_y):
            for x in range(self.map_x):
                # ✅ 선택된 블록은 항상 표시
                if self.check[y][x] == 1:
                    self.screen.blit(self.cursor, (x * 72 + 20, y * 72 + 20))

                    # ✅ turn == 1일 때, 선택된 블록의 상하좌우에 마우스를 올려야 커서 표시
                    if self.mouse.turn == 1:
                        if y - 1 >= 0 and x * 72 + 20 <= mouse_x < (x + 1) * 72 + 20 and (y - 1) * 72 + 20 <= mouse_y < y * 72 + 20:
                            self.screen.blit(self.cursor, (x * 72 + 20, (y - 1) * 72 + 20))  # 🔥 위쪽 블록
                        if y + 1 < self.map_y and x * 72 + 20 <= mouse_x < (x + 1) * 72 + 20 and (y + 1) * 72 + 20 <= mouse_y < (y + 2) * 72 + 20:
                            self.screen.blit(self.cursor, (x * 72 + 20, (y + 1) * 72 + 20))  # 🔥 아래쪽 블록
                        if x - 1 >= 0 and y * 72 + 20 <= mouse_y < (y + 1) * 72 + 20 and (x - 1) * 72 + 20 <= mouse_x < x * 72 + 20:
                            self.screen.blit(self.cursor, ((x - 1) * 72 + 20, y * 72 + 20))  # 🔥 왼쪽 블록
                        if x + 1 < self.map_x and y * 72 + 20 <= mouse_y < (y + 1) * 72 + 20 and (x + 1) * 72 + 20 <= mouse_x < (x + 2) * 72 + 20:
                            self.screen.blit(self.cursor, ((x + 1) * 72 + 20, y * 72 + 20))  # 🔥 오른쪽 블록

                # ✅ turn == 0일 때, 마우스가 위치한 곳 어디든 커서 표시
                elif self.mouse.turn == 0 and x * 72 + 20 <= mouse_x < (x + 1) * 72 + 20 and y * 72 + 20 <= mouse_y < (y + 1) * 72 + 20:
                    self.screen.blit(self.cursor, (x * 72 + 20, y * 72 + 20))  # ✅ 마우스 위치한 블록에도 커서 표시


    def check_switch(self, y, x):
        """🔥 블록을 스왑한 후 3개 이상 일치하는 블록이 있는지 확인"""
        for i in range(10):
            for j in range(8):
                self.search[i][j] = self.neko[i][j]

        for i in range(1, 9):
            for j in range(8):
                if self.search[i][j] > 0:
                    if self.search[i - 1][j] == self.search[i][j] and self.search[i + 1][j] == self.search[i][j]:
                        return True  # 🔥 3개 이상 일치하는 경우 True 반환

        for i in range(10):
            for j in range(1, 7):
                if self.search[i][j] > 0:
                    if self.search[i][j - 1] == self.search[i][j] and self.search[i][j + 1] == self.search[i][j]:
                        return True  # 🔥 3개 이상 일치하는 경우 True 반환
        return False  # 🔥 3개 이상 일치하는 블록이 없으면 False 반환

class Mouse:
    def __init__(self, game_logic, cursor, map_x, map_y):
        self.turn = 0
        self.map_y = map_y
        self.map_x = map_x
        self.cursor = cursor
        self.game_logic = game_logic  # 🔥 GameLogic 객체 참조
    
    def get_move(self):
        """🔥 마우스 이동 & 클릭 감지"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for y in range(self.map_y):
            for x in range(self.map_x):
                if x*72+20 < mouse[0] < (x+1)*72+20 and y*72+20 < mouse[1] < (y+1)*72+20:
                    if self.turn == 0:
                        self.game_logic.screen.blit(self.cursor, (x*72+20, y*72+20))
                        if click[0]:
                            # print(f"{self.turn} click {self.game_logic.check[y][x]}")
                            self.game_logic.check[y][x] = 1  # ✅ 여기 수정
                            self.turn = 1
                            # print(f"{self.turn} after click")
                    else:
                        if (y+1 < self.map_y and self.game_logic.check[y+1][x] == 1) or \
                            (0 <= y-1 and self.game_logic.check[y-1][x] == 1) or \
                            (x+1 < self.map_x and self.game_logic.check[y][x+1] == 1) or \
                            (0<= x-1 and self.game_logic.check[y][x-1] == 1):

                            self.game_logic.screen.blit(self.cursor, (x*72+20, y*72+20))
                            if click[0]:
                                # print(f"{self.turn} click {self.game_logic.check[y][x]}")
                                self.switch_neko(y, x)
                                if not self.game_logic.check_switch(y, x):
                                    self.switch_neko(y, x)
                                self.cursor_reset()
                                self.turn = 0
                        if click[2]:
                            self.cursor_reset()
                            self.turn = 0

    def is_adjacent(self, y, x):
        """🔥 인접한 블록인지 확인"""
        return (
            (y + 1 < self.map_y and self.game_logic.check[y + 1][x] == 1) or
            (y - 1 >= 0 and self.game_logic.check[y - 1][x] == 1) or
            (x + 1 < self.map_x and self.game_logic.check[y][x + 1] == 1) or
            (x - 1 >= 0 and self.game_logic.check[y][x - 1] == 1)
        )

    def switch_neko(self, y, x):
        """🔥 블록 스왑"""
        for i in range(10):
            for j in range(8):
                if self.game_logic.check[i][j] == 1:
                    # 🔥 스왑 전 임시 저장
                    temp = self.game_logic.neko[i][j]
                    self.game_logic.neko[i][j] = self.game_logic.neko[y][x]
                    self.game_logic.neko[y][x] = temp

                    # 🔥 유효한 조합인지 확인
                    if not self.game_logic.check_switch(y, x):  
                        # 🔄 유효하지 않으면 원래 상태로 복구
                        self.game_logic.neko[y][x] = self.game_logic.neko[i][j]
                        self.game_logic.neko[i][j] = temp

                    self.cursor_reset()
                    self.turn = 0

    def cursor_reset(self):
        """🔥 선택 해제"""
        # print("발동?")
        self.game_logic.check = [[0 for _ in range(8)] for _ in range(10)]
