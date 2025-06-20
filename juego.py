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

        self.muro_grupo = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.fantasmas_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Calibri", 20)
        self.puntuacion = 0

        self.direccion_actual = (0, 0)
        self.mapa_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.crearmapa()
    def crearmapa(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                pos = (x * self.tile_size, y * self.tile_size)

                if celda in self.colores_paredes:
                    muro = Muro(pos[0], pos[1])
                    muro.image.fill(self.colores_paredes[celda])  # Pinta el muro con el color correcto
                    self.muro_grupo.add(muro)

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
                elif celda == "F":
                    blinky_x = x * self.tile_size + self.tile_size // 2
                    blinky_y = y * self.tile_size + self.tile_size // 2
                    self.blinky = Blinky(self.muro_grupo, blinky_x, blinky_y)
                    self.fantasmas_group.add(self.blinky)
    def update(self):
        keys = pygame.key.get_pressed()

        # Cambiar solo direccion objetivo según tecla
        if keys[pygame.K_RIGHT]:
            self.pacman.direccion_objetivo = (1, 0)
        elif keys[pygame.K_LEFT]:
            self.pacman.direccion_objetivo = (-1, 0)
        elif keys[pygame.K_UP]:
            self.pacman.direccion_objetivo = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.pacman.direccion_objetivo = (0, 1)

        # Mover Pacman pasando grupo de muros para colision
        self.pacman.mover(self.muro_grupo)

        # Mover fantasmas
        for fantasma in self.fantasmas_group:
            fantasma.move((self.pacman.x, self.pacman.y))

        # Colisiones monedas
        if pygame.sprite.spritecollide(self.pacman, self.coin_group, True):
            self.puntuacion += 10
            print(f"Puntuación: {self.puntuacion}")

        # Colisión con fantasmas
        if pygame.sprite.spritecollide(self.pacman, self.fantasmas_group, False):
            print("¡Has sido atrapado por el fantasma!")

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False



    def draw(self):
        self.ventana.blit(self.mapa_surface, (0, 0))

        # Dibujar monedas
        self.coin_group.draw(self.ventana)

        # Dibujar fantasmas
        for fantasma in self.fantasmas_group:
            fantasma.draw(self.ventana)
        #Dibujar muros
        self.muro_grupo.draw(self.ventana)

        # Dibujar Pac-Man
        self.pacman.draw(self.ventana)

        # Mostrar puntuación
        texto = self.fuente.render(f"SCORE: {self.puntuacion}", True, WHITE)
        self.ventana.blit(texto, (10, 10))

        pygame.display.flip()

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
