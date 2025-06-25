import pygame
from pygame.sprite import Sprite

class tunel(Sprite):
    def __init__(self, x, y, tamaño):
        super().__init__()
        self.rect = pygame.Rect(x, y, tamaño, tamaño)

    def contiene(self, objeto_rect):
        return self.rect.colliderect(objeto_rect)