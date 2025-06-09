import pygame
from Config import *

class Mapa:
    def __init__(self):
        self.datos = [list(fila) for fila in datos]  # Convierte cada fila a una lista de caracteres
        self.tile_size = tile_size
        self.ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Colores
        self.colores_paredes = {
            '1': (0, 0, 255),  # Azul
            '2': (255, 0, 0),  # Rojo
            '3': (0, 255, 0),  # Verde
            '4': (255, 165, 0),  # Naranja
        }

    def crearmapa(self):
        # Mostrar puntuación
        self.ventana.fill(BLACK)
        texto = self.fuente.render(f"SCORE: {self.puntuacion}", True, WHITE)
        self.ventana.blit(texto, (10, 10))

        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                pos = (x * self.tile_size, y * self.tile_size)

                if celda in self.colores_paredes:
                    pygame.draw.rect(self.ventana, self.colores_paredes[celda], (*pos, self.tile_size, self.tile_size))
                elif celda == "0":
                    cx = x * self.tile_size + self.tile_size // 2
                    cy = y * self.tile_size + self.tile_size // 2
                    moneda = Coin(cx, cy)
                    self.coin_group.add(moneda)
                elif celda == "S":
                    pygame.draw.circle(self.ventana, (255, 255, 0),
                                       (pos[0] + self.tile_size // 2, pos[1] + self.tile_size // 2), 6)
                elif celda == "F":
                    for fantasma in self.fantasmas_group:
                        fantasma.draw(self.ventana)
                elif celda == "P":
                    self.pacman.draw(self.ventana)

        pygame.display.flip()  # Esta función se encarga de actualizar la pantalla

    def get_celda(self, x, y):
        if 0 <= y < self.alto and 0 <= x < self.ancho:
            return self.datos[y][x]
        return None  # Fuera del mapa

    def set_celda(self, x, y, valor):
        if 0 <= y < self.alto and 0 <= x < self.ancho:
            self.datos[y][x] = valor

    def buscar_posicion(self, simbolo):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                if celda == simbolo:
                    return x, y
        return None
