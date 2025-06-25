from pygame.sprite import Sprite
import pygame
from Config import *

class superpoder(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        pygame.draw.circle(self.image, Dorado, (tamaño // 2, tamaño // 2), 6)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)

