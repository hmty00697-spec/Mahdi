import pygame
import random
import math
import sys

pygame.init()

WIDTH = 480
HEIGHT = 850

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Glow Ball")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (60, 160, 255)
LIGHT_BLUE = (150, 220, 255)
PINK = (255, 80, 150)
DARK = (35, 45, 60)
GRAY = (230, 235, 240)

font_big = pygame.font.Font(None, 58)
font = pygame.font.Font(None, 42)
font_small = pygame.font.Font(None, 28)

MENU = 0
GAME = 1

state = MENU
paused = False

# =========================
# تنظیم ربات
# =========================

ai_level = 5

player_score = 0
ai_score = 0

# =========================
# پدال‌ها
# =========================

paddle_width = 120
paddle_height = 16

player_x = WIDTH / 2 - paddle_width / 2
player_y = HEIGHT - 80

ai_x = WIDTH / 2 - paddle_width / 2
ai_y = 55

# =========================
# توپ
# =========================

ball_radius = 15
ball_x = WIDTH / 2
ball_y = HEIGHT / 2

ball_speed = 5

ball_dx = 5
ball_dy = 5

touch_x = WIDTH / 2

# =========================
# دکمه‌های منو
# =========================

minus_button = pygame.Rect(
    65, 330, 80, 65
)

plus_button = pygame.Rect(
    335, 330, 80, 65
)

start_button = pygame.Rect(
    90, 500, 300, 75
)

# =========================
# دکمه Pause
# =========================

pause_button = pygame.Rect(
    WIDTH - 80,
    HEIGHT // 2 - 30,
    60,
    60
)

# =========================
# تنظیمات AI
# =========================

def get_ai_settings(level):

    speed = 0.035 + level * 0.008

    accuracy = 0.25 + level * 0.065

    prediction = 0.20 + level * 0.065

    mistake = 80 - level * 6

    return speed, accuracy, prediction, mistake


# =========================
# پس‌زمینه
# =========================

def draw_background():

    screen.fill(WHITE)

    wall = 20

    pygame.draw.line(
        screen,
        BLUE,
        (wall, 0),
        (wall, HEIGHT),
        7
    )

    pygame.draw.line(
        screen,
        BLUE,
        (WIDTH - wall, 0),
        (WIDTH - wall, HEIGHT),
        7
    )

    pygame.draw.line(
        screen,
        BLUE,
        (wall, wall),
        (WIDTH - wall, wall),
        7
    )

    pygame.draw.line(
        screen,
        PINK,
        (wall, HEIGHT - wall),
        (WIDTH - wall, HEIGHT - wall),
        7
    )


# =========================
# توپ
# =========================

def draw_ball():

    for r in range(32, ball_radius, -5):

        pygame.draw.circle(
            screen,
            (210, 235, 255),
            (int(ball_x), int(ball_y)),
            r,
            1
        )

    pygame.draw.circle(
        screen,
        LIGHT_BLUE,
        (int(ball_x), int(ball_y)),
        ball_radius
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(ball_x - 4),
            int(ball_y - 4)
        ),
        5
    )


# =========================
# پدال
# =========================

def draw_paddle(x, y, color):

    pygame.draw.rect(
        screen,
        color,
        (
            int(x),
            int(y),
            paddle_width,
            paddle_height
        ),
        border_radius=8
    )


# =========================
# ریست توپ
# =========================

def reset_ball(direction):

    global ball_x
    global ball_y
    global ball_dx
    global ball_dy

    ball_x = WIDTH / 2
    ball_y = HEIGHT / 2

    angle = random.uniform(
        math.radians(35),
        math.radians(145)
    )

    ball_dx = math.cos(angle) * ball_speed

    ball_dy = (
        math.sin(angle)
        * ball_speed
        * direction
    )


# =========================
# منوی ربات
# =========================

def draw_menu():

    draw_background()

    # عنوان
    title = font_big.render(
        "GLOW BALL",
        True,
        DARK
    )

    screen.blit(
        title,
        (
            WIDTH / 2 - title.get_width() / 2,
            90
        )
    )

    # زیرعنوان
    subtitle = font_small.render(
        "AI BATTLE",
        True,
        BLUE
    )

    screen.blit(
        subtitle,
        (
            WIDTH / 2 - subtitle.get_width() / 2,
            165
        )
    )

    # عنوان تنظیم ربات
    text = font.render(
        "AI LEVEL",
        True,
        DARK
    )

    screen.blit(
        text,
        (
            WIDTH / 2 - text.get_width() / 2,
            240
        )
    )

    # دکمه -
    pygame.draw.rect(
        screen,
        PINK,
        minus_button,
        border_radius=14
    )

    text = font_big.render(
        "-",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            minus_button.centerx
            - text.get_width() / 2,
            minus_button.centery
            - text.get_height() / 2
        )
    )

    # عدد سطح ربات
    text = font_big.render(
        str(ai_level),
        True,
        BLUE
    )

    screen.blit(
        text,
        (
            WIDTH / 2
            - text.get_width() / 2,
            315
        )
    )

    # دکمه +
    pygame.draw.rect(
        screen,
        BLUE,
        plus_button,
        border_radius=14
    )

    text = font_big.render(
        "+",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            plus_button.centerx
            - text.get_width() / 2,
            plus_button.centery
            - text.get_height() / 2
        )
    )

    # درجه سختی
    if ai_level <= 3:
        difficulty = "EASY"

    elif ai_level <= 7:
        difficulty = "NORMAL"

    else:
        difficulty = "HARD"

    text = font_small.render(
        difficulty,
        True,
        PINK
    )

    screen.blit(
        text,
        (
            WIDTH / 2
            - text.get_width() / 2,
            405
        )
    )

    # توضیح سطح
    text = font_small.render(
        "ROBOT POWER: " + str(ai_level) + "/10",
        True,
        DARK
    )

    screen.blit(
        text,
        (
            WIDTH / 2
            - text.get_width() / 2,
            440
        )
    )

    # START
    pygame.draw.rect(
        screen,
        PINK,
        start_button,
        border_radius=16
    )

    text = font.render(
        "START",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            start_button.centerx
            - text.get_width() / 2,
            start_button.centery
            - text.get_height() / 2
        )
    )


# =========================
# پیش‌بینی توپ
# =========================

def predict_ball_x():

    if ball_dy >= 0:
        return ball_x

    distance = ball_y - ai_y

    if distance <= 0:
        return ball_x

    time = distance / abs(ball_dy)

    predicted = ball_x + ball_dx * time

    left = 20
    right = WIDTH - 20

    for i in range(20):

        if predicted < left:

            predicted = left + (left - predicted)

        elif predicted > right:

            predicted = right - (predicted - right)

        else:

            break

    return predicted


# =========================
# حرکت ربات
# =========================

def update_ai():

    global ai_x

    speed, accuracy, prediction, mistake = \
        get_ai_settings(ai_level)

    if ball_dy < 0:

        predicted = predict_ball_x()

        target = (
            ball_x * (1 - prediction)
            + predicted * prediction
        )

        target -= paddle_width / 2

        if random.random() > accuracy:

            target += random.uniform(
                -mistake,
                mistake
            )

    else:

        target = (
            WIDTH / 2
            - paddle_width / 2
        )

    min_x = 20
    max_x = WIDTH - 20 - paddle_width

    target = max(
        min_x,
        min(max_x, target)
    )

    ai_x += (
        target - ai_x
    ) * speed


# =========================
# آپدیت بازی
# =========================

def update_game():

    global player_x
    global ball_x
    global ball_y
    global ball_dx
    global ball_dy
    global player_score
    global ai_score

    # بازیکن
    target_x = (
        touch_x
        - paddle_width / 2
    )

    player_x += (
        target_x - player_x
    ) * 0.45

    player_x = max(
        20,
        min(
            WIDTH - 20 - paddle_width,
            player_x
        )
    )

    # ربات
    update_ai()

    # توپ
    ball_x += ball_dx
    ball_y += ball_dy

    # دیوار چپ
    if ball_x - ball_radius <= 20:

        ball_x = 20 + ball_radius

        ball_dx = abs(ball_dx)

    # دیوار راست
    if ball_x + ball_radius >= WIDTH - 20:

        ball_x = (
            WIDTH
            - 20
            - ball_radius
        )

        ball_dx = -abs(ball_dx)

    # =========================
    # برخورد با ربات
    # =========================

    ai_rect = pygame.Rect(
        int(ai_x),
        int(ai_y),
        paddle_width,
        paddle_height
    )

    ball_rect = pygame.Rect(
        int(ball_x - ball_radius),
        int(ball_y - ball_radius),
        ball_radius * 2,
        ball_radius * 2
    )

    if (
        ball_dy < 0
        and ball_rect.colliderect(ai_rect)
    ):

        ball_y = (
            ai_y
            + paddle_height
            + ball_radius
        )

        ball_dy = abs(ball_dy)

        hit = (
            ball_x
            - (
                ai_x
                + paddle_width / 2
            )
        )

        ball_dx += hit * 0.025

    # =========================
    # برخورد با بازیکن
    # =========================

    player_rect = pygame.Rect(
        int(player_x),
        int(player_y),
        paddle_width,
        paddle_height
    )

    if (
        ball_dy > 0
        and ball_rect.colliderect(player_rect)
    ):

        ball_y = (
            player_y
            - ball_radius
        )

        ball_dy = -abs(ball_dy)

        hit = (
            ball_x
            - (
                player_x
                + paddle_width / 2
            )
        )

        ball_dx += hit * 0.025

    # محدود کردن سرعت
    max_speed = 8

    ball_dx = max(
        -max_speed,
        min(max_speed, ball_dx)
    )

    # =========================
    # امتیاز
    # =========================

    if ball_y < -30:

        player_score += 1

        reset_ball(1)

    if ball_y > HEIGHT + 30:

        ai_score += 1

        reset_ball(-1)


# =========================
# دکمه Pause
# =========================

def draw_pause_button():

    pygame.draw.circle(
        screen,
        GRAY,
        pause_button.center,
        30
    )

    if paused:

        pygame.draw.polygon(
            screen,
            DARK,
            [
                (
                    pause_button.centerx - 8,
                    pause_button.centery - 15
                ),
                (
                    pause_button.centerx - 8,
                    pause_button.centery + 15
                ),
                (
                    pause_button.centerx + 14,
                    pause_button.centery
                )
            ]
        )

    else:

        pygame.draw.rect(
            screen,
            DARK,
            (
                pause_button.centerx - 11,
                pause_button.centery - 15,
                7,
                30
            ),
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            DARK,
            (
                pause_button.centerx + 4,
                pause_button.centery - 15,
                7,
                30
            ),
            border_radius=3
        )


# =========================
# رسم بازی
# =========================

def draw_game():

    draw_background()

    # امتیاز ربات
    text = font.render(
        str(ai_score),
        True,
        BLUE
    )

    screen.blit(
        text,
        (
            WIDTH / 2
            - text.get_width() / 2,
            70
        )
    )

    # امتیاز بازیکن
    text = font.render(
        str(player_score),
        True,
        PINK
    )

    screen.blit(
        text,
        (
            WIDTH / 2
            - text.get_width() / 2,
            HEIGHT - 125
        )
    )

    # سطح ربات
    text = font_small.render(
        "AI " + str(ai_level),
        True,
        BLUE
    )

    screen.blit(
        text,
        (35, 105)
    )

    draw_paddle(
        ai_x,
        ai_y,
        BLUE
    )

    draw_paddle(
        player_x,
        player_y,
        PINK
    )

    draw_ball()

    # صفحه توقف
    if paused:

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(180)

        overlay.fill(WHITE)

        screen.blit(
            overlay,
            (0, 0)
        )

        text = font_big.render(
            "PAUSED",
            True,
            DARK
        )

        screen.blit(
            text,
            (
                WIDTH / 2
                - text.get_width() / 2,
                HEIGHT / 2
                - text.get_height() / 2
            )
        )

    draw_pause_button()


# =========================
# شروع دوباره بازی
# =========================

def start_game():

    global player_score
    global ai_score
    global player_x
    global ai_x
    global touch_x
    global paused
    global state

    player_score = 0
    ai_score = 0

    player_x = (
        WIDTH / 2
        - paddle_width / 2
    )

    ai_x = (
        WIDTH / 2
        - paddle_width / 2
    )

    touch_x = WIDTH / 2

    reset_ball(1)

    paused = False

    state = GAME


# =========================
# حلقه اصلی
# =========================

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =====================
        # لمس
        # =====================

        elif event.type == pygame.FINGERDOWN:

            x = event.x * WIDTH
            y = event.y * HEIGHT

            if state == MENU:

                if minus_button.collidepoint(x, y):

                    ai_level = max(
                        1,
                        ai_level - 1
                    )

                elif plus_button.collidepoint(x, y):

                    ai_level = min(
                        10,
                        ai_level + 1
                    )

                elif start_button.collidepoint(x, y):

                    start_game()

            else:

                if pause_button.collidepoint(x, y):

                    paused = not paused

                elif not paused:

                    touch_x = x

        # =====================
        # حرکت انگشت
        # =====================

        elif event.type == pygame.FINGERMOTION:

            if (
                state == GAME
                and not paused
            ):

                touch_x = event.x * WIDTH

        # =====================
        # موس
        # =====================

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if state == MENU:

                if minus_button.collidepoint(x, y):

                    ai_level = max(
                        1,
                        ai_level - 1
                    )

                elif plus_button.collidepoint(x, y):

                    ai_level = min(
                        10,
                        ai_level + 1
                    )

                elif start_button.collidepoint(x, y):

                    start_game()

            else:

                if pause_button.collidepoint(x, y):

                    paused = not paused

                elif not paused:

                    touch_x = x

        elif event.type == pygame.MOUSEMOTION:

            if (
                state == GAME
                and not paused
                and pygame.mouse.get_pressed()[0]
            ):

                touch_x = event.pos[0]

        # =====================
        # کیبورد
        # =====================

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                if state == GAME:

                    paused = not paused

                else:

                    running = False

    # =========================
    # اجرا
    # =========================

    if state == MENU:

        draw_menu()

    else:

        if not paused:

            update_game()

        draw_game()

    pygame.display.flip()


pygame.quit()
sys.exit()
