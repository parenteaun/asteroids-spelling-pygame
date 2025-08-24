# assets/config.py
SCREEN_W, SCREEN_H = 800, 600

def wrap_position(pos):
    """Keeps a point inside the screen (wrap-around)."""
    return (pos[0] % SCREEN_W, pos[1] % SCREEN_H)
