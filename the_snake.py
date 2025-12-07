"""Snake Game - классическая игра змейка."""
import random
import sys

import pygame


# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Игровые переменные
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = 'RIGHT'
score = 0
game_over = False
speed = 10


def generate_food():
    """Генерация случайной позиции для еды."""
    while True:
        x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if (x, y) not in snake:
            return x, y


def handle_direction_key(event_key, current_direction):
    """Обработка клавиш направления."""
    key_mappings = {
        pygame.K_LEFT: ('LEFT', 'RIGHT'),
        pygame.K_RIGHT: ('RIGHT', 'LEFT'),
        pygame.K_UP: ('UP', 'DOWN'),
        pygame.K_DOWN: ('DOWN', 'UP'),
        pygame.K_a: ('LEFT', 'RIGHT'),
        pygame.K_d: ('RIGHT', 'LEFT'),
        pygame.K_w: ('UP', 'DOWN'),
        pygame.K_s: ('DOWN', 'UP'),
    }
    
    if event_key in key_mappings:
        new_dir, opposite_dir = key_mappings[event_key]
        if current_direction != opposite_dir:
            return new_dir
    return current_direction


def handle_keydown(event, current_game_over):
    """Обработка нажатий клавиш."""
    if current_game_over:
        if event.key == pygame.K_SPACE:
            # Рестарт игры
            new_snake = [(WIDTH // 2, HEIGHT // 2)]
            new_direction = 'RIGHT'
            new_score = 0
            new_food = generate_food()
            new_speed = 10
            return new_snake, new_direction, new_score, new_food, new_speed, False
        return snake, direction, score, food, speed, current_game_over
    
    new_direction = handle_direction_key(event.key, direction)
    return snake, new_direction, score, food, speed, current_game_over


def move_snake(current_snake, current_direction, current_game_over):
    """Движение змейки."""
    if current_game_over:
        return current_snake, current_game_over
    
    head_x, head_y = current_snake[0]

    if current_direction == 'LEFT':
        head_x -= BLOCK_SIZE
    elif current_direction == 'RIGHT':
        head_x += BLOCK_SIZE
    elif current_direction == 'UP':
        head_y -= BLOCK_SIZE
    elif current_direction == 'DOWN':
        head_y += BLOCK_SIZE

    new_head = (head_x, head_y)

    # Проверка столкновения со стенами
    if (head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
            or new_head in current_snake):
        current_game_over = True

    if not current_game_over:
        current_snake.insert(0, new_head)

    return current_snake, current_game_over


def draw_game():
    """Отрисовка всех элементов игры."""
    screen.fill(BLACK)

    # Рисуем сетку
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

    # Рисуем змейку
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else BLUE
        pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, WHITE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Рисуем еду
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.circle(
        screen,
        (200, 0, 0),
        (food[0] + BLOCK_SIZE // 2, food[1] + BLOCK_SIZE // 2),
        BLOCK_SIZE // 2,
    )

    # Отображаем счет
    score_msg = 'Score: ' + str(score)
    score_text = font.render(score_msg, True, WHITE)
    screen.blit(score_text, (10, 10))

    # Отображаем скорость
    speed_msg = 'Speed: ' + str(speed)
    speed_text = small_font.render(speed_msg, True, WHITE)
    screen.blit(speed_text, (10, 50))

    # Отображаем длину змейки
    length_msg = 'Length: ' + str(len(snake))
    length_text = small_font.render(length_msg, True, WHITE)
    screen.blit(length_text, (10, 80))

    # Сообщение Game Over
    if game_over:
        game_over_text = font.render('GAME OVER!', True, RED)
        restart_text = small_font.render('Press SPACE to restart', True, WHITE)

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30),
        )
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10),
        )

    # Инструкции по управлению
    controls_text = small_font.render(
        'Controls: ARROWS or WASD', True, (200, 200, 200)
    )
    screen.blit(controls_text, (WIDTH - controls_text.get_width() - 10, 10))

    pygame.display.flip()


# Генерация первой еды
food = generate_food()

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            result = handle_keydown(event, game_over)
            snake, direction, score, food, speed, game_over = result

    # Движение змейки
    snake, game_over = move_snake(snake, direction, game_over)

    # Проверка съедания еды
    if not game_over and snake[0] == food:
        score += 10
        food = generate_food()
        speed = min(30, speed + 1)
    elif not game_over and len(snake) > 1:
        snake.pop()

    # Отрисовка
    draw_game()
    clock.tick(speed)
