import pygame
from pygame.sprite import Sprite
from Config import *

class Superpoder(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        self.radio = tamaño // 4
        self.centro = (tamaño // 2, tamaño // 2)
        pygame.draw.circle(self.image, Dorado, self.centro, self.radio)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)
