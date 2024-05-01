import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('スペースバトル')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sound', 'bullet_hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'sound', 'bullet_fire.mp3'))
# BULLET_HIT_SOUND.set_volume(0)
# BULLET_FIRE_SOUND.set_volume(0)

MAIN_FONT_PATH = os.path.join('assets', 'font', 'NotoSansJP-Regular.ttf')

HEALTH_FONT = pygame.font.Font(MAIN_FONT_PATH, 40)
WINNER_FONT = pygame.font.Font(MAIN_FONT_PATH, 100)

FPS = 60
MAX_HP = 2
VELOCITY = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Pygame has in-built events.
# Define custom events by using the USEREVENT constant and adding an integer to it.
# Event types reference: https://www.pygame.org/docs/ref/event.html
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'img', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'img', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'img', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red: pygame.Rect, yellow: pygame.Rect,
                red_bullets: list[pygame.Rect], yellow_bullets: list[pygame.Rect],
                red_health: int, yellow_health: int):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render(
        f'残機: {yellow_health}', 1, WHITE)
    red_health_text = HEALTH_FONT.render(
        f'残機: {red_health}', 1, WHITE)
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed: pygame.key.ScancodeWrapper, yellow: pygame.Rect):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed: pygame.key.ScancodeWrapper, red: pygame.Rect):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:  # DOWN
        red.y += VELOCITY


def handle_bullets(yellow_bullets: list[pygame.Rect], red_bullets: list[pygame.Rect],
                   yellow: pygame.Rect, red: pygame.Rect):
    """
    Handles movements of bullets and checks for collision with enemy spaceship.
    """

    # Handle yellow bullets; For each bullet, check if it collides with
    # red spaceship. If collided, post custom event RED_HIT
    for bullet in yellow_bullets:
        # Move bullet towards the right
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    # Handle red bullets; For each bullet, check if it collides with
    # yellow spaceship. If collided, post custom event YELLOW_HIT
    for bullet in red_bullets:
        # Move bullet towards the left
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text: str):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = MAX_HP
    yellow_health = MAX_HP

    clock = pygame.time.Clock()
    run = True

    # Game loop
    while run:
        # 60 FPS
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''

        if red_health <= 0:
            winner_text = 'Yellow Wins!'

        if yellow_health <= 0:
            winner_text = 'Red Wins!'

        if winner_text != '':
            # Display winner text for 5 seconds
            draw_winner(winner_text)
            pygame.time.delay(5000)
            break

        # Handle spaceship movements
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Handle movement and collision of bullets
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Clear screen, draw objects and update
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    # Call main() again to start a new game
    main()


if __name__ == '__main__':
    main()
