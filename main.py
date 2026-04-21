import pygame
import sys
from enemy import Enemy
from tower import Tower

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()

PATH = [
    (0, 300),
    (200, 300),
    (200, 150),
    (500, 150),
    (500, 450),
    (800, 450)
]

enemies = [Enemy(PATH)]
towers = []
bullets = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ставим башню по клику мыши
            mx, my = pygame.mouse.get_pos()
            towers.append(Tower(mx, my))

    # Обновление врагов
    for enemy in enemies:
        if enemy.alive:
            enemy.update()

    # Обновление башен
    for tower in towers:
        bullet = tower.update(enemies)
        if bullet:
            bullets.append(bullet)

    # Обновление пуль
    for bullet in bullets:
        bullet.update()
    bullets = [b for b in bullets if b.alive]

    # Отрисовка
    screen.fill((30, 30, 30))
    pygame.draw.lines(screen, (80, 80, 80), False, PATH, 3)

    for enemy in enemies:
        if enemy.alive:
            enemy.draw(screen)

    for tower in towers:
        tower.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()
    clock.tick(60)