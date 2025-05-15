import pygame
import sys

from Config import *
from Pacman import pacman
from Pared import Muro
from Coin import Coin

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
        self.fuente = pygame.font.SysFont("Calibri", 20)  #fuente SCORE
        self.puntuacion = 0   #guardará los puntos que Pac-Man obtiene al comer monedas
        self.coin = Coin(400, 100)   #crea una moneda aleatoria en el mapa
        self.coin_group = pygame.sprite.Group(self.coin) #agrupa esa moneda dentro de un Sprite
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

    #Colision moneda


        if pygame.sprite.spritecollide(self.pacman, self.coin_group, True):
            self.puntuacion += 10
            print(f"Puntuación: {self.puntuacion}")

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.ventana.fill(BLACK)
        self.pacman.draw(self.ventana)
        self.pared.draw(self.ventana)


        self.coin_group.draw(self.ventana)        #dibuja moneda en ventana
        # Mostrar puntuación
        texto = self.fuente.render(f"SCORE: {self.puntuacion}", True, WHITE)
        self.ventana.blit(texto, (10, 10))

        pygame.display.flip()   #Esta función se encarga de actualizar la pantalla

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
