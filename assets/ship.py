# assets/ship.py
import pygame
from pygame.locals import *
import math
from assets.config import wrap_position, SCREEN_W, SCREEN_H
from assets.bullet import Bullet

SHIP_TURN_SPEED = 4       # degrees per frame
SHIP_ACCEL      = 0.25
SHIP_FRICTION   = 0.985
SHIP_MAX_SPEED  = 6.0
SHIP_COOLDOWN   = 12      # frames between shots

class Ship:
    def __init__(self, pos, lives=3):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0  # 0 degrees points up
        self.lives = lives
        self.bullets = []
        self.cooldown = 0

    def handle_input(self, keys):
        if keys[K_LEFT]:
            self.angle -= SHIP_TURN_SPEED
        if keys[K_RIGHT]:
            self.angle += SHIP_TURN_SPEED
        if keys[K_UP]:
            thrust = pygame.Vector2(0, -SHIP_ACCEL).rotate(self.angle)
            self.vel += thrust

        if keys[K_SPACE] and self.cooldown == 0:
            self.shoot()

    def shoot(self):
        self.bullets.append(Bullet(self.pos, self.angle))
        self.cooldown = SHIP_COOLDOWN

    def update(self):
        # speed cap & friction
        if self.vel.length() > SHIP_MAX_SPEED:
            self.vel.scale_to_length(SHIP_MAX_SPEED)
        self.vel *= SHIP_FRICTION
        self.pos += self.vel
        self.pos.xy = wrap_position(self.pos)

        if self.cooldown > 0:
            self.cooldown -= 1

        # update bullets
        alive = []
        for b in self.bullets:
            b.update()
            if b.alive():
                alive.append(b)
        self.bullets = alive

    def polygon(self):
        # triangle ship
        tip = pygame.Vector2(0, -16).rotate(self.angle) + self.pos
        left = pygame.Vector2(-10, 10).rotate(self.angle) + self.pos
        right = pygame.Vector2(10, 10).rotate(self.angle) + self.pos
        return [tip, left, right]

    def draw(self, surf):
        pygame.draw.polygon(surf, (255,255,255), self.polygon(), 2)
        for b in self.bullets:
            b.draw(surf)
