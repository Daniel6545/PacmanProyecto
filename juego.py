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
        self.vidas = 3  # vidas PacMan
        self.mostrar_ready = True

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

        if keys[pygame.K_RIGHT]:
            self.pacman.direccion_objetivo = (1, 0)
            self.direccion_actual = (1, 0)
        elif keys[pygame.K_LEFT]:
            self.pacman.direccion_objetivo = (-1, 0)
            self.direccion_actual = (-1, 0)
        elif keys[pygame.K_UP]:
            self.pacman.direccion_objetivo = (0, -1)
            self.direccion_actual = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.pacman.direccion_objetivo = (0, 1)
            self.direccion_actual = (0, 1)

        if self.mostrar_ready and self.direccion_actual != (0, 0):
            self.mostrar_ready = False
            self.pacman.direccion = self.direccion_actual

        if not self.mostrar_ready:
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
            self.vidas -= 1
            print(f"¡Te ha atrapado un fantasma! Vidas restantes: {self.vidas}")
            pygame.time.delay(1500)
            if self.vidas <= 0:
                print("GAME OVER")
                self.running = False
            else:
                self.reiniciar_pacman()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reiniciar_pacman(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                if celda == "P":
                    # Posición centrada en el centro de la celda
                    pac_x = x * self.tile_size + self.tile_size // 2
                    pac_y = y * self.tile_size + self.tile_size // 2

                    self.pacman.x = pac_x - self.pacman.rect.width // 2
                    self.pacman.y = pac_y - self.pacman.rect.height // 2
                    self.pacman.rect.topleft = (self.pacman.x, self.pacman.y)
                    self.pacman.direccion_actual = (0, 0)
                    # Reiniciar movimiento
                    self.pacman.direccion_actual = (0, 0)
                    if hasattr(self.pacman, "detener"):
                        self.pacman.detener()
                    return


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

        # Mostrar Vidas
        texto_vidas = self.fuente.render("", True, WHITE)
        self.ventana.blit(texto_vidas, (SCREEN_WIDTH - 130, 10))

        # Dibujar mini Pac-Man (Vidas)
        sprite_vida = pygame.transform.scale(self.pacman.imagenes[(1, 0)][0],
                                             (20, 20))  # Escalar imagen derecha pequeña

        for i in range(self.vidas):
            x = SCREEN_WIDTH - 60 + i * 20  # separa las imágenes un poco más para que no se monten
            y = 10  # posición vertical
            self.ventana.blit(sprite_vida, (x, y))

        # Dibujar READY! en las XXXXX
        if self.mostrar_ready:
            ready_text = self.fuente.render("R E A D Y !", True, Rojo)

            # Posicionar READY! centrado sobre las XXXXX (fila 18, columnas 11–15 aprox.)
            ready_x = tile_size * 13.5  # Columna del medio de las XXXXX
            ready_y = tile_size * 18.5  # Fila donde están las XXXXX

            text_rect = ready_text.get_rect(center=(ready_x, ready_y))
            self.ventana.blit(ready_text, text_rect)
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
