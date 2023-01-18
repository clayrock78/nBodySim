import pygame as pg

class Planet():
    def __init__(self, m:float, p:pg.Vector2):
        self.m:float = m
        self.p:pg.Vector2 = p
        self.a:pg.Vector2 = pg.Vector2(0,0)
        self.v:pg.Vector2 = pg.Vector2(0,0)
        self.r:float = 100

    def update(self,dt):
        self.v += self.a * dt
        self.p += self.v * dt
        self.a = pg.Vector2(0,0)

    def apply_force_from_vector(self, force:pg.Vector2) -> None:
        self.a += force / self.m
        

    def apply_force_from_polar(self, magnitude:float, direction:float) -> None:
        pass

planets = [Planet(1000, pg.Vector2(500,500))]

BLACK = (0,0,0)
RED = (255,0,0)

pg.init()
screen = pg.display.set_mode((1000, 1000))
pg.display.set_caption("<Your game>")
clock = pg.time.Clock()     ## For syncing the FPS
FPS = 100

## Game loop
running = True
while running:

    #1 Process input/events
    dt = clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pg.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                planets[0].apply_force_from_vector(pg.Vector2(10,0))

    #3 Draw/render
    screen.fill(BLACK)

    for planet in planets:
        planet.update(dt)
        pg.draw.circle(screen, RED, planet.p, planet.r)


    pg.display.flip()       

pg.quit()