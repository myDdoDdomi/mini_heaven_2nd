import pygame
import time
class Player:
    
    def __init__(self, initial_position, side):
        self.position = initial_position
        self.damage = 1
        self.volume = 10
        self.side = side
        self.hp = 10
        self.angle = 0
        self.gauge = 0

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def angle_move(self, theta):
        self.angle += theta

    def charge(self, power):
        self.gauge += power

    def hit(self):
        self.hp -= (self.damage * damage_scale)

class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            self.gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            self.gameDisplay.blit(img_in, (x, y))