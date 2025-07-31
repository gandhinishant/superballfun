import pygame
import random

class ConfettiParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 10)
        self.color = random.choice([
            (255, 0, 0), (0, 255, 0), (0, 128, 255),
            (255, 255, 0), (255, 0, 255), (255, 165, 0)
        ])
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-3, -1)
        self.gravity = 0.05
        self.lifetime = random.randint(240, 600)  # frames

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


class ConfettiManager:
    def __init__(self):
        self.particles = []

    def spawn(self, x, y, amount=30):
        for _ in range(amount):
            self.particles.append(ConfettiParticle(x, y))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
