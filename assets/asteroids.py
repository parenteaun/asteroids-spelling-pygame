# assets/asteroids.py
import pygame, random, math
from assets.config import wrap_position, SCREEN_W, SCREEN_H

SIZE_HP = {3: 4, 2: 3, 1: 2}
SIZE_RADIUS = {3: 40, 2: 25, 1: 15}
SIZE_COLOR = {3: (120,120,120), 2: (170,170,170), 1: (220,220,220)}

class Asteroid:
    def __init__(self, pos, size=3, letter=None):
        self.pos = pygame.Vector2(pos)
        ang = random.uniform(0, 360)
        speed = random.uniform(1.0, 3.0)
        self.vel = pygame.Vector2(speed, 0).rotate(ang)
        self.size = size
        self.hp = SIZE_HP[self.size]
        self.letter = letter or chr(random.randint(65, 90))

    @property
    def radius(self):
        return SIZE_RADIUS[self.size]

    def update(self):
        self.pos += self.vel
        self.pos.xy = wrap_position(self.pos)

    def draw(self, surf, font=None):
        pygame.draw.circle(surf, SIZE_COLOR[self.size], (int(self.pos.x), int(self.pos.y)), self.radius, 2)
        if font:
            txt = font.render(self.letter, True, (255,255,0))
            rect = txt.get_rect(center=(self.pos.x, self.pos.y))
            surf.blit(txt, rect)

    def collide_with_point(self, p):
        return self.pos.distance_to(p) <= self.radius

    def split(self):
        """Return list of child asteroids if any (for size > 1)."""
        if self.size <= 1:
            return []
        children = []
        for _ in range(2):
            child = Asteroid(self.pos, self.size-1, self.letter)
            child.vel = self.vel.rotate(random.uniform(-35, 35)) * 1.2
            children.append(child)
        return children
