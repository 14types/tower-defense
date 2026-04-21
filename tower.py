import pygame

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 150       # радиус обнаружения врага
        self.damage = 10       # урон за выстрел
        self.fire_rate = 60    # кадров между выстрелами (60 = раз в секунду)
        self.fire_timer = 0    # счётчик до следующего выстрела

    def update(self, enemies):
        # Уменьшаем таймер каждый кадр
        if self.fire_timer > 0:
            self.fire_timer -= 1
            return None

        # Ищем ближайшего врага в радиусе
        target = None
        for enemy in enemies:
            if not enemy.alive:
                continue
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx**2 + dy**2) ** 0.5
            if distance <= self.range:
                target = enemy
                break

        # Если нашли врага — стреляем
        if target:
            self.fire_timer = self.fire_rate
            return Bullet(self.x, self.y, target)

        return None

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 150, 255), (self.x - 15, self.y - 15, 30, 30))
        pygame.draw.circle(screen, (50, 150, 255), (self.x, self.y), self.range, 1)


class Bullet:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.damage = 10
        self.alive = True

    def update(self):
        if not self.target.alive:
            self.alive = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.speed:
            # Попали в врага
            self.target.hp -= self.damage
            if self.target.hp <= 0:
                self.target.alive = False
            self.alive = False
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 4)