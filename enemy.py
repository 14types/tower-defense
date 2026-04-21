class Enemy:
    def __init__(self, path):
        self.path = path
        self.path_index = 1
        self.x, self.y = path[0]
        self.speed = 2
        self.hp = 100
        self.alive = True

    def update(self):
        # Берём следующую точку пути
        target_x, target_y = self.path[self.path_index]

        # Считаем разницу между текущей позицией и целевой
        dx = target_x - self.x
        dy = target_y - self.y

        # Считаем расстояние до цели
        distance = (dx**2 + dy**2) ** 0.5

        # Если мы почти дошли до точки — переключаемся на следующую
        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.alive = False  # враг дошёл до конца
                return
        else:
            # Двигаемся в сторону цели
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, (220, 50, 50), (int(self.x), int(self.y)), 12)