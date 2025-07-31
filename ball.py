import random
import pygame

from peg import Peg

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = float(0.0)
        self.vy = float(0.0)
        self.gravity = float(0.5)
        self.touching_goal = False
        self.queue_delete = False
        self.confetti = False
        self.split = False
        self.explode = False

    def update(self, pegs):
        self.vy += self.gravity

        steps = int(max(abs(self.vx), abs(self.vy)) // self.radius) + 1
        dx = self.vx / steps
        dy = self.vy / steps

        for _ in range(steps):
            self.x += dx
            self.y += dy

            # check collision each small step
            for peg in pegs:
                self.bounce_off_peg(peg)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    def bounce_off_peg(self, peg: Peg):
        if peg.type == "EMPTY": 
            return

        dx = self.x - peg.x
        dy = self.y - peg.y
        dist = (dx**2 + dy**2)**0.5
        if dist == 0:
            return  # avoid division by zero

        if dist < self.radius + peg.radius:
            peg.effects(self)

            nx = dx / dist
            ny = dy / dist
            overlap = self.radius + peg.radius - dist

            # reflect velocity
            dot = self.vx * nx + self.vy * ny
            self.vx -= 2 * dot * nx
            self.vy -= 2 * dot * ny

            # move ball out of peg
            self.x += nx * overlap
            self.y += ny * overlap

            # dampen bounce
            self.vx *= peg.bounciness
            self.vy *= peg.bounciness

            # add small randomness
            self.vx += random.uniform(-0.5, 0.5)

            # apply min bounce force if too slow
            min_bounce = 2
            if abs(self.vx) < min_bounce:
                self.vx += min_bounce * (1 if self.vx >= 0 else -1)
            if abs(self.vy) < min_bounce:
                self.vy += min_bounce * (1 if self.vy >= 0 else -1)
