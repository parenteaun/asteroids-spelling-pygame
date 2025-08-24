# assets/hearts.py
import pygame

HEART_SIZE = 14
HEART_COLOR = (220, 20, 60)

def _heart_points(x, y, s):
    # simple pixel heart polygon
    return [
        (x+1*s, y+0*s), (x+3*s, y+0*s), (x+4*s, y+1*s), (x+5*s, y+0*s),
        (x+7*s, y+0*s), (x+8*s, y+1*s), (x+8*s, y+3*s), (x+7*s, y+4*s),
        (x+4*s, y+7*s), (x+1*s, y+4*s), (x+0*s, y+3*s), (x+0*s, y+1*s)
    ]

class Hearts:
    def __init__(self, lives, pos):
        self.lives = lives
        self.pos = pos  # (x, y)

    def set_lives(self, n):
        self.lives = max(0, int(n))

    def draw(self, surf):
        x0, y0 = self.pos
        for i in range(self.lives):
            pts = _heart_points(x0 + i*(HEART_SIZE+8), y0, 1)
            pygame.draw.polygon(surf, HEART_COLOR, pts)
