import pygame
import sys
from enemy import Enemy
from tower import Tower

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

PATH = [
    (0, 300),
    (200, 300),
    (200, 150),
    (500, 150),
    (500, 450),
    (800, 450)
]

# Состояние игры
money = 100
lives = 10
wave = 1
enemies = []
towers = []
bullets = []

# Волны — список списков врагов
# Каждая волна это список параметров для Enemy
WAVES = [
    [{"hp": 100, "speed": 2, "reward": 10, "color": (220, 50, 50)}] * 5,
    [{"hp": 150, "speed": 2, "reward": 15, "color": (220, 50, 50)}] * 7,
    [{"hp": 100, "speed": 4, "reward": 20, "color": (255, 165, 0)}] * 8,
    [{"hp": 300, "speed": 1, "reward": 30, "color": (180, 0, 180)}] * 5,
]

# Для спауна врагов с задержкой
spawn_timer = 0
spawn_delay = 60   # кадров между появлением врагов
current_wave_enemies = list(WAVES[0])
wave_started = True
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mx, my = pygame.mouse.get_pos()
            if money >= 50:
                towers.append(Tower(mx, my))
                money -= 50

    if not game_over:
        # Спаун врагов из текущей волны
        if current_wave_enemies:
            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                spawn_timer = 0
                params = current_wave_enemies.pop(0)
                enemies.append(Enemy(PATH, **params))

        # Обновление врагов
        for enemy in enemies:
            if enemy.alive:
                enemy.update()
            elif enemy.path_index >= len(PATH):
                # Враг дошёл до конца — забираем жизнь
                lives -= 1
                enemy.path_index = 0   # сбрасываем чтобы не считать дважды

        # Собираем деньги за убитых врагов
        for enemy in enemies:
            if not enemy.alive and enemy.reward > 0:
                money += enemy.reward
                enemy.reward = 0

        enemies = [e for e in enemies if e.alive or e.path_index > 0]

        # Обновление башен
        for tower in towers:
            bullet = tower.update(enemies)
            if bullet:
                bullets.append(bullet)

        # Обновление пуль
        for bullet in bullets:
            bullet.update()
        bullets = [b for b in bullets if b.alive]

        # Проверяем конец волны
        if not current_wave_enemies and not enemies:
            wave += 1
            if wave > len(WAVES):
                game_over = True
            else:
                current_wave_enemies = list(WAVES[wave - 1])
                money += 50   # бонус за волну

        # Проверяем проигрыш
        if lives <= 0:
            game_over = True

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

    # Интерфейс
    money_text = font.render(f"Деньги: {money}$  Башня: 50$", True, (255, 255, 255))
    lives_text = font.render(f"Жизни: {lives}", True, (255, 100, 100))
    wave_text = font.render(f"Волна: {wave}", True, (100, 255, 100))
    screen.blit(money_text, (10, 10))
    screen.blit(lives_text, (10, 45))
    screen.blit(wave_text, (10, 80))

    if game_over:
        if lives <= 0:
            msg = font.render("GAME OVER", True, (255, 50, 50))
        else:
            msg = font.render("ТЫ ПОБЕДИЛ!", True, (50, 255, 50))
        screen.blit(msg, (WIDTH // 2 - 80, HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)