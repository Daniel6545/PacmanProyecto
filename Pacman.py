from Config import *
import pygame
from pygame.sprite import Sprite


class pacman(Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = SCREEN_HEIGHT // 2

        self.image = pygame.Surface((tamaño_pacman, tamaño_pacman))
        self.image.fill((255, 255, 0))  # Amarillo

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.velocidad = Pac_Vel

        # DIRECCIONES
        self.direccion_actual = (0, 0)
        self.direccion_objetivo = (0, 0)

    def mover(self, muros):
        # Intentar cambiar direccion actual por la objetivo si no hay colision
        dx, dy = self.direccion_objetivo
        rect_prueba = self.rect.copy()
        rect_prueba.x += dx * self.velocidad
        rect_prueba.y += dy * self.velocidad

        if not any(rect_prueba.colliderect(muro.rect) for muro in muros):
            self.direccion_actual = self.direccion_objetivo

        # Mover en la direccion actual
        dx, dy = self.direccion_actual
        nueva_x = self.x + dx * self.velocidad
        nueva_y = self.y + dy * self.velocidad

        # Comprobar colision horizontal
        rect_x = self.rect.copy()
        rect_x.x = int(nueva_x)
        if not any(rect_x.colliderect(muro.rect) for muro in muros):
            self.x = nueva_x

        # Comprobar colision vertical
        rect_y = self.rect.copy()
        rect_y.y = int(nueva_y)
        if not any(rect_y.colliderect(muro.rect) for muro in muros):
            self.y = nueva_y

        # Teletransporte horizontal (túnel lateral)
        if self.rect.right < 0:
            self.x = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.x = -self.rect.width

        self.rect.topleft = (int(self.x), int(self.y))

    def detener(self):
        self.direccion_actual = (0, 0)
        self.direccion_objetivo = (0, 0)

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)
