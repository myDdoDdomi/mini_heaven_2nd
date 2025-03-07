import pygame

class Button:
    def __init__(self, img_normal, x, y, width, height, img_hover, action=None):
        """
        버튼 생성
        :param img_normal: 기본 버튼 이미지
        :param x: 버튼 X 좌표
        :param y: 버튼 Y 좌표
        :param width: 버튼 가로 크기
        :param height: 버튼 세로 크기
        :param img_hover: 마우스 올렸을 때 버튼 이미지
        :param action: 클릭 시 실행할 함수
        """
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.rect = pygame.Rect(x, y, width, height)  # 버튼 위치 및 크기
        self.action = action  # 버튼 클릭 시 실행할 함수

    def draw(self, screen):
        """
        버튼을 화면에 그리기
        """
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # 마우스가 버튼 위에 있을 때
        if self.rect.collidepoint(mouse_pos):
            screen.blit(self.img_hover, (self.rect.x, self.rect.y))
            if mouse_click[0] and self.action is not None:
                self.action()  # 클릭된 경우 함수 실행
        else:
            screen.blit(self.img_normal, (self.rect.x, self.rect.y))
