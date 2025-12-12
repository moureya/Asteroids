import pygame
import sys

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_event

def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots)
    player = Player(x, y)
    asteroidfield = AsteroidField()
    
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        dt = clock.tick(60) / 1000

        screen.fill("black")
        
        updatable.update(dt)
        for sprite in drawable:
            sprite.draw(screen)
        shots.update(dt)
        for shot in shots:
            shot.draw(screen)
        for asteroid in asteroids:
            for shot in shots:
                if Shot.collides_with(asteroid, shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
        for asteroid in asteroids:
            if Asteroid.collides_with(asteroid, player):
                log_event("player_hit")
                print(f"Game over!")
                sys.exit()

        pygame.display.flip()

        

if __name__ == "__main__":
    main()
