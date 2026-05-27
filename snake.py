import pygame
import sys
import random

CELL_SIZE = 25
GRID_NUM = 20
SCORE_HEIGHT = 60
WIDTH = CELL_SIZE * GRID_NUM
HEIGHT = (CELL_SIZE * GRID_NUM) + SCORE_HEIGHT

COLOR_BG = (28, 28, 32)
COLOR_BG_ALT = (33, 33, 38)
COLOR_HEADER = (20, 20, 23)
COLOR_SNAKE_HEAD = (46, 125, 50)
COLOR_SNAKE_BODY = (76, 175, 80)
COLOR_SNAKE_GOLD = (255, 215, 0)
COLOR_APPLE = (233, 30, 99)
COLOR_GOLD_APPLE = (255, 193, 7)
COLOR_LEAF = (139, 195, 74)
COLOR_TEXT = (255, 255, 255)
COLOR_MUTED = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern Snake Pro")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 24, bold=True)

snake = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
direction = pygame.Vector2(1, 0)
new_direction = direction
score = 0
high_score = 0
game_over = False

apple = None
gold_apple = None
gold_timer = 0
apples_eaten = 0
gold_glow_duration = 0

def get_random_item_pos():
    while True:
        pos = pygame.Vector2(random.randint(0, GRID_NUM - 1), random.randint(0, GRID_NUM - 1))
        if pos not in snake and pos != apple and (gold_apple is None or pos != gold_apple):
            return pos

apple = get_random_item_pos()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game_over:
                snake = [pygame.Vector2(5, 10), pygame.Vector2(4, 10), pygame.Vector2(3, 10)]
                direction = pygame.Vector2(1, 0)
                new_direction = direction
                gold_apple = None
                gold_timer = 0
                apples_eaten = 0
                apple = get_random_item_pos()
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

        if gold_apple:
            gold_timer -= 1
            if gold_timer <= 0:
                gold_apple = None

        if gold_glow_duration > 0:
            gold_glow_duration -= 1

        if not (0 <= new_head.x < GRID_NUM and 0 <= new_head.y < GRID_NUM) or new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == apple:
                score += 1
                apples_eaten += 1
                if score > high_score: high_score = score
                
                if apples_eaten % 5 == 0:
                    gold_apple = get_random_item_pos()
                    gold_timer = 55
                
                apple = get_random_item_pos()
            elif gold_apple and new_head == gold_apple:
                score += 5
                if score > high_score: high_score = score
                gold_apple = None
                gold_glow_duration = 20
            else:
                snake.pop()

    screen.fill(COLOR_BG)

    pygame.draw.rect(screen, COLOR_HEADER, (0, 0, WIDTH, SCORE_HEIGHT))
    score_surf = font.render(f"SCORE: {score}", True, COLOR_TEXT)
    high_surf = font.render(f"BEST: {high_score}", True, COLOR_MUTED)
    screen.blit(score_surf, (20, (SCORE_HEIGHT - score_surf.get_height()) // 2))
    screen.blit(high_surf, (WIDTH - high_surf.get_width() - 20, (SCORE_HEIGHT - high_surf.get_height()) // 2))
    
    if gold_apple:
        timer_surf = font.render(f"GOLD: {int(gold_timer//11)+1}s", True, COLOR_GOLD_APPLE)
        screen.blit(timer_surf, (WIDTH // 2 - timer_surf.get_width() // 2, (SCORE_HEIGHT - timer_surf.get_height()) // 2))

    map_surf = pygame.Surface((WIDTH, WIDTH))
    map_surf.fill(COLOR_BG)

    for row in range(GRID_NUM):
        for col in range(GRID_NUM):
            if (row + col) % 2 == 0:
                pygame.draw.rect(map_surf, COLOR_BG_ALT, pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    apple_rect = pygame.Rect(apple.x * CELL_SIZE, apple.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(map_surf, COLOR_APPLE, apple_rect.inflate(-4, -4), border_radius=8)
    pygame.draw.circle(map_surf, COLOR_LEAF, (int(apple_rect.centerx + 4), int(apple_rect.top + 2)), 3)

    if gold_apple:
        g_apple_rect = pygame.Rect(gold_apple.x * CELL_SIZE, gold_apple.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(map_surf, COLOR_GOLD_APPLE, g_apple_rect.inflate(-2, -2), border_radius=8)
        pygame.draw.circle(map_surf, COLOR_TEXT, (int(g_apple_rect.centerx + 4), int(g_apple_rect.top + 2)), 3)

    for i, block in enumerate(snake):
        block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        
        current_body_color = COLOR_SNAKE_GOLD if gold_glow_duration > 0 else COLOR_SNAKE_BODY
        current_head_color = COLOR_SNAKE_GOLD if gold_glow_duration > 0 else COLOR_SNAKE_HEAD

        if i == 0:
            pygame.draw.rect(map_surf, current_head_color, block_rect, border_radius=6)
            eye_offset_x, eye_offset_y = direction.x * 4, direction.y * 4
            eye_color = (0, 0, 0) if gold_glow_duration > 0 else COLOR_TEXT
            if direction.x != 0:
                pygame.draw.circle(map_surf, eye_color, (int(block_rect.centerx + eye_offset_x), block_rect.centery - 4), 3)
                pygame.draw.circle(map_surf, eye_color, (int(block_rect.centerx + eye_offset_x), block_rect.centery + 4), 3)
            else:
                pygame.draw.circle(map_surf, eye_color, (block_rect.centerx - 4, int(block_rect.centery + eye_offset_y)), 3)
                pygame.draw.circle(map_surf, eye_color, (block_rect.centerx + 4, int(block_rect.centery + eye_offset_y)), 3)
        else:
            pygame.draw.rect(map_surf, current_body_color, block_rect.inflate(-2, -2), border_radius=4)

    if game_over:
        go_surf = font.render("GAME OVER - Press Any Key", True, (255, 82, 82))
        map_surf.blit(go_surf, go_surf.get_rect(center=(WIDTH // 2, WIDTH // 2)))

    screen.blit(map_surf, (0, SCORE_HEIGHT))
    pygame.display.flip()
    clock.tick(11 + (score // 3))