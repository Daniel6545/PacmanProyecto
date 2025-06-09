import pygame
import sys

from Config import *
from Pacman import pacman
from Pared import Muro
from Coin import Coin
from Blinky import Blinky


class Juego:
    def __init__(self):
        self.direccion_actual = (0, 0)
        self.ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.datos = datos
        self.tile_size = tile_size
        self.colores_paredes = colores_paredes

        self.running = True
        #self.pacman = pacman()
        #self.pacman_group = pygame.sprite.Group(self.pacman)

        self.blinky = Blinky()
        self.fantasmas_group = pygame.sprite.Group(self.blinky)

        self.pared = Muro(50, 200)
        self.muro_grupo = pygame.sprite.Group(self.pared)

        self.clock = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Calibri", 20)  #fuente SCORE
        self.puntuacion = 0   #guardará los puntos que Pac-Man obtiene al comer monedas
        self.coin_group = pygame.sprite.Group() #agrupa esa moneda dentro de un Sprite

        self.mapa_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.crearmapa()  # Dibuja el mapa sobre esa surface




    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if dx != 0:
            self.direccion_actual = (dx, 0)
        elif dy != 0:
            self.direccion_actual = (0, dy)

        self.pacman.mover(*self.direccion_actual)
        #mover fant
        for fantasma in self.fantasmas_group:
            fantasma.move((self.pacman.x, self.pacman.y))
    #colision muros (Pacman)
        if pygame.sprite.groupcollide(self.pacman_group, self.muro_grupo, False, False):
            self.pacman.mover(-self.direccion_actual[0], -self.direccion_actual[1])
            self.direccion_actual = (0, 0)
    #Colision moneda
        if pygame.sprite.spritecollide(self.pacman, self.coin_group, True):
            self.puntuacion += 10
            print(f"Puntuación: {self.puntuacion}")
    #colision Fantasma:
        if pygame.sprite.spritecollide(self.pacman, self.fantasmas_group, False):
            print("¡Has sido atrapado por el fantasma!")

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def crearmapa(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                pos = (x * self.tile_size, y * self.tile_size)

                if celda in self.colores_paredes:
                    pygame.draw.rect(self.mapa_surface, self.colores_paredes[celda],
                                     (*pos, self.tile_size, self.tile_size))
                elif celda == "0":
                    cx = x * self.tile_size + self.tile_size // 2
                    cy = y * self.tile_size + self.tile_size // 2
                    moneda = Coin(cx, cy)
                    self.coin_group.add(moneda)
                elif celda == "S":
                    pygame.draw.circle(self.mapa_surface, Dorado,
                                       (pos[0] + self.tile_size // 2, pos[1] + self.tile_size // 2), 5)
                elif celda == "P":
                    pac_x = x * self.tile_size + self.tile_size // 2
                    pac_y = y * self.tile_size + self.tile_size // 2
                    self.pacman = pacman(pac_x, pac_y)
                    self.pacman_group = pygame.sprite.Group(self.pacman)


    def draw(self):
        # Dibujar el mapa una vez ya creado
        self.ventana.blit(self.mapa_surface, (0, 0))

        # Dibujar monedas
        self.coin_group.draw(self.ventana)

        # Dibujar fantasmas
        for fantasma in self.fantasmas_group:
            fantasma.draw(self.ventana)

        # Dibujar Pac-Man
        self.pacman.draw(self.ventana)

        # Mostrar puntuación
        texto = self.fuente.render(f"SCORE: {self.puntuacion}", True, WHITE)
        self.ventana.blit(texto, (10, 10))

        pygame.display.flip()  # Esta función se encarga de actualizar la pantalla
    def run(self):
        while self.running:
            self.eventos()
            self.update()
            self.draw()
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
