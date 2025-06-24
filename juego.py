import pygame
import sys
from Config import *
from Pacman import pacman
from Pared import Muro
from Coin import Coin
from Alberto import alberto
from Oscar import oscar
from Juan import juan
from Puerta import puerta
from Superpoder import Superpoder

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
        self.puertas_group = pygame.sprite.Group()
        self.superpoder_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Calibri", 20)
        self.puntuacion = 0
        self.vidas = 3  # vidas PacMan
        self.mostrar_ready = True
        self.nivel=0

        self.mapa_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.superpoder_activo = False
        self.superpoder_tiempo = 0

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
                    self.moneda = Coin(cx, cy)
                    self.coin_group.add(self.moneda)

                elif celda == "P":
                    pac_x = x * self.tile_size + self.tile_size // 2
                    pac_y = y * self.tile_size + self.tile_size // 2

                    self.pacman = pacman(pac_x, pac_y)
                    self.pacman_group = pygame.sprite.Group(self.pacman)
                elif celda == "A":
                    alberto_x = x * self.tile_size + self.tile_size // 2
                    alberto_y = y * self.tile_size + self.tile_size // 2
                    self.alberto = alberto(self.muro_grupo, alberto_x, alberto_y, self.nivel)
                    self.fantasmas_group.add(self.alberto)
                elif celda == "O":
                    oscar_x = x * self.tile_size + self.tile_size // 2
                    oscar_y = y * self.tile_size + self.tile_size // 2
                    self.oscar = oscar(self.muro_grupo, oscar_x, oscar_y, self.nivel)
                    self.fantasmas_group.add(self.oscar)
                elif celda == "J":
                    juan_x = x * self.tile_size + self.tile_size // 2
                    juan_y = y * self.tile_size + self.tile_size // 2
                    self.juan = juan(self.muro_grupo, juan_x, juan_y, self.nivel)
                    self.fantasmas_group.add(self.juan)
                elif celda =="x":
                    self.puerta = puerta(pos[0], pos[1], self.tile_size)
                    self.puertas_group.add(self.puerta)
                elif celda == "S":
                    cx = x * self.tile_size + self.tile_size // 2
                    cy = y * self.tile_size + self.tile_size // 2
                    self.poder = Superpoder(cx, cy)
                    self.superpoder_group.add(self.poder)
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
            self.pacman.mover(self.muro_grupo, self.puertas_group)
            for fantasma in self.fantasmas_group:
                fantasma.move((self.pacman.x, self.pacman.y), self.puertas_group)



        # Colisiones monedas
        if pygame.sprite.spritecollide(self.pacman, self.coin_group, True):
            self.puntuacion += 10
            if len(self.coin_group) == 0:
                pygame.time.delay(2000)
                self.nivel += 0.05
                self.reiniciar_nivel()

        # Colisión con fantasmas
        fantasmas_colision = pygame.sprite.spritecollide(self.pacman, self.fantasmas_group, False)
        if fantasmas_colision:
            if self.superpoder_activo:
                for fantasma in fantasmas_colision:
                    self.reiniciar_fantasma(fantasma)
            else:
                self.vidas -= 1
                pygame.time.delay(1500)
                if self.vidas <= 0:
                    print("GAME OVER")
                    self.running = False
                else:
                    self.reiniciar_pacman()
                    self.reiniciar_Fantasmas()
        # Superpoder recogido
        if pygame.sprite.spritecollide(self.pacman, self.superpoder_group, True):
            self.superpoder_activo = True
            self.superpoder_tiempo = pygame.time.get_ticks()
            for fantasma in self.fantasmas_group:
                fantasma.activar_miedo()

        if self.superpoder_activo:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.superpoder_tiempo > 7000:
                self.superpoder_activo = False
                for fantasma in self.fantasmas_group:
                    fantasma.desactivar_miedo()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reiniciar_nivel(self):
        # Reiniciar todos los grupos
        self.muro_grupo.empty()
        self.coin_group.empty()
        self.fantasmas_group.empty()
        self.puertas_group.empty()
        self.superpoder_group.empty()
        self.mostrar_ready = True
        self.direccion_actual = (0, 0)
        self.crearmapa()



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

    def reiniciar_Fantasmas(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                cx = x * self.tile_size + self.tile_size // 2
                cy = y * self.tile_size + self.tile_size // 2

                if celda == "A" and hasattr(self, "alberto"):
                    self.alberto.x = cx
                    self.alberto.y = cy
                    self.alberto.rect.topleft = (self.alberto.x, self.alberto.y)
                    self.alberto.direccion_actual = (0, 0)
                if celda == "O" and hasattr(self, "oscar"):
                    self.oscar.x = cx
                    self.oscar.y = cy
                    self.oscar.rect.topleft = (self.oscar.x, self.oscar.y)
                    self.oscar.direccion_actual = (0, 0)
                if celda == "J" and hasattr(self, "juan"):
                    self.juan.x = cx
                    self.juan.y = cy
                    self.juan.rect.topleft = (self.juan.x, self.juan.y)
                    self.juan.direccion_actual = (0, 0)

    def reiniciar_fantasma(self, fantasma):
        fantasma.desactivar_miedo()
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                cx = x * self.tile_size + self.tile_size // 2
                cy = y * self.tile_size + self.tile_size // 2

                if celda == "A" and isinstance(fantasma, alberto):
                    fantasma.x = cx
                    fantasma.y = cy
                elif celda == "O" and isinstance(fantasma, oscar):
                    fantasma.x = cx
                    fantasma.y = cy
                elif celda == "J" and isinstance(fantasma, juan):
                    fantasma.x = cx
                    fantasma.y = cy

                fantasma.rect.topleft = (fantasma.x, fantasma.y)
                fantasma.direccion_actual = (0, 0)

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
        #dibuja Superpoder
        self.superpoder_group.draw(self.ventana)

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
        self.puerta.draw(self.ventana)
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