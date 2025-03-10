import pygame
import time

class Button:
    def __init__(self, img_normal, x, y, width, height, img_hover, x_act=None, y_act=None, action=None):
        """
        버튼 생성
        :param img_normal: 기본 버튼 이미지
        :param x: 버튼 X 좌표
        :param y: 버튼 Y 좌표
        :param width: 버튼 가로 크기
        :param height: 버튼 세로 크기
        :param img_hover: 마우스 올렸을 때 버튼 이미지
        :param x_act: 마우스 올렸을 때 이미지 변경 위치 X (None이면 기존 위치 유지)
        :param y_act: 마우스 올렸을 때 이미지 변경 위치 Y (None이면 기존 위치 유지)
        :param action: 클릭 시 실행할 함수
        """
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.rect = pygame.Rect(x, y, width, height)  # 버튼 위치 및 크기
        self.action = action  # 버튼 클릭 시 실행할 함수
        self.x_act = x_act if x_act is not None else x
        self.y_act = y_act if y_act is not None else y

    def draw(self, screen):
        """
        버튼을 화면에 그리기
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 마우스가 버튼 위에 있을 때
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.img_hover, (self.x_act, self.y_act))
            if mouse_click[0] and self.action is not None:
                time.sleep(0.2)  # 클릭 후 딜레이
                self.action()  # 클릭된 경우 함수 실행
        else:
            screen.blit(self.img_normal, (self.rect.x, self.rect.y))


class InputBox:
    def __init__(self, x, y, width, height, font, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.active = False  # 입력창이 클릭되었을 때만 활성화
        self.placeholder = placeholder  # 플레이스홀더 텍스트
        self.color_active = (50, 50, 250)  # 활성화 시 색상 (파란색)
        self.color_inactive = (200, 200, 200)  # 비활성화 시 색상 (회색)

    def handle_event(self, event):
        """마우스 클릭 및 키 입력 처리"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 클릭한 위치가 입력창이면 활성화, 아니면 비활성화
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False  # 엔터 입력 시 비활성화
                return self.text  # 입력값 반환
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # 글자 삭제
            else:
                self.text += event.unicode  # 문자 추가

        return None  # 입력값 없음

    def draw(self, screen):
        """입력창을 화면에 그리기"""
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect, 2)  # 테두리 색상
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  # 배경 색상

        # 텍스트 표시 (플레이스홀더 포함)
        text_surface = self.font.render(self.text if self.text else self.placeholder, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))