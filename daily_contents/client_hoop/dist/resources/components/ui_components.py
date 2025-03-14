import pygame
import sys
import time

class Button:
    def __init__(self, img_normal, x, y, width, height, img_hover, x_act=None, y_act=None, action=None):
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.rect = pygame.Rect(x, y, width, height)  # 버튼 위치 및 크기
        self.action = action  # 버튼 클릭 시 실행할 함수
        self.x_act = x_act if x_act is not None else x
        self.y_act = y_act if y_act is not None else y
        self.clicked = False  # 🔥 클릭 상태 추가

    def draw(self, screen):
        """버튼을 화면에 그리기"""
        mouse_pos = pygame.mouse.get_pos()

        # 마우스가 버튼 위에 있으면 hover 이미지 표시
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.img_hover, (self.x_act, self.y_act))
        else:
            screen.blit(self.img_normal, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        """🔥 버튼 클릭 이벤트 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):  # 클릭된 위치가 버튼 안인지 확인
                self.clicked = True  # 🔥 버튼이 클릭됨
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):  
                if self.action:
                    self.action()  # 🔥 클릭 시 지정된 함수 실행
                self.clicked = False  # 클릭 상태 초기화

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)  # 비활성화 색상
        self.color_active = (0, 0, 0)  # 활성화 색상
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.active = False
        self.placeholder = placeholder
        self.ime_active = False  # IME (한글 입력기) 상태

    def handle_event(self, event):
        """ 이벤트 처리 (마우스 클릭 및 키보드 입력) """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 클릭하면 활성화/비활성화 토글
            if self.rect.collidepoint(event.pos):
                self.active = True
                pygame.key.start_text_input()  # ✅ 한글 입력 활성화
                self.ime_active = True
            else:
                self.active = False
                pygame.key.stop_text_input()  # ✅ 한글 입력 비활성화
                self.ime_active = False
            self.color = self.color_active if self.active else self.color_inactive

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:  # 엔터 키 처리
                    print(f"입력된 값: {self.text}")  # 콘솔에 출력
                    return self.text  # 입력한 값 반환 후
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # 한 글자 삭제
                else:
                    self.text += event.unicode  # ✅ 한글 포함 모든 문자 입력 가능

        elif event.type == pygame.TEXTINPUT and self.ime_active:
            """✅ 한글 입력 모드에서 TEXTINPUT 이벤트 사용"""
            self.text += event.text

    def draw(self, screen):
        """ 입력 박스 렌더링 """
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_to_render = self.text if self.text else self.placeholder
        txt_surface = self.font.render(text_to_render, True, (0, 0, 0))
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
