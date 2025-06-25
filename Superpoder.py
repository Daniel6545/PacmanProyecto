import pygame
from pygame.sprite import Sprite
from Config import *

class Superpoder(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)
        self.radio = tamaño // 4
        self.centro = (tamaño // 2, tamaño // 2)
        pygame.draw.circle(self.original_image, Dorado, self.centro, self.radio)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))

        self.visible = True  # estado de visibilidad
        self.timer = 0       # contador de tiempo

    def update(self):
        self.timer += 1
        # Parpadeo 10 frames
        if self.timer % 10 == 0:
            self.visible = not self.visible

    def draw(self, ventana):
        if self.visible:
            ventana.blit(self.image, self.rect)
