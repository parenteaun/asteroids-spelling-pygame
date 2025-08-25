# assets/ship.py
import pygame
from pygame.locals import *
import math
from assets.config import wrap_position, SCREEN_W, SCREEN_H, STARTING_LIVES
from assets.bullet import Bullet

SHIP_TURN_SPEED = 4       # degrees per frame
SHIP_ACCEL      = 0.25
SHIP_FRICTION   = 0.985
SHIP_MAX_SPEED  = 6.0
SHIP_COOLDOWN   = 12      # frames between shots
INVINCIBILITY_DURATION = 180  # 3 seconds at 60 FPS

class Ship:
    def __init__(self, pos, lives=STARTING_LIVES, sound_manager=None):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0  # 0 degrees points up
        self.lives = lives
        self.bullets = []
        self.cooldown = 0
        self.invincible = False
        self.invincibility_timer = 0
        self.sound_manager = sound_manager

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
        if self.sound_manager:
            self.sound_manager.play_sound('shoot')

    def take_damage(self):
        """Trigger invincibility when ship takes damage."""
        self.invincible = True
        self.invincibility_timer = INVINCIBILITY_DURATION

    def is_invincible(self):
        """Check if ship is currently invincible."""
        return self.invincible

    def update(self):
        # speed cap & friction
        if self.vel.length() > SHIP_MAX_SPEED:
            self.vel.scale_to_length(SHIP_MAX_SPEED)
        self.vel *= SHIP_FRICTION
        self.pos += self.vel
        self.pos.xy = wrap_position(self.pos)

        if self.cooldown > 0:
            self.cooldown -= 1

        # update invincibility timer
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False

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
        # Blinking animation when invincible
        if self.invincible and (self.invincibility_timer // 6) % 2 == 0:
            # Skip drawing every other frame for blinking effect
            pass
        else:
            pygame.draw.polygon(surf, (255,255,255), self.polygon(), 2)
        
        for b in self.bullets:
            b.draw(surf)
