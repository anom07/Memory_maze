import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
MAZE_WIDTH, MAZE_HEIGHT = 700, 600  # Maze area
INFO_PANEL_WIDTH = WIDTH - MAZE_WIDTH  # HUD area
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Maze: Shadow Pursuit")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
DARK_GREY = (30, 30, 30)
LIGHT_ORB = (255, 215, 0)

# Maze settings
TILE_SIZE = 40
ROWS, COLS = MAZE_HEIGHT // TILE_SIZE, MAZE_WIDTH // TILE_SIZE

# Fonts
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 40, bold=True)

# Player and Shadow
player_pos = [0, 0]
shadow_path = []
shadow_delay = 10  # Moves after 10 frames delay

# Timer and Score
start_time = time.time()
score = 0

# Light mechanic
darkness_level = 0
light_orbs = []

# Maze Generation
def generate_maze():
    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range((ROWS * COLS) // 3):  # Random walls
        maze[random.randint(0, ROWS-1)][random.randint(0, COLS-1)] = 1
    maze[0][0] = 0  # Start
    maze[ROWS-1][COLS-1] = 0  # Exit
    return maze

maze = generate_maze()

# Power-Ups and Orbs
def spawn_light_orbs():
    for _ in range(5):
        row, col = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if maze[row][col] == 0:
            light_orbs.append((row, col))

spawn_light_orbs()

# Flashback Feature
def flashback():
    overlay = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(WHITE)
    screen.blit(overlay, (0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, GREY, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.display.update()
    pygame.time.delay(1000)

# Dynamic Maze Changer
def dynamic_maze():
    for _ in range(5):
        row, col = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if (row, col) != (0, 0) and (row, col) != (ROWS-1, COLS-1):
            maze[row][col] = 1 if maze[row][col] == 0 else 0

# Draw Game
def draw_game():
    global darkness_level

    screen.fill(DARK_GREY)

    # Draw Maze
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, GREY, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw Exit
    pygame.draw.rect(screen, GREEN, ((COLS-1)*TILE_SIZE, (ROWS-1)*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw Light Orbs
    for orb in light_orbs:
        pygame.draw.circle(screen, LIGHT_ORB, (orb[1]*TILE_SIZE + TILE_SIZE//2, orb[0]*TILE_SIZE + TILE_SIZE//2), 8)

    # Draw Player and Shadow
    pygame.draw.rect(screen, BLUE, (player_pos[1]*TILE_SIZE, player_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    if len(shadow_path) > shadow_delay:
        shadow_pos = shadow_path[-shadow_delay]
        pygame.draw.rect(screen, RED, (shadow_pos[1]*TILE_SIZE, shadow_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Darkness Overlay
    darkness_overlay = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
    darkness_overlay.set_alpha(min(200, darkness_level))
    darkness_overlay.fill(BLACK)
    screen.blit(darkness_overlay, (0, 0))

    # Info Panel
    pygame.draw.rect(screen, BLACK, (MAZE_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT))
    pygame.draw.line(screen, WHITE, (MAZE_WIDTH, 0), (MAZE_WIDTH, HEIGHT), 3)

    score_text = font.render(f"Score: {score}", True, WHITE)
    time_text = font.render(f"Time: {int(time.time() - start_time)}s", True, WHITE)
    flashback_text = font.render("Press 'F' for Flashback", True, YELLOW)

    screen.blit(score_text, (MAZE_WIDTH + 10, 50))
    screen.blit(time_text, (MAZE_WIDTH + 10, 100))
    screen.blit(flashback_text, (MAZE_WIDTH + 10, 150))

    pygame.display.update()

# Game Loop
clock = pygame.time.Clock()
running = True
dynamic_timer = time.time()

while running:
    draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move_made = False

    if keys[pygame.K_UP] and player_pos[0] > 0 and maze[player_pos[0]-1][player_pos[1]] == 0:
        player_pos[0] -= 1
        move_made = True
    if keys[pygame.K_DOWN] and player_pos[0] < ROWS-1 and maze[player_pos[0]+1][player_pos[1]] == 0:
        player_pos[0] += 1
        move_made = True
    if keys[pygame.K_LEFT] and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1]-1] == 0:
        player_pos[1] -= 1
        move_made = True
    if keys[pygame.K_RIGHT] and player_pos[1] < COLS-1 and maze[player_pos[0]][player_pos[1]+1] == 0:
        player_pos[1] += 1
        move_made = True
    if keys[pygame.K_f]:
        flashback()

    if move_made:
        score += 1
        shadow_path.append(player_pos[:])
        darkness_level += 5  # Increase darkness with movement

    # Collect Light Orbs
    for orb in light_orbs[:]:
        if tuple(player_pos) == orb:
            light_orbs.remove(orb)
            darkness_level = max(0, darkness_level - 50)  # Reduce darkness

    # Dynamic Maze every 30 seconds
    if time.time() - dynamic_timer > 30:
        dynamic_maze()
        dynamic_timer = time.time()

    # Shadow Collision
    if len(shadow_path) > shadow_delay and player_pos == shadow_path[-shadow_delay]:
        lose_text = large_font.render("Caught by the Shadow!", True, RED)
        screen.blit(lose_text, (MAZE_WIDTH//4, HEIGHT//2 - 20))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Win Condition
    if player_pos == [ROWS-1, COLS-1]:
        win_text = large_font.render(f"You Escaped! Score: {score}", True, GREEN)
        screen.blit(win_text, (MAZE_WIDTH//6, HEIGHT//2 - 20))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    clock.tick(15)

pygame.quit()
