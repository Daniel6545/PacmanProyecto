from Config import *
import pygame
from pygame.sprite import Sprite


class pacman(Sprite):
    def __init__(self, x=None, y=None):
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = SCREEN_HEIGHT // 2
        self.x = x
        self.y = y
        # CREAR JUGADPR:
        super().__init__()
        self.rect = pygame.Rect(
            self.x - tamaño // 2,
            self.y - tamaño // 2,
            tamaño,
            tamaño
        )

    def mover(self, dx, dy):
        self.x += dx * Pac_Vel
        self.y += dy * Pac_Vel

        # Actualizar rectangulo (pacman)
        self.rect.center = (self.x, self.y)

        # mantener pacman en pantalla:
        if self.x > SCREEN_WIDTH - tamaño // 2:
            self.x = tamaño // 2

        elif self.x < tamaño // 2:
            self.x = SCREEN_WIDTH - tamaño

        elif self.y > SCREEN_HEIGHT - tamaño // 2:
            self.y = tamaño // 2

        elif self.y < tamaño // 2:
            self.y = SCREEN_HEIGHT - tamaño

    def draw(self, ventana):
        pygame.draw.rect(ventana, YELLOW, self.rect)

