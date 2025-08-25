# game.py
import pygame
from pygame.locals import *
import random

from assets.config import SCREEN_W, SCREEN_H, wrap_position
from assets.ship import Ship
from assets.asteroids import Asteroid
from assets.hearts import Hearts
from assets.collision import bullets_vs_asteroids, ship_vs_asteroids
from assets.sounds.sound_manager import SoundManager
from letterfrequency import build_frequency_list

FPS = 60

def make_field_letters(n=6):
    # letters the asteroids will carry
    freq = build_frequency_list()
    return [random.choice(freq) for _ in range(n)]

def spawn_asteroids(field_letters, count=6):
    asteroids = []
    for _ in range(count):
        edge = random.choice(['top','bottom','left','right'])
        if edge == 'top':
            pos = (random.randrange(SCREEN_W), 0)
        elif edge == 'bottom':
            pos = (random.randrange(SCREEN_W), SCREEN_H-1)
        elif edge == 'left':
            pos = (0, random.randrange(SCREEN_H))
        else:
            pos = (SCREEN_W-1, random.randrange(SCREEN_H))
        letter = random.choice(field_letters)
        asteroids.append(Asteroid(pos, size=random.choice([2,3]), letter=letter))
    return asteroids

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Asteroids Spelling")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    bigfont = pygame.font.SysFont(None, 48)

    # Initialize sound manager
    sound_manager = SoundManager()

    ship = Ship((SCREEN_W/2, SCREEN_H/2), sound_manager=sound_manager)
    hearts = Hearts(ship, (10, SCREEN_H-26))

    # Start background music
    sound_manager.play_music('background')

    target_word = "PYGAME"
    collected = ""
    field_letters = make_field_letters(8)
    asteroids = spawn_asteroids(field_letters, 6)

    game_over = False
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sound_manager.cleanup()
                return
            if event.type == KEYDOWN and (game_over or win):
                # restart
                ship = Ship((SCREEN_W/2, SCREEN_H/2), sound_manager=sound_manager)
                hearts = Hearts(ship, (10, SCREEN_H-26))
                collected = ""
                asteroids = spawn_asteroids(field_letters, 6)
                game_over = False
                win = False

        keys = pygame.key.get_pressed()
        if not (game_over or win):
            ship.handle_input(keys)
            ship.update()

            # collisions
            letters, asteroids = bullets_vs_asteroids(ship, asteroids)
            for L in letters:
                collected += L
                sound_manager.play_sound('asteroid_hit')  # Play hit sound
                if all(ch in collected for ch in target_word):
                    sound_manager.play_sound('victory')  # Play victory sound
                    win = True

            # ship hits
            lives_delta = ship_vs_asteroids(ship, asteroids)
            if lives_delta < 0:
                ship.lives += lives_delta
                sound_manager.play_sound('ship_hit')  # Play ship hit sound
                if ship.lives <= 0:
                    sound_manager.play_sound('game_over')  # Play game over sound
                    game_over = True

            # update asteroids
            for a in asteroids:
                a.update()

            # respawn a few if needed
            while len(asteroids) < 6 and not (game_over or win):
                asteroids.extend(spawn_asteroids(field_letters, 1))

        # draw
        screen.fill((0,0,0))

        for a in asteroids:
            a.draw(screen, font)

        ship.draw(screen)
        hearts.draw(screen)

        # HUD
        hud = font.render(f"Target: {target_word}  Collected: {''.join(sorted(collected))}", True, (200,200,200))
        screen.blit(hud, (10,10))

        if game_over or win:
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            txt = bigfont.render("YOU WIN!" if win else "GAME OVER", True, (255,255,0) if win else (255,255,255))
            rect = txt.get_rect(center=(SCREEN_W/2, SCREEN_H/2 - 20))
            overlay.blit(txt, rect)
            sub = font.render("Press any key to restart", True, (200,200,200))
            srect = sub.get_rect(center=(SCREEN_W/2, SCREEN_H/2 + 20))
            overlay.blit(sub, srect)
            screen.blit(overlay, (0,0))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
