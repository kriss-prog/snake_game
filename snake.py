import pygame
import sys
import random

# Configuration & Layout
CELL_SIZE = 25
GRID_NUM = 20
SCORE_HEIGHT = 60
WIDTH = CELL_SIZE * GRID_NUM
HEIGHT = (CELL_SIZE * GRID_NUM) + SCORE_HEIGHT

# Color Palette (Upgraded with a subtle secondary tile color)
COLOR_BG = (28, 28, 32)
COLOR_BG_ALT = (33, 33, 38)  # For the checkerboard pattern
COLOR_HEADER = (20, 20, 23)
COLOR_SNAKE_HEAD = (46, 125, 50)
COLOR_SNAKE_BODY = (76, 175, 80)
COLOR_APPLE = (233, 30, 99)
COLOR_LEAF = (139, 195, 74)
COLOR_TEXT = (255, 255, 255)
COLOR_MUTED = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Snake Pro")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 24, bold=True)

# Game State Variables
snake = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
direction = pygame.Vector2(1, 0)
new_direction = direction
score = 0
high_score = 0  # High Score Tracker
game_over = False

def get_random_apple():
    while True:
        pos = pygame.Vector2(random.randint(0, GRID_NUM - 1), random.randint(0, GRID_NUM - 1))
        if pos not in snake:
            return pos

apple = get_random_apple()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game_over:
                # Reset Game (Keeps high score)
                snake = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
                direction = pygame.Vector2(1, 0)
                new_direction = direction
                apple = get_random_apple()
                score = 0
                game_over = False
            else:
                if event.key == pygame.K_w and direction.y == 0: new_direction = pygame.Vector2(0, -1)
                if event.key == pygame.K_s and direction.y == 0: new_direction = pygame.Vector2(0, 1)
                if event.key == pygame.K_a and direction.x == 0: new_direction = pygame.Vector2(-1, 0)
                if event.key == pygame.K_d and direction.x == 0: new_direction = pygame.Vector2(1, 0)

    if not game_over:
        direction = new_direction
        new_head = snake[0] + direction

        # Collision Logic
        if not (0 <= new_head.x < GRID_NUM and 0 <= new_head.y < GRID_NUM) or new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == apple:
                score += 1
                if score > high_score:
                    high_score = score
                apple = get_random_apple()
            else:
                snake.pop()

    # --- RENDER GRAPHICS ---
    screen.fill(COLOR_BG)

    # Top Bar Layout (Score & High Score Dashboard)
    pygame.draw.rect(screen, COLOR_HEADER, (0, 0, WIDTH, SCORE_HEIGHT))
    score_surf = font.render(f"SCORE: {score}", True, COLOR_TEXT)
    high_surf = font.render(f"BEST: {high_score}", True, COLOR_MUTED)
    screen.blit(score_surf, (20, (SCORE_HEIGHT - score_surf.get_height()) // 2))
    screen.blit(high_surf, (WIDTH - high_surf.get_width() - 20, (SCORE_HEIGHT - high_surf.get_height()) // 2))

    # Map Playing Grid
    map_surf = pygame.Surface((WIDTH, WIDTH))
    map_surf.fill(COLOR_BG)

    # Dynamic Feature: Checkerboard Background Generation
    for row in range(GRID_NUM):
        for col in range(GRID_NUM):
            if (row + col) % 2 == 0:
                tile_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(map_surf, COLOR_BG_ALT, tile_rect)

    # Model: The Apple
    apple_rect = pygame.Rect(apple.x * CELL_SIZE, apple.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(map_surf, COLOR_APPLE, apple_rect.inflate(-4, -4), border_radius=8)
    pygame.draw.circle(map_surf, COLOR_LEAF, (int(apple_rect.centerx + 4), int(apple_rect.top + 2)), 3)

    # Model: The Snake
    for i, block in enumerate(snake):
        block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        if i == 0: # Head Model
            pygame.draw.rect(map_surf, COLOR_SNAKE_HEAD, block_rect, border_radius=6)
            eye_offset_x = direction.x * 4
            eye_offset_y = direction.y * 4
            if direction.x != 0:
                pygame.draw.circle(map_surf, COLOR_TEXT, (int(block_rect.centerx + eye_offset_x), block_rect.centery - 4), 3)
                pygame.draw.circle(map_surf, COLOR_TEXT, (int(block_rect.centerx + eye_offset_x), block_rect.centery + 4), 3)
            else:
                pygame.draw.circle(map_surf, COLOR_TEXT, (block_rect.centerx - 4, int(block_rect.centery + eye_offset_y)), 3)
                pygame.draw.circle(map_surf, COLOR_TEXT, (block_rect.centerx + 4, int(block_rect.centery + eye_offset_y)), 3)
        else: # Body Model
            pygame.draw.rect(map_surf, COLOR_SNAKE_BODY, block_rect.inflate(-2, -2), border_radius=4)

    if game_over:
        go_surf = font.render("GAME OVER - Press Any Key", True, (255, 82, 82))
        map_surf.blit(go_surf, go_surf.get_rect(center=(WIDTH // 2, WIDTH // 2)))

    screen.blit(map_surf, (0, SCORE_HEIGHT))
    pygame.display.flip()
    
    # Dynamic Feature: Speed increases by 1 frame-per-second for every 3 points scored
    current_speed = 10 + (score // 3)
    clock.tick(current_speed)