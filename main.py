import pygame as pg
from random import randint, uniform, choice
from math import ceil


class Planet():
    def __init__(self, m: float, p: pg.Vector2, v: pg.Vector2, color):
        self.color = color
        self.m: float = m
        self.p: pg.Vector2 = p
        self.a: pg.Vector2 = pg.Vector2(0, 0)
        self.v: pg.Vector2 = v
        self.r: float = m/500

    def update(self, dt):
        p1 = self.p
        self.v += self.a * dt
        self.p += self.v * dt
        self.a = pg.Vector2(0, 0)
        #self.p.x %= 1000
        #self.p.y %= 1000
        pg.draw.line(trail_layer, self.color, p1, self.p, )#width=int(ceil(self.v.magnitude()**.5)))

    def apply_force_from_vector(self, force: pg.Vector2) -> None:
        self.a += force / self.m

    def apply_force_from_polar(self, magnitude: float, direction: float) -> None:
        pass

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

WIDTH=2000
HEIGHT=2000


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
PURPLE = (255, 0, 255)
BROWN = (255, 255, 0)
ALL_COLORS = [RED, BLUE, GREEN, WHITE, PURPLE, BROWN]

def random_planets(num):
    return [Planet(randint(5000,10000), pg.Vector2(randint(-.5*SCREEN_WIDTH,.5*SCREEN_WIDTH)+WIDTH/2, randint(-.5*SCREEN_HEIGHT,.5*SCREEN_HEIGHT)+HEIGHT/2), pg.Vector2(uniform(-8,8),uniform(-8,8)), choice(ALL_COLORS)) for _ in range(num)]

planets = random_planets(3)


pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
world_surf = pg.Surface((WIDTH,HEIGHT))
pg.display.set_caption("<Your game>")
clock = pg.time.Clock()  # For syncing the FPS
FPS = 300

camera_mode = "normal"
track_planet = 0
trail_layer = pg.Surface((WIDTH,HEIGHT))
trail_layer.fill(BLACK)

dragging = False
mouse_prev = pg.Vector2(0,0)
cam_offset = pg.Vector2(world_surf.get_rect().center)


# Game loop
running = True
while running:
    print(cam_offset)
    print(planets[0].p)

    # 1 Process input/events
    # will make the loop run at the same speed all the time
    dt = clock.tick(FPS)
    # gets all the events which have occured till now and keeps tab of them.
    for event in pg.event.get():
        # listening for the the X button at the top
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                trail_layer.fill(BLACK)
                cam_offset = pg.Vector2(0,0)
                planets = random_planets(3)
            if event.key == pg.K_LEFT:
                track_planet -= 1 
                track_planet %= len(planets)
            if event.key == pg.K_RIGHT:
                track_planet += 1 
                track_planet %= len(planets)
            if event.key == pg.K_UP:
                camera_mode = "average"
            if event.key == pg.K_DOWN:
                camera_mode = "track"

    if pg.mouse.get_pressed()[0]:
        dragging = True
        cam_offset = pg.Vector2(pg.mouse.get_pos()) - mouse_prev
    elif dragging:
        dragging = False
    else:
        mouse_prev = pg.Vector2(pg.mouse.get_pos()) - cam_offset



    # 3 Draw/render
    if camera_mode == "average":
        p_sum = pg.Vector2(0,0)
        for planet in planets:
            p_sum += planet.p
        p_avg = p_sum / len(planets) + pg.Vector2(500,500)
    elif camera_mode == "track":
        p_avg = planets[track_planet].p + pg.Vector2(500,500)
    else:
        p_avg = pg.Vector2(0,0)
    
    world_surf.fill(BLACK)
    world_surf.blit(trail_layer,(0,0))

    for planet in planets:
        for planet2 in planets:
            if planet == planet2:
                continue
            distance = (planet.p - planet2.p).magnitude_squared()
            if distance < planet.r**2:
                trail_layer.fill(BLACK)
                planets = random_planets(3)
                break
            force = 6 * planet.m * planet2.m / distance
            force_vector = (planet2.p - planet.p).normalize() * force
            planet.apply_force_from_vector(force_vector)
    
    for planet in planets:
        planet.update(dt/40)
        pg.draw.circle(world_surf, planet.color, planet.p, planet.r)

    screen.fill(BLACK)
    screen.blit(world_surf, cam_offset)

    pg.display.flip()

pg.quit()
