# assets/bullet.py
import pygame
from assets.config import wrap_position, SCREEN_W, SCREEN_H

BULLET_SPEED = 12
BULLET_LIFETIME = 60  # frames

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pygame.Vector2(pos)
        rad = angle * 3.14159265 / 180.0
        self.vel = pygame.Vector2(0, -BULLET_SPEED).rotate(angle)
        self.age = 0

    def update(self):
        self.pos += self.vel
        self.pos.xy = wrap_position(self.pos)
        self.age += 1

    def alive(self):
        return self.age < BULLET_LIFETIME

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), (*self.pos, 2, 2))
