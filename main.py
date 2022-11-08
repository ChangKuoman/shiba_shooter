import pygame
import random

pygame.font.init()
pygame.display.set_caption("MEMORY SHIBAS")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# constants
WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
VEL = 5
MAX_BULLETS = 5
BULLET_VEL = 10
ENEMY_VEL = 5
SHIPS_EVERY_X_SECOND = 100

# fonts
NORMAL_FONT = pygame.font.SysFont("britannic", 30)
END_FONT = pygame.font.SysFont("britannic", 100)

# image
SHIBA = pygame.transform.flip(pygame.image.load("assets/shiba_53x42.png"), True, False)
ENEMY_SHIP = pygame.image.load("assets/ship_60x52.png")
SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load("assets/space_background.jpg"), (WIDTH, HEIGHT))

ENEMY_HITTED = pygame.USEREVENT + 1
SHIBA_HITTED = pygame.USEREVENT + 2


def draw_window(shiba, bullets, enemies, enemy_bullets, shiba_health, score):
    WINDOW.blit(SPACE_BACKGROUND, (0, 0))
    WINDOW.blit(SHIBA, (shiba.x, shiba.y))

    for enemy in enemies:
        WINDOW.blit(ENEMY_SHIP, (enemy.x, enemy.y))

    for bullet in enemy_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    score_text = NORMAL_FONT.render(f"Score: {score}", True, WHITE)
    shiba_health_text = NORMAL_FONT.render(f"Health: {shiba_health}", True , WHITE)
    WINDOW.blit(score_text, (WIDTH//2-score_text.get_width()//2, 40))
    WINDOW.blit(shiba_health_text, (WIDTH//2-shiba_health_text.get_width()//2, 20))

    pygame.display.update()


def shiba_movement(keys_pressed, shiba):
    if keys_pressed[pygame.K_w] and shiba.y - VEL > 0 + 20:  # UP
        shiba.y -= VEL
    if keys_pressed[pygame.K_s] and shiba.y + VEL + shiba.height < HEIGHT - 20:  # DOWN
        shiba.y += VEL


def handle_bullets(bullets, shiba, enemy_bullets, enemies):
    for bullet in bullets:
        bullet.x += BULLET_VEL
        for enemy in enemies:
            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HITTED))
                bullets.remove(bullet)
                enemies.remove(enemy)
        else:
            if bullet.x >= WIDTH:
                bullets.remove(bullet)

    for bullet in enemy_bullets:
        bullet.x -= BULLET_VEL
        if shiba.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SHIBA_HITTED))
            enemy_bullets.remove(bullet)
        elif bullet.x <= 0:
            enemy_bullets.remove(bullet)


def create_enemy(enemies):
    enemy = pygame.Rect(WIDTH, random.randint(20, HEIGHT-20-ENEMY_SHIP.get_height()), ENEMY_SHIP.get_width(), ENEMY_SHIP.get_height())
    enemies.append(enemy)


def enemies_movement(enemies, shiba):
    for enemy in enemies:
        enemy.x -= ENEMY_VEL
        if shiba.colliderect(enemy):
            pygame.event.post(pygame.event.Event(SHIBA_HITTED))
            enemies.remove(enemy)
        elif enemy.x <= 0:
            enemies.remove(enemy)


def create_enemies_bullets(enemies, enemy_bullets):
    for enemy in enemies:
        probability = random.randint(1, 100)
        if probability <= 1:
            bullet = pygame.Rect(enemy.x + enemy.width, enemy.y + enemy.height // 2 - 2, 10, 5)
            enemy_bullets.append(bullet)


def draw_ending(score):
    score_text = END_FONT.render(f"Final Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (WIDTH//2-score_text.get_width()//2, HEIGHT//2-score_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(10000)


def main():
    run = True
    clock = pygame.time.Clock()

    shiba = pygame.Rect(20, HEIGHT // 2 - SHIBA.get_height() // 2, SHIBA.get_width(), SHIBA.get_height())
    bullets = []
    enemy_bullets = []
    enemies = []
    shiba_health = 10
    score = 0
    time_counter = 0

    while run:
        time_counter += 1
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(shiba.x + shiba.width, shiba.y + shiba.height // 2 - 2, 10, 5)
                    bullets.append(bullet)

            if event.type == ENEMY_HITTED:
                score += 20
            if event.type == SHIBA_HITTED:
                shiba_health -= 1

        if time_counter == SHIPS_EVERY_X_SECOND:
            time_counter = 0
            create_enemy(enemies)

        keys_pressed = pygame.key.get_pressed()
        shiba_movement(keys_pressed, shiba)
        create_enemies_bullets(enemies, enemy_bullets)
        handle_bullets(bullets, shiba, enemy_bullets, enemies)
        enemies_movement(enemies, shiba)

        draw_window(shiba, bullets, enemies, enemy_bullets, shiba_health, score)

        if shiba_health <= 0:
            draw_ending(score)
            break

    pygame.quit()


if __name__ == "__main__":
    main()
