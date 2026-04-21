import pygame
import sys
from enemy import Enemy

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()

# Путь врага — список точек (x, y)
PATH = [
    (0, 300),
    (200, 300),
    (200, 150),
    (500, 150),
    (500, 450),
    (800, 450)
]

# Создаём врага
enemy = Enemy(PATH)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Обновление
    if enemy.alive:
        enemy.update()

    # Отрисовка
    screen.fill((30, 30, 30))

    # Рисуем путь
    pygame.draw.lines(screen, (80, 80, 80), False, PATH, 3)

    # Рисуем врага
    enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)