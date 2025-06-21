import pygame
from pygame.sprite import Sprite

class puerta(Sprite):
    def __init__(self, x, y,tamaño):
        super().__init__()
        self.rect = pygame.Rect(x, y, tamaño, tamaño)
        self.direccion_salida = (0,-1)

    def permite_paso(self, direccion_movimiento):
        """
        Permite paso solo si el movimiento es en la dirección de salida.
        Fantasmas pueden salir, pero no entrar.
        """
        return direccion_movimiento == self.direccion_salida

    def draw(self, screen):
        # Opcional: dibuja la puerta como un rectángulo semi-transparente para debug
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((255, 0, 0, 100))  # rojo semi-transparente
        screen.blit(s, (self.rect.x, self.rect.y))