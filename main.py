import pygame as pg
from random import randint, uniform, choice


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
        pg.draw.line(trail_layer, self.color, p1, self.p)

    def apply_force_from_vector(self, force: pg.Vector2) -> None:
        self.a += force / self.m

    def apply_force_from_polar(self, magnitude: float, direction: float) -> None:
        pass


BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
PURPLE = (255, 0, 255)
BROWN = (255, 255, 0)
ALL_COLORS = [RED, BLUE, GREEN, WHITE, PURPLE, BROWN]

planets = [Planet(randint(5000,10000), pg.Vector2(randint(0,1000), randint(0,1000)), pg.Vector2(uniform(-4,4),uniform(-4,4)), choice(ALL_COLORS)) for _ in range(3)]



pg.init()
screen = pg.display.set_mode((1000, 1000))
pg.display.set_caption("<Your game>")
clock = pg.time.Clock()  # For syncing the FPS
FPS = 300

camera_mode = "normal"
track_planet = 0
trail_layer = pg.Surface((1000,1000))
trail_layer.fill(BLACK)

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
                trail_layer.fill(BLACK)
                planets = [Planet(randint(5000,10000), pg.Vector2(randint(0,1000), randint(0,1000)), pg.Vector2(uniform(-8,8),uniform(-8,8)), choice(ALL_COLORS)) for _ in range(3)]
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
    if camera_mode == "average":
        p_sum = pg.Vector2(0,0)
        for planet in planets:
            p_sum += planet.p
        p_avg = p_sum / len(planets) + pg.Vector2(500,500)
    elif camera_mode == "track":
        p_avg = planets[track_planet].p + pg.Vector2(500,500)
    else:
        p_avg = pg.Vector2(0,0)
    
    screen.fill(BLACK)
    screen.blit(trail_layer,(0,0))

    for planet in planets:
        for planet2 in planets:
            if planet == planet2:
                continue
            distance = (planet.p - planet2.p).magnitude_squared()
            if distance < planet.r**2 and False:
                trail_layer.fill(BLACK)
                planets = [Planet(randint(5000,10000), pg.Vector2(randint(0,1000), randint(0,1000)), pg.Vector2(uniform(-8,8),uniform(-8,8))) for _ in range(4)]
                break
            force = 6 * planet.m * planet2.m / distance
            force_vector = (planet2.p - planet.p).normalize() * force
            planet.apply_force_from_vector(force_vector)
    
    for planet in planets:
        planet.update(dt/40)
        pg.draw.circle(screen, planet.color, planet.p, planet.r)


    pg.display.flip()

pg.quit()
