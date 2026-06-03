import pygame
import random

pygame.init()

info = pygame.display.Info()
SW, SH = info.current_w, info.current_h
IS_PHONE = SW < 800 or SH < 800

if IS_PHONE:
    W, H = SW, SH
else:
    W, H = 500, 700

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

BG = (15, 15, 30)
SNAKE_COLOR = (100, 255, 100)
HEAD_COLOR = (255, 255, 100)
FOOD_COLOR = (255, 80, 80)
BTN_COLOR = (40, 40, 60)
TEXT_COLOR = (255, 255, 255)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 24)

GRID = 20
COLS = W // GRID
ROWS = 14
FIELD_TOP = H // 2 - (ROWS * GRID) // 2 - 20
FIELD_H = ROWS * GRID

STATE_MENU = 0
STATE_PLAY = 1
state = STATE_MENU

snake = [(COLS // 2, ROWS // 2)]
dx, dy = 1, 0
food = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
score = 0
game_over = False
move_counter = 0

BTN_SIZE = 90
ARROW_GAP = 15
cx, cy = W // 2, FIELD_TOP + FIELD_H + 70


def spawn_food():
    while True:
        f = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if f not in snake:
            return f


def reset():
    global snake, dx, dy, food, score, game_over, state, move_counter
    snake = [(COLS // 2, ROWS // 2)]
    dx, dy = 1, 0
    food = spawn_food()
    score = 0
    game_over = False
    state = STATE_PLAY
    move_counter = 0


def draw_btn(x, y, w, h, text, color=BTN_COLOR, font_size=None):
    r = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, r, border_radius=10)
    use_font = pygame.font.Font(None, font_size) if font_size else small_font
    t = use_font.render(text, True, TEXT_COLOR)
    screen.blit(t, (x + w // 2 - t.get_width() // 2, y + h // 2 - t.get_height() // 2))
    return r


running = True
while running:
    screen.fill(BG)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if state == STATE_MENU:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                if btn_start.collidepoint(mx, my):
                    reset()
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_RETURN):
                    reset()

        elif state == STATE_PLAY:
            if e.type == pygame.KEYDOWN and not IS_PHONE:
                if e.key == pygame.K_UP and dy != 1:
                    dx, dy = 0, -1
                elif e.key == pygame.K_DOWN and dy != -1:
                    dx, dy = 0, 1
                elif e.key == pygame.K_LEFT and dx != 1:
                    dx, dy = -1, 0
                elif e.key == pygame.K_RIGHT and dx != -1:
                    dx, dy = 1, 0
                elif e.key == pygame.K_r and game_over:
                    reset()
                elif e.key == pygame.K_ESCAPE:
                    state = STATE_MENU
                    game_over = False

            if e.type == pygame.MOUSEBUTTONDOWN and IS_PHONE:
                mx, my = e.pos
                if not game_over:
                    if btn_up.collidepoint(mx, my) and dy != 1:
                        dx, dy = 0, -1
                    elif btn_down.collidepoint(mx, my) and dy != -1:
                        dx, dy = 0, 1
                    elif btn_left.collidepoint(mx, my) and dx != 1:
                        dx, dy = -1, 0
                    elif btn_right.collidepoint(mx, my) and dx != -1:
                        dx, dy = 1, 0
                if btn_restart.collidepoint(mx, my):
                    reset()
                if btn_menu.collidepoint(mx, my):
                    state = STATE_MENU
                    game_over = False

    if state == STATE_MENU:
        title = big_font.render("ЗМЕЙКА", True, (100, 255, 100))
        screen.blit(title, (W // 2 - title.get_width() // 2, H // 3 - 60))

        btn_start = draw_btn(W // 2 - 80, H // 2 - 20, 160, 50, "НАЧАТЬ ИГРУ", (30, 120, 30))

        hint = small_font.render("Нажми ПРОБЕЛ или кнопку", True, (150, 150, 150))
        screen.blit(hint, (W // 2 - hint.get_width() // 2, H // 2 + 50))

        device_text = small_font.render(
            "Режим: Телефон" if IS_PHONE else "Режим: Компьютер (стрелки)",
            True, (150, 150, 150)
        )
        screen.blit(device_text, (W // 2 - device_text.get_width() // 2, H // 2 + 80))

    elif state == STATE_PLAY:
        score_text = font.render(f"Счёт: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (W // 2 - score_text.get_width() // 2, FIELD_TOP - 50))

        top_btn_y = FIELD_TOP - 45
        btn_restart = draw_btn(10, top_btn_y, 90, 35, "ЗАНОВО", font_size=22)
        btn_menu = draw_btn(W - 100, top_btn_y, 90, 35, "МЕНЮ", font_size=22)

        field_rect = pygame.Rect(0, FIELD_TOP, W, FIELD_H)
        pygame.draw.rect(screen, (25, 25, 40), field_rect)

        for x in range(0, W, GRID):
            pygame.draw.line(screen, (35, 35, 50), (x, FIELD_TOP), (x, FIELD_TOP + FIELD_H))
        for y in range(FIELD_TOP, FIELD_TOP + FIELD_H, GRID):
            pygame.draw.line(screen, (35, 35, 50), (0, y), (W, y))

        fx, fy = food
        food_size = GRID + 2
        food_offset = -1
        pygame.draw.rect(screen, FOOD_COLOR,
                         (fx * GRID + food_offset, FIELD_TOP + fy * GRID + food_offset,
                          food_size, food_size), border_radius=6)

        for i, (sx, sy) in enumerate(snake):
            if i == 0:
                head_size = GRID + 4
                head_offset = -2
                pygame.draw.rect(screen, HEAD_COLOR,
                                 (sx * GRID + head_offset, FIELD_TOP + sy * GRID + head_offset,
                                  head_size, head_size), border_radius=6)
            else:
                pygame.draw.rect(screen, SNAKE_COLOR,
                                 (sx * GRID, FIELD_TOP + sy * GRID, GRID - 1, GRID - 1), border_radius=4)

        if IS_PHONE:
            btn_up = draw_btn(cx - BTN_SIZE // 2, cy - BTN_SIZE - ARROW_GAP // 2,
                              BTN_SIZE, BTN_SIZE, "▲", font_size=40)
            btn_down = draw_btn(cx - BTN_SIZE // 2, cy + ARROW_GAP // 2,
                                BTN_SIZE, BTN_SIZE, "▼", font_size=40)
            btn_left = draw_btn(cx - BTN_SIZE - ARROW_GAP // 2 - BTN_SIZE // 2, cy - BTN_SIZE // 2,
                                BTN_SIZE, BTN_SIZE, "◄", font_size=40)
            btn_right = draw_btn(cx + ARROW_GAP // 2 + BTN_SIZE // 2, cy - BTN_SIZE // 2,
                                 BTN_SIZE, BTN_SIZE, "►", font_size=40)

        if game_over:
            overlay = pygame.Surface((W, FIELD_H))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, FIELD_TOP))

            go = font.render("ИГРА ОКОНЧЕНА!", True, (255, 100, 100))
            screen.blit(go, (W // 2 - go.get_width() // 2, FIELD_TOP + FIELD_H // 2 - 20))

        if not game_over:
            move_counter += 1
            if move_counter >= 2:
                move_counter = 0
                nx = snake[0][0] + dx
                ny = snake[0][1] + dy

                if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS or (nx, ny) in snake:
                    game_over = True
                else:
                    snake.insert(0, (nx, ny))
                    if (nx, ny) == food:
                        score += 1
                        food = spawn_food()
                    else:
                        snake.pop()

    pygame.display.flip()
    clock.tick(8)

pygame.quit()
