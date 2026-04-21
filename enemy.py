class Enemy:
    def __init__(self, path, hp=100, speed=2, reward=10, color=(220, 50, 50)):
        self.path = path
        self.path_index = 1
        self.x, self.y = path[0]
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.reward = reward    # деньги за убийство
        self.color = color
        self.alive = True

    def update(self):
        target_x, target_y = self.path[self.path_index]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.alive = False
                return
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, screen):
        import pygame
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 12)

        # Полоска HP над врагом
        bar_width = 24
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, (150, 0, 0), (int(self.x) - 12, int(self.y) - 20, bar_width, 4))
        pygame.draw.rect(screen, (0, 220, 0), (int(self.x) - 12, int(self.y) - 20, int(bar_width * hp_ratio), 4))