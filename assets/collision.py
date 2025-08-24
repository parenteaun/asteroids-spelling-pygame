# assets/collision.py
import pygame
from assets.asteroids import Asteroid

def bullets_vs_asteroids(ship, asteroids):
    """Handle bullet collisions. Returns (collected_letters, new_asteroids)."""
    collected = []
    new_asts = []
    remaining_asteroids = []
    for ast in asteroids:
        hit = False
        for b in list(ship.bullets):
            if ast.collide_with_point(b.pos):
                ship.bullets.remove(b)
                ast.hp -= 1
                if ast.hp <= 0:
                    if ast.size == 1:
                        collected.append(ast.letter)
                    else:
                        new_asts.extend(ast.split())
                hit = True
                break
        if not hit or (hit and (ast.hp > 0 and ast.size >= 1)):
            remaining_asteroids.append(ast)
    remaining_asteroids.extend(new_asts)
    return collected, remaining_asteroids

def ship_vs_asteroids(ship, asteroids):
    """Return lives_delta and asteroids (no removal on contact)."""
    lives_delta = 0
    for ast in asteroids:
        if ast.collide_with_point(ship.pos):
            lives_delta -= 1
    return lives_delta
