import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants for the game
WINDOW_WIDTH, WINDOW_HEIGHT = 650, 977
FIELD_WIDTH, FIELD_HEIGHT = 630, 630
FIELD_X, FIELD_Y = (WINDOW_WIDTH - FIELD_WIDTH) // 2, (WINDOW_HEIGHT - FIELD_HEIGHT) // 2
CAP_RADIUS = 25
MAX_CAPS = 5  # Each player has 5 caps
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255)]  # Red for player 1, Blue for player 2

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pushing Game")
font = pygame.font.Font(None, 36)

# Game Variables
current_player = 0
total_players = 2
turn_complete = [False] * total_players
caps = []
friction = 0.5  # Damping factor to simulate friction (increased friction effect)

# Function to draw the playing field
def draw_field():
    pygame.draw.rect(screen, (0, 255, 0), (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT))

# Function to draw caps and their directions
def draw_caps():
    for cap in caps:
        pygame.draw.circle(screen, cap['color'], cap['position'], CAP_RADIUS)
        if cap['direction']:
            pygame.draw.line(screen, (255, 255, 255), cap['position'], 
                             [cap['position'][0] + cap['direction'][0], cap['position'][1] + cap['direction'][1]], 2)

# Initialize cap positions randomly within the field
def initialize_caps():
    global caps
    caps.clear()
    for i in range(total_players):
        for _ in range(MAX_CAPS):
            x = random.randint(FIELD_X + CAP_RADIUS, FIELD_X + FIELD_WIDTH - CAP_RADIUS)
            y = random.randint(FIELD_Y + CAP_RADIUS, FIELD_Y + FIELD_HEIGHT - CAP_RADIUS)
            caps.append({
                'position': [x, y],
                'velocity': [0, 0],
                'color': PLAYER_COLORS[i],
                'player': i,
                'active': False,
                'direction': None
            })

def detect_collisions():
    n = len(caps)
    for i in range(n):
        for j in range(i + 1, n):
            cap1, cap2 = caps[i], caps[j]
            dx, dy = cap1['position'][0] - cap2['position'][0], cap1['position'][1] - cap2['position'][1]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 2 * CAP_RADIUS:
                # Calculate response vector
                overlap = 2 * CAP_RADIUS - distance
                nx, ny = dx / distance, dy / distance  # Normalized normal vector
                # Displace caps to avoid overlapping
                displacement = overlap / 2
                cap1['position'][0] += nx * displacement
                cap1['position'][1] += ny * displacement
                cap2['position'][0] -= nx * displacement
                cap2['position'][1] -= ny * displacement
                # Reflect and apply friction to velocities
                v1i = [cap1['velocity'][0], cap1['velocity'][1]]
                v2i = [cap2['velocity'][0], cap2['velocity'][1]]
                cap1['velocity'][0] = friction * (v2i[0] - nx * (nx * v2i[0] + ny * v2i[1]))
                cap1['velocity'][1] = friction * (v2i[1] - ny * (nx * v2i[0] + ny * v2i[1]))
                cap2['velocity'][0] = friction * (v1i[0] - nx * (nx * v1i[0] + ny * v1i[1]))
                cap2['velocity'][1] = friction * (v1i[1] - ny * (nx * v1i[0] + ny * v1i[1]))

def move_caps():
    global caps
    for cap in caps:
        cap['position'][0] += int(cap['velocity'][0])
        cap['position'][1] += int(cap['velocity'][1])
        if cap['position'][0] < FIELD_X + CAP_RADIUS or cap['position'][0] > FIELD_X + FIELD_WIDTH - CAP_RADIUS or \
           cap['position'][1] < FIELD_Y + CAP_RADIUS or cap['position'][1] > FIELD_Y + FIELD_HEIGHT - CAP_RADIUS:
            caps = [c for c in caps if c != cap]  # Remove cap if it goes out of the field
            
def handle_mouse_events(event):
    global current_player
    if event.type == pygame.MOUSEBUTTONDOWN:
        for cap in caps:
            if cap['player'] == current_player and not cap['direction']:
                distance = math.sqrt((event.pos[0] - cap['position'][0]) ** 2 + (event.pos[1] - cap['position'][1]) ** 2)
                if distance < CAP_RADIUS:
                    cap['active'] = True
                    cap['direction'] = [0, 0]  # Initialize direction
                    break
    elif event.type == pygame.MOUSEBUTTONUP:
        for cap in caps:
            if cap['active']:
                cap['velocity'] = [-(event.pos[0] - cap['position'][0]) / 20, -(event.pos[1] - cap['position'][1]) / 20]
                cap['direction'] = [cap['velocity'][0] * 20, cap['velocity'][1] * 20]
                cap['active'] = False
        if all(not cap['active'] and cap['direction'] is not None for cap in caps if cap['player'] == current_player):
            turn_complete[current_player] = True
            if current_player == total_players - 1:
                pygame.time.set_timer(pygame.USEREVENT, 3000)  # 3-second countdown
            current_player = (current_player + 1) % total_players
            



def main():
    global current_player
    initialize_caps()
    clock = pygame.time.Clock()
    running = True
    countdown_active = False
    countdown_time = 3

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                handle_mouse_events(event)
            elif event.type == pygame.USEREVENT and all(turn_complete):
                countdown_active = True

        if countdown_active:
            if countdown_time > 0:
                countdown_time -= clock.get_time() / 1000
            else:
                move_caps()
                detect_collisions()

        screen.fill((0, 0, 0))
        draw_field()
        draw_caps()
        if countdown_active and countdown_time > 0:
            time_text = font.render(f"Starting in {int(countdown_time)}...", True, (255, 255, 255))
            screen.blit(time_text, (100, 100))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
