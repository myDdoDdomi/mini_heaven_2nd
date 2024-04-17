import pygame
import time
import random
import math
import sys
pygame.init()

# 아이콘 이미지
new_icon = pygame.image.load("image/ball1.png")
new_icon=pygame.transform.scale(new_icon, (30, 30))
pygame.display.set_icon(new_icon)

# BGM 넣기
music=pygame.mixer.music.load('bgm/start_bgm_1.mp3')

fallSound=pygame.mixer.Sound('bgm/effect_fall.wav')
effect_ending=pygame.mixer.Sound('bgm/effect_ending.wav')
pygame.mixer.music.play()

# 스타트 페이지 이미지
background_start = [pygame.image.load(f"./image/main_background/{i}.png") for i in range(92)] # 스타트 배경
background_start = [pygame.transform.scale(image, (650, 977))for image in background_start]
title_start=pygame.image.load('image/title.png')
title_start=pygame.transform.scale(title_start, (577, 303))
btn_start = pygame.image.load("./image/start_btn.png") # 스타트 버튼
btn_start = pygame.transform.scale(btn_start, (350, 147))
btn_start_click = pygame.image.load("./image/start_btn2.png") # 클릭시 스타트 버튼
btn_start_click = pygame.transform.scale(btn_start_click, (350, 147))

# 플레이 페이지 이미지
background_play = [pygame.image.load(f"./image/background_{i}.png") for i in range(4)]

background_land_play = pygame.image.load("./image/land.jpg") # 플레이 배경
background_play = [pygame.transform.scale(image, (650, 977)) for image in background_play]
background_land_play = pygame.transform.scale(background_land_play, (630, 630))

# 앤드 페이지 이미지
background_end=pygame.image.load('image/ending_background.jpg')
background_end=pygame.transform.scale(background_end, (650, 977))
btn_end = pygame.image.load("./image/ending_replay_click.png") # 리플레이 버튼
btn_end = pygame.transform.scale(btn_end, (350, 147))
btn_end_click = pygame.image.load("./image/ending_replay.png") # 클릭시 리플레이 버튼
btn_end_click = pygame.transform.scale(btn_end_click, (350, 147))

winner_1=pygame.image.load("image/ending_player1_win.png")
winner_1=pygame.transform.scale(winner_1, (579, 277))
winner_2=pygame.image.load("image/ending_player2_win.png")
winner_2=pygame.transform.scale(winner_2, (579, 277))
winner=0

# 디스플레이 창 크기 설정
display_width = 650 # 가로 사이즈
display_height = 977 # 세로 사이즈

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("PONGDANG")

# 시작 버튼 스타트 배경 위에 blit
button_x = (display_width - btn_start.get_width()) // 2  # 가로 위치
button_y = (display_height - btn_start.get_height()) // 1.3  # 세로 위치
gameDisplay.blit(btn_start, (button_x, button_y)) # 버튼 built

# 배경 이미지 인덱스
current_background_index = 0
next_change_time = pygame.time.get_ticks() + 300  # 3초마다 이미지 변경

# 스타트 배경 bilt
gameDisplay.blit(background_start[current_background_index], (0, 0))


#메인 게임 필요 변수, 함수
def load_scaled_image(filepath, new_size):
    """ 이미지를 불러와서 지정된 크기로 조정합니다. """
    image = pygame.image.load(filepath).convert_alpha()  # 이미지를 불러옵니다.
    return pygame.transform.scale(image, new_size)  # 이미지의 크기를 조정합니다.


FIELD_WIDTH, FIELD_HEIGHT = 630, 630
FIELD_X, FIELD_Y = (display_width - FIELD_WIDTH) // 2, (display_height - FIELD_HEIGHT) // 2
CAP_RADIUS = 25
MAX_CAPS = 5  # Each player has 5 caps
font = pygame.font.Font(None, 36)
player_images = [
    load_scaled_image('image/ball2.png', (50, 50)),  # 플레이어 1 이미지
    load_scaled_image('image/ball3.png', (50, 50))   # 플레이어 2 이미지
]
current_player = 0
total_players = 2
caps_set = [0, 0]  # Tracks the number of caps set by each player
caps = []
movement_started = False
start_time = None


def initialize_caps():
    """ Initialize cap positions in a grid pattern ensuring no overlap and then shuffle """
    global caps
    caps = []
    grid_size = CAP_RADIUS * 2 + 5  # Grid size ensuring no overlap, add a little extra space
    cols = (FIELD_WIDTH // grid_size)
    rows = (FIELD_HEIGHT // grid_size)
    
    # Create a list of positions based on the grid
    positions = [(FIELD_X + (i % cols) * grid_size + CAP_RADIUS, FIELD_Y + (i // cols) * grid_size + CAP_RADIUS)
                 for i in range(cols * rows)]
    random.shuffle(positions)  # Shuffle the positions to get a random order

    for i in range(total_players):
        player_caps = []
        for j in range(MAX_CAPS):
            if positions:
                new_pos = positions.pop()
                player_caps.append({'position': list(new_pos), 'velocity': [0, 0], 'color': player_images[i], 'player': i, 'active': False})
        caps.append(player_caps)

    # In the unlikely event that there's still overlap, run another check and reposition caps
    for i, cap1 in enumerate(caps[0] + caps[1]):
        for cap2 in (caps[0] + caps[1])[i+1:]:
            while math.hypot(cap1['position'][0] - cap2['position'][0], cap1['position'][1] - cap2['position'][1]) < 2 * CAP_RADIUS:
                cap2['position'][0] = random.randint(FIELD_X + CAP_RADIUS, FIELD_X + FIELD_WIDTH - CAP_RADIUS)
                cap2['position'][1] = random.randint(FIELD_Y + CAP_RADIUS, FIELD_Y + FIELD_HEIGHT - CAP_RADIUS)

def start_movement():
    """ Begin the movement after both players have set their caps """
    global movement_started, start_time
    movement_started = True
    start_time = time.time()

def handle_mouse_events(event):
    """ Handle mouse events to set directions for the caps """
    global current_player, caps_set, movement_started, start_time, dragging_start_pos
    if event.type == pygame.MOUSEBUTTONDOWN and not movement_started:
        for cap in caps[current_player]:
            if not cap['active'] and math.hypot(event.pos[0] - cap['position'][0], event.pos[1] - cap['position'][1]) < CAP_RADIUS:
                cap['active'] = True
                dragging_start_pos = cap['position']  # Set the dragging start position
                return
    elif event.type == pygame.MOUSEBUTTONUP and any(cap['active'] for cap in caps[current_player]):
        for cap in caps[current_player]:
            if cap['active']:
                drag_vector = [event.pos[0] - dragging_start_pos[0], event.pos[1] - dragging_start_pos[1]]
                distance = math.hypot(*drag_vector)
                power = min(distance / 10, 15)  # Cap the power to prevent excessively high values
                cap['velocity'] = [-power * dim / distance for dim in drag_vector]
                cap['active'] = False
                caps_set[current_player] += 1
                dragging_start_pos = None  # Reset dragging position

        # Check if the current player has set directions for all their caps
        if caps_set[current_player] >= len([cap for cap in caps[current_player] if FIELD_X < cap['position'][0] < FIELD_X + FIELD_WIDTH and FIELD_Y < cap['position'][1] < FIELD_Y + FIELD_HEIGHT]):
            # Move to the next player if current player is done setting caps
            current_player = (current_player + 1) % total_players

        # If all players have set their caps, begin the movement
        if all(caps_set[p] >= len([cap for cap in caps[p] if FIELD_X < cap['position'][0] < FIELD_X + FIELD_WIDTH and FIELD_Y < cap['position'][1] < FIELD_Y + FIELD_HEIGHT]) for p in range(total_players)):
            start_movement()

def update_positions():
    """ Update positions of all caps based on their velocities and handle collisions """
    if not movement_started:
        return  # Do not update positions if the movement has not started
    if time.time() - start_time < 3:
        return  # Wait for 3 seconds before moving the caps
    for player_caps in caps:
        for cap in player_caps:
            cap['position'][0] += cap['velocity'][0]
            cap['position'][1] += cap['velocity'][1]
            cap['velocity'] = [0.98 * v for v in cap['velocity']]  # Apply friction
    handle_collisions()

def handle_collisions():
    """ Handle collisions between caps """
    all_caps = [cap for sublist in caps for cap in sublist]
    for i, cap1 in enumerate(all_caps):
        for cap2 in all_caps[i+1:]:
            dx, dy = cap1['position'][0] - cap2['position'][0], cap1['position'][1] - cap2['position'][1]
            distance = math.hypot(dx, dy)
            if distance < 2 * CAP_RADIUS:
                nx, ny = dx / distance, dy / distance
                v1n = nx * cap1['velocity'][0] + ny * cap1['velocity'][1]
                v2n = nx * cap2['velocity'][0] + ny * cap2['velocity'][1]
                cap1['velocity'][0] += v2n * nx - v1n * nx
                cap1['velocity'][1] += v2n * ny - v1n * ny
                cap2['velocity'][0] += v1n * nx - v2n * nx
                cap2['velocity'][1] += v1n * ny - v2n * ny

def draw_caps():
    """ Draw all caps using images """
    for player_index, player_caps in enumerate(caps):
        for cap in player_caps:
            image = player_images[cap['player']]
            rect = image.get_rect(center=(int(cap['position'][0]), int(cap['position'][1])))
            gameDisplay.blit(image, rect)

def remove_out_of_bounds_caps():
    """ Remove caps that have gone out of the playing field """
    global caps
    for i in range(total_players):
        # temp=caps
        caps[i] = [cap for cap in caps[i] if FIELD_X <= cap['position'][0] <= FIELD_X + FIELD_WIDTH and
                   FIELD_Y <= cap['position'][1] <= FIELD_Y + FIELD_HEIGHT]
        # if temp!=caps:
        #     fallSound.play()

def check_game_over():
    """ Check if the game is over and return the result """
    if not caps[0]:
        return 1  # Player 2 wins
    if not caps[1]:
        return 0  # Player 1 wins
    if not caps[0] and not caps[1]:
        return -1  # Draw
    return None  # Game is not over

def all_caps_stopped():
    """ Check if all caps have stopped moving """
    for player_caps in caps:
        for cap in player_caps:
            if math.hypot(*cap['velocity']) > 0.01:  # If any cap is still moving (above a small threshold)
                return False
    return True

def reset_for_next_turn():
    """ Reset variables for the next turn """
    global current_player, caps_set, movement_started, start_time
    current_player = 0
    caps_set = [0, 0]
    movement_started = False
    start_time = None
    for player_caps in caps:
        for cap in player_caps:
            cap['active'] = False  # No cap is currently being dragged
            cap['velocity'] = [0, 0]  # Reset the velocity of all caps



# 디스플레이 업데이트
pygame.display.update()

class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            gameDisplay.blit(img_in, (x, y))

def main():
    global next_change_time,current_background_index,current_player, movement_started, start_time, dragging_start_pos
    pygame.mixer.music.stop()
    
    pygame.mixer.music.load('bgm/main_bgm_1.mp3')
    pygame.mixer.music.play()
    initialize_caps()
    running = True
    winner = None
    dragging_start_pos = None  # Track the start position of a drag
    running = True
    next_change_time = pygame.time.get_ticks()
    while running:
        # 배경 이미지 변경
        
        if pygame.time.get_ticks() >= next_change_time:
            next_change_time += 300  # 3초 추가
            current_background_index = (current_background_index + 1) % len(background_play)
        
        gameDisplay.blit(background_play[current_background_index], (0, 0))
        gameDisplay.blit(background_land_play, (10,175))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not movement_started and winner is None:
                handle_mouse_events(event)

        if movement_started:
            if time.time() - start_time >= 3:
                update_positions()
                draw_caps()
                if all_caps_stopped():
                    remove_out_of_bounds_caps()
                    winner = check_game_over()
                    if winner is not None:
                        end_page(winner)
                          # End game after displaying the winner
                    else:
                        reset_for_next_turn()  # Prepare for the next turn
            else:
                # Draw a countdown timer on the gameDisplay
                countdown_timer = max(0, int(3 - (time.time() - start_time)))
                timer_surface = font.render(f"Moving in {countdown_timer}...", True, (255, 255, 255))
                gameDisplay.blit(timer_surface, (display_width // 2 - timer_surface.get_width() // 2, display_height // 2 - timer_surface.get_height() // 2))
        else:
            draw_caps()  # Draw caps only when not in movement

        # Draw the line while dragging
        if dragging_start_pos:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(gameDisplay, (255, 255, 255), dragging_start_pos, mouse_pos, 5)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
                
                
        pygame.display.update()
    pygame.quit()
    sys.exit()

# 이벤트 루프
def start_page():
    global next_change_time,current_background_index
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse_pos = pygame.mouse.get_pos()

        # 마우스 위치 확인
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_x, mouse_y = mouse_pos
        # if pygame.time.get_ticks() >= next_change_time:
        current_background_index = (current_background_index + 1) % len(background_start)
            # next_change_time += 80  # 3초 추가
        time.sleep(0.1)
        gameDisplay.blit(background_start[current_background_index], (0, 0))
        # gameDisplay.blit(background_start, (0, 0))
        gameDisplay.blit(title_start,(36,240))
        Button(btn_start, button_x, button_y, 350, 147, btn_start_click, button_x, button_y, main)
        
        pygame.display.update()
    pygame.quit()
    sys.exit()
    
# 이벤트 루프
def end_page(winner):
    effect_ending.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # if pygame.time.get_ticks() >= next_change_time:
        #     current_background_index = (current_background_index + 1) % len(background_start)
        #     next_change_time += 80  # 3초 추가
        gameDisplay.blit(background_end, (0, 0))
        if winner==0:
            gameDisplay.blit(winner_1, (35, 200))
        else:
            gameDisplay.blit(winner_2, (35, 200))
        # gameDisplay.blit(background_start, (0, 0))
        # gameDisplay.blit(title_start,(36,240))
        
        Button(btn_end, button_x, button_y, 350, 147, btn_end_click, button_x, button_y, start_page)
        
        pygame.display.update()
    pygame.quit()
    sys.exit()
    


if __name__ == '__main__':
    start_page()