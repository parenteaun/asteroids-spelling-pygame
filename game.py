#!/usr/bin/env python3
"""
Asteroids‑Spelling – Minimal skeleton
"""

import math
import random
import pygame
from pygame.locals import *
from collections import deque

# ----- CONSTANTS -------------------------------------------------
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
SHIP_TURN_SPEED = 5          # degrees per frame
SHIP_ACCEL = 0.25
SHIP_FRICTION = 0.99
BULLET_SPEED = 10
MAX_LIVES = 10
TARGET_WORD = "ASTEROID"

# ----- HELPER FUNCTIONS ------------------------------------------
def wrap_position(pos):
    """Wrap around screen edges."""
    x, y = pos
    return (
        x % SCREEN_W,
        y % SCREEN_H
    )

def rotate_vector(vec, angle_deg):
    """Rotate a 2‑vector by angle degrees."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    x, y = vec
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

# ----- CLASSES ----------------------------------------------------
class Ship:
    def __init__(self):
        self.pos = pygame.Vector2(SCREEN_W / 2, SCREEN_H / 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0          # 0 points up
        self.lives = MAX_LIVES
        self.bullets = []       # list of Bullet
        self.cooldown = 0

    def handle_input(self, keys):
        if keys[K_LEFT]:
            self.angle -= SHIP_TURN_SPEED
        if keys[K_RIGHT]:
            self.angle += SHIP_TURN_SPEED
        if keys[K_UP]:
            # Accelerate in direction of ship
            rad = math.radians(self.angle)
            thrust = pygame.Vector2(-math.sin(rad), -math.cos(rad))
            self.vel += thrust * SHIP_ACCEL

        if self.cooldown <= 0 and keys[K_SPACE]:
            self.shoot()
            self.cooldown = 15   # frames

    def shoot(self):
        # Bullet starts at ship tip
        rad = math.radians(self.angle)
        tip = self.pos + pygame.Vector2(-math.sin(rad), -math.cos(rad)) * 20
        bullet_vel = pygame.Vector2(-math.sin(rad), -math.cos(rad)) * BULLET_SPEED
        self.bullets.append(Bullet(tip, bullet_vel))

    def update(self):
        self.pos += self.vel
        self.vel *= SHIP_FRICTION
        self.pos = pygame.Vector2(wrap_position(self.pos))
        if self.cooldown > 0:
            self.cooldown -= 1

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not (0 <= bullet.pos.x <= SCREEN_W and 0 <= bullet.pos.y <= SCREEN_H):
                self.bullets.remove(bullet)

    def draw(self, surf):
        # Draw ship as a triangle
        rad = math.radians(self.angle)
        tip = pygame.Vector2(-math.sin(rad), -math.cos(rad)) * 20
        left = pygame.Vector2(math.sin(rad - math.pi / 2), math.cos(rad - math.pi / 2)) * 15
        right = pygame.Vector2(math.sin(rad + math.pi / 2), math.cos(rad + math.pi / 2)) * 15
        points = [self.pos + tip, self.pos + left, self.pos + right]
        pygame.draw.polygon(surf, (255, 255, 255), points)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surf)


class Bullet:
    def __init__(self, pos, vel):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)

    def update(self):
        self.pos += self.vel

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), (*self.pos, 2, 2))


class Asteroid:
    """Circular asteroid that can split into two smaller ones."""
    def __init__(self, pos=None, size=3, letter=None):
        self.size = size                # 3 = large, 2 = medium, 1 = small
        self.radius = 40 * size
        self.pos = pygame.Vector2(pos if pos else (random.randint(0, SCREEN_W), random.randint(0, SCREEN_H)))
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5) / size
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        self.letter = letter or random.choice(build_frequency_list())
        self.surf = None  # Cached rendered surface

    def update(self):
        self.pos += self.vel
        self.pos = pygame.Vector2(wrap_position(self.pos))

    def draw(self, surf):
        # Cache a surface for performance
        if self.surf is None:
            self.surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.surf, (100, 100, 100), (self.radius, self.radius), self.radius)
            # Render letter
            font = pygame.font.SysFont(None, int(self.radius))
            txt = font.render(self.letter, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=(self.radius, self.radius))
            self.surf.blit(txt, txt_rect)
        surf.blit(self.surf, (self.pos.x - self.radius, self.pos.y - self.radius))

    def collide_with(self, point):
        return self.pos.distance_to(point) <= self.radius

    def split(self):
        """Return list of smaller asteroids after splitting."""
        if self.size == 1:
            return []  # Smallest asteroid cannot split
        new_size = self.size - 1
        return [
            Asteroid(self.pos, new_size, random.choice(build_frequency_list())),
            Asteroid(self.pos, new_size, random.choice(build_frequency_list())),
        ]


class Hangman:
    """Keeps track of letters guessed and draws the partial hangman."""
    def __init__(self, word, max_lives):
        self.word = word.upper()
        self.guessed = set()
        self.wrong_guesses = 0
        self.max_lives = max_lives

    def guess(self, letter):
        letter = letter.upper()
        if letter in self.guessed:
            return False  # already guessed
        self.guessed.add(letter)
        if letter not in self.word:
            self.wrong_guesses += 1
        return True

    def is_solved(self):
        return all(ch in self.guessed for ch in self.word)

    def is_dead(self):
        return self.wrong_guesses >= self.max_lives

    def display(self, surf):
        """Draw the current word state and a simple stick‑figure."""
        # Word state
        font = pygame.font.SysFont(None, 48)
        display_word = " ".join([c if c in self.guessed else "_" for c in self.word])
        txt = font.render(display_word, True, (255, 255, 255))
        surf.blit(txt, (20, SCREEN_H - 60))

        # Simple stick figure (just a line and a circle)
        base_y = SCREEN_H - 120
        pygame.draw.line(surf, (255, 255, 0), (20, base_y), (20, base_y - 80), 4)
        pygame.draw.circle(surf, (255, 255, 0), (20, base_y - 80), 10, 4)
        # You can extend this to add more parts if wrong_guesses increases

# ----- GAME LOOP -------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids‑Spelling")

    ship = Ship()
    asteroids = [Asteroid() for _ in range(5)]
    hangman = Hangman(TARGET_WORD, MAX_LIVES)

    running = True
    while running:
        dt = clock.tick(FPS)
        # ---- INPUT -------------------------------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        ship.handle_input(keys)

        # ---- UPDATE -------------------------------------------------
        ship.update()
        for asteroid in asteroids:
            asteroid.update()

        # Bullet–asteroid collision
        for bullet in ship.bullets[:]:
            for asteroid in asteroids[:]:
                if asteroid.collide_with(bullet.pos):
                    ship.bullets.remove(bullet)
                    # Collect letter
                    hangman.guess(asteroid.letter)
                    # Split or remove
                    asteroids.remove(asteroid)
                    asteroids.extend(asteroid.split())
                    break

        # Ship–asteroid collision
        for asteroid in asteroids:
            if asteroid.collide_with(ship.pos):
                ship.lives -= 1
                hangman.wrong_guesses += 1
                asteroids.remove(asteroid)
                break

        # ---- END CONDITION -----------------------------------------
        if hangman.is_solved():
            print("You solved it! 🎉")
            running = False
        if ship.lives <= 0 or hangman.is_dead():
            print("Game Over.")
            running = False

        # ---- DRAW --------------------------------------------------
        screen.fill((0, 0, 0))

        for asteroid in asteroids:
            asteroid.draw(screen)

        ship.draw(screen)

        hangman.display(screen)

        # If game over, overlay a semi‑transparent box
        if not running:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # 180/255 ~ 70% opaque
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont(None, 64)
            msg = "YOU WON!" if hangman.is_solved() else "GAME OVER"
            txt = font.render(msg, True, (255, 255, 255))
            txt_rect = txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
            screen.blit(txt, txt_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
