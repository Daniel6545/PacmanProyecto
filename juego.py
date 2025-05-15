import pygame
import sys

from pygame.examples.sprite_texture import group

from Config import *
from Pacman import pacman
from Pared import Muro

class Juego:
    def __init__(self):
        self.direccion_actual = (0, 0)
        self.ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")

        self.running = True
        self.pacman = pacman()
        self.pacman_group = pygame.sprite.Group(self.pacman)

        self.pared = Muro(50, 200)
        self.muro_grupo = pygame.sprite.Group(self.pared)

        self.clock = pygame.time.Clock()

    def update(self):
        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        if dx != 0:
            self.direccion_actual = (dx, 0)
        elif dy != 0:
            self.direccion_actual = (0, dy)

        self.pacman.mover(*self.direccion_actual)

        collisions = pygame.sprite.groupcollide(self.pacman_group, self.muro_grupo, False, False)
        if collisions:
            self.pacman.mover(-self.direccion_actual[0], -self.direccion_actual[1])
            self.direccion_actual = (0, 0)

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.ventana.fill(BLACK)
        self.pacman.draw(self.ventana)
        self.pared.draw(self.ventana)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.eventos()
            self.draw()
            self.update()
            self.clock.tick(60)


def main():
    try:
        pygame.init()
        juego = Juego()
        juego.run()
    except Exception as e:
        print(f"Error:{e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    main()
