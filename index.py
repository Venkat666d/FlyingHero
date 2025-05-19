import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero vs Drones")
clock = pygame.time.Clock()

# Load & scale images once
bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Building variants
BUILDING_W, BUILDING_H = 100, 200
building_files = ["building.png", "building1.png", "building3.png"]
building_imgs = [
    pygame.transform.scale(pygame.image.load(fname).convert_alpha(), (BUILDING_W, BUILDING_H))
    for fname in building_files
]

enemy_img = pygame.image.load("enemy.jpg").convert_alpha()
ENEMY_W, ENEMY_H = 50, 50
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_W, ENEMY_H))

power_img = pygame.image.load("power.png").convert_alpha()
POWER_W, POWER_H = 40, 40
power_img = pygame.transform.scale(power_img, (POWER_W, POWER_H))

hero_img = pygame.image.load("hero.png").convert_alpha()
HERO_W, HERO_H = 60, 50
hero_img = pygame.transform.scale(hero_img, (HERO_W, HERO_H))

# Fonts
font = pygame.font.SysFont(None, 48)

def draw_text(text, size, color, x, y):
    f = pygame.font.SysFont(None, size)
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def reset_game():
    hero = pygame.Rect(100, HEIGHT//2, HERO_W, HERO_H)
    hero_movement = 0
    building_x = WIDTH
    current_building = random.choice(building_imgs)
    drone_timer = 0
    power_timer = 0
    score = 0
    drones = []
    powers = []
    return hero, hero_movement, building_x, current_building, drone_timer, power_timer, score, drones, powers

# Game constants
GRAVITY = 0.5
JUMP_STRENGTH = -7
BOOST_STRENGTH = -14
MAX_FALL = 8
BUILDING_SPEED = 4

# Initialize game state
hero, hero_movement, building_x, current_building, drone_timer, power_timer, score, drones, powers = reset_game()
game_active = True

# Main loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                hero_movement = JUMP_STRENGTH
        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                hero, hero_movement, building_x, current_building, drone_timer, power_timer, score, drones, powers = reset_game()
                game_active = True

    # Draw background
    screen.blit(bg, (0, 0))

    if game_active:
        # Hero
        hero_movement = min(hero_movement + GRAVITY, MAX_FALL)
        hero.y += int(hero_movement)
        screen.blit(hero_img, hero)
        hero_rect = hero

        # Building
        building_x -= BUILDING_SPEED
        if building_x < -BUILDING_W:
            building_x = WIDTH
            current_building = random.choice(building_imgs)
            score += 1
        building_y = HEIGHT - BUILDING_H
        screen.blit(current_building, (building_x, building_y))
        building_rect = pygame.Rect(building_x, building_y, BUILDING_W, BUILDING_H)

        # Drones
        drone_timer += 1
        if drone_timer > 80:
            drone_timer = 0
            y = random.randint(20, HEIGHT//2)
            drones.append(pygame.Rect(WIDTH, y, ENEMY_W, ENEMY_H))
        for d in drones[:]:
            d.x -= BUILDING_SPEED + 1
            screen.blit(enemy_img, d)
            if d.right < 0:
                drones.remove(d)

        # Power-ups
        power_timer += 1
        if power_timer > 300:
            power_timer = 0
            y = random.randint(HEIGHT//2, HEIGHT - POWER_H - 20)
            powers.append(pygame.Rect(WIDTH, y, POWER_W, POWER_H))
        for p in powers[:]:
            p.x -= BUILDING_SPEED
            screen.blit(power_img, p)
            if hero_rect.colliderect(p):
                hero_movement = BOOST_STRENGTH
                powers.remove(p)
            elif p.right < 0:
                powers.remove(p)

        # Collisions
        if (hero_rect.colliderect(building_rect)
            or any(hero_rect.colliderect(d) for d in drones)
            or hero.top < 0
            or hero.bottom > HEIGHT):
            game_active = False

        # Score
        draw_text(str(score), 48, (255, 255, 255), WIDTH//2, 40)

    else:
        draw_text("Game Over", 64, (255, 0, 0), WIDTH//2, HEIGHT//2 - 50)
        draw_text("Press R to Restart", 36, (255, 255, 255), WIDTH//2, HEIGHT//2 + 20)

    pygame.display.update()
    clock.tick(30)
