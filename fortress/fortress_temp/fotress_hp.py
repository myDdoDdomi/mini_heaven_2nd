import pygame

# 이미지 로드
img_hp = [  # 하트 게이지 이미지 목록
    None,
    pygame.image.load("./img/hp0.png"),  # 하트 0
    pygame.image.load("./img/hp1.png"),  # 하트 1
    pygame.image.load("./img/h p2.png"),  # 하트 2
    pygame.image.load("./img/hp3.png"),  # 하트 3
    pygame.image.load("./img/hp4.png"),  # 하트 4
    pygame.image.load("./img/hp5.png"),  # 하트 5
]

# 현재 하트 게이지 값을 증가시키는 함수
def demage(hit, current):
    # hit이 True일 경우 하트 게이지를 증가
    if hit:
        current += 1  # 하트 게이지를 1 증가시킴
        # 최대 값이 5를 초과하지 않도록 제한
        if current > 5:
            current = 5
    return current

# 현재 하트 게이지를 화면에 표시하는 함수
def hp(current, game_display):
    # 하트 게이지 이미지를 표시
    if 0 <= current <= 5:
        game_display.blit(img_hp[current], (x_position, y_position))

# 사용 예시
current_hp = 0  # 초기 하트 게이지 값
hit_occurred = True  # 타격이 발생했는지 여부

# 타격이 발생했을 때 하트 게이지를 증가
current_hp = demage(hit_occurred, current_hp)

# 하트 게이지를 화면에 표시합니다.
hp(current_hp, game_display)

    