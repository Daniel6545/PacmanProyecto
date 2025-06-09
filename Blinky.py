import pygame
import math
from pygame.sprite import Sprite
from Config import *

class Blinky(Sprite):
    def __init__(self):
        super().__init__()
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT // 2

        # Configuración inicial
        self.color = Rojo
        self.speed = blinky_speed  # Usamos la velocidad de Config.py
        self.scatter_target = scatter_target
        self.mode = "chase"  # Modos posibles: chase/scatter/frightened/eaten
        self.directions = directions  # Usamos las direcciones de Config.py

        # Crear rectángulo para colisiones
        self.rect = pygame.Rect(
            self.x - tamaño // 2,
            self.y - tamaño // 2,
            tamaño,
            tamaño
        )

        # Temporizador para cambio de modos
        self.mode_timer = 0
        self.mode_duration = {
            "chase": 20000,  # 20 segundos en modo persecución
            "scatter": 7000  # 7 segundos en modo dispersión
        }

    def distance(self, pos1, pos2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def update_mode(self):
        """Alterna entre modos chase y scatter basado en temporizador."""
        current_time = pygame.time.get_ticks()

        if self.mode == "chase" and current_time - self.mode_timer >= self.mode_duration["chase"]:
            self.mode = "scatter"
            self.mode_timer = current_time
        elif self.mode == "scatter" and current_time - self.mode_timer >= self.mode_duration["scatter"]:
            self.mode = "chase"
            self.mode_timer = current_time

    def move(self, pacman_pos):
        """Mueve al fantasma según su modo actual."""
        self.update_mode()

        # Determina el objetivo según el modo
        target_pos = pacman_pos if self.mode == "chase" else self.scatter_target

        best_dir = None
        min_dist = float('inf')

        # Evalúa cada dirección posible
        for dx, dy in self.directions:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            dist = self.distance((new_x, new_y), target_pos)

            if dist < min_dist:
                min_dist = dist
                best_dir = (dx, dy)

        # Aplica el movimiento
        if best_dir:
            self.x += best_dir[0] * self.speed
            self.y += best_dir[1] * self.speed
            self.rect.center = (self.x, self.y)

    def draw(self, screen):
        """Dibuja al fantasma en la pantalla."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), tamaño // 2)