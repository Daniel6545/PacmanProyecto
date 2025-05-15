from pygame.sprite import Sprite
import pygame
from Config import *

class Muro(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((tamaño, tamaño))
        self.image.fill(WHITE)  # Para que se vea el muro, llenamos la superficie con blanco
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)