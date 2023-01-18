import pygame as pg
from random import randint, uniform


class Planet():
    def __init__(self, m: float, p: pg.Vector2, v: pg.Vector2):
        self.m: float = m
        self.p: pg.Vector2 = p
        self.a: pg.Vector2 = pg.Vector2(0, 0)
        self.v: pg.Vector2 = v
        self.r: float = m/500

    def update(self, dt):
        self.v += self.a * dt
        self.p += self.v * dt
        self.a = pg.Vector2(0, 0)

    def apply_force_from_vector(self, force: pg.Vector2) -> None:
        self.a += force / self.m

    def apply_force_from_polar(self, magnitude: float, direction: float) -> None:
        pass

planets = [Planet(randint(5000,10000), pg.Vector2(randint(0,1000), randint(0,1000)), pg.Vector2(uniform(-4,4),uniform(-4,4))) for _ in range(3)]

BLACK = (0, 0, 0)
RED = (255, 0, 0)

pg.init()
screen = pg.display.set_mode((1000, 1000))
pg.display.set_caption("<Your game>")
clock = pg.time.Clock()  # For syncing the FPS
FPS = 100

camera_mode = "track"
track_planet = 0

# Game loop
running = True
while running:

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
                planets = [Planet(randint(5000,10000), pg.Vector2(randint(0,1000), randint(0,1000)), pg.Vector2(uniform(-4,4),uniform(-4,4))) for _ in range(3)]
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

    # 3 Draw/render
    screen.fill(BLACK)
    if camera_mode == "average":
        p_sum = pg.Vector2(0,0)
        for planet in planets:
            p_sum += planet.p
        p_avg = p_sum / len(planets) + pg.Vector2(500,500)
    elif camera_mode == "track":
        p_avg = planets[track_planet].p + pg.Vector2(500,500)

    for planet in planets:
        for planet2 in planets:
            if planet == planet2:
                continue
            distance = (planet.p - planet2.p).magnitude_squared()
            force = planet.m * planet2.m / distance
            force_vector = (planet2.p - planet.p).normalize() * force
            planet.apply_force_from_vector(force_vector)
    
    for planet in planets:
        planet.update(dt/20)
        pg.draw.circle(screen, RED, p_avg-planet.p, planet.r)


    pg.display.flip()

pg.quit()
