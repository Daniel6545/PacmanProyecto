from pygame.sprite import Sprite
import pygame
from Config import *

class Coin(Sprite):
    def __init__(self, x, y):  # Añadimos los parámetros x y y
        super().__init__()
        self.image = pygame.Surface((tamaño // 2, tamaño // 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (tamaño // 6, tamaño // 6), tamaño // 6)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Establecemos la posición de la moneda

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)

