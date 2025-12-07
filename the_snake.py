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


def handle_keydown(event, game_over):
    """Обработка нажатий клавиш."""
    if game_over:
        if event.key == pygame.K_SPACE:
            # Рестарт игры
            snake = [(WIDTH // 2, HEIGHT // 2)]
            direction = 'RIGHT'
            score = 0
            food = generate_food()
            speed = 10
            return snake, direction, score, food, speed, False
        return snake, direction, score, food, speed, game_over
    else:
        # Обработка управления
        if event.key == pygame.K_LEFT and direction != 'RIGHT':
            direction = 'LEFT'
        elif event.key == pygame.K_RIGHT and direction != 'LEFT':
            direction = 'RIGHT'
        elif event.key == pygame.K_UP and direction != 'DOWN':
            direction = 'UP'
        elif event.key == pygame.K_DOWN and direction != 'UP':
            direction = 'DOWN'
        elif event.key == pygame.K_a and direction != 'RIGHT':
            direction = 'LEFT'
        elif event.key == pygame.K_d and direction != 'LEFT':
            direction = 'RIGHT'
        elif event.key == pygame.K_w and direction != 'DOWN':
            direction = 'UP'
        elif event.key == pygame.K_s and direction != 'UP':
            direction = 'DOWN'
    
    return snake, direction, score, food, speed, game_over


def move_snake(snake, direction, game_over):
    """Движение змейки."""
    if game_over:
        return snake, game_over
    
    head_x, head_y = snake[0]

    if direction == 'LEFT':
        head_x -= BLOCK_SIZE
    elif direction == 'RIGHT':
        head_x += BLOCK_SIZE
    elif direction == 'UP':
        head_y -= BLOCK_SIZE
    elif direction == 'DOWN':
        head_y += BLOCK_SIZE

    new_head = (head_x, head_y)

    # Проверка столкновения со стенами
    if (head_x < 0
            or head_x >= WIDTH
            or head_y < 0
            or head_y >= HEIGHT
            or new_head in snake):
        game_over = True

    if not game_over:
        snake.insert(0, new_head)

    return snake, game_over


def check_food_collision(snake, food, score, speed):
    """Проверка столкновения с едой."""
    if not game_over and snake[0] == food:
        score += 10
        food = generate_food()
        speed = min(30, speed + 1)  # Постепенное увеличение скорости
        return food, score, speed
    return food, score, speed


def draw_game():
    """Отрисовка всех элементов игры."""
    # Отрисовка
    screen.fill(BLACK)

    # Рисуем сетку (опционально)
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

    # Рисуем змейку
    for i, (x, y) in enumerate(snake):
        color = GREEN if i == 0 else BLUE  # Голова зеленая, тело синее
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
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Отображаем скорость
    speed_text = small_font.render(f'Speed: {speed}', True, WHITE)
    screen.blit(speed_text, (10, 50))

    # Отображаем длину змейки
    length_text = small_font.render(f'Length: {len(snake)}', True, WHITE)
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
            # Если была рестарт
            if len(result) > 6:
                snake, direction, score, food, speed, game_over, _ = result

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
