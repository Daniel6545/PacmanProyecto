import pygame
import math
from pygame.sprite import Sprite
from Config import *

class alberto(Sprite):
    def __init__(self, muros_grupo, x_inicial, y_inicial):
        super().__init__()
        self.x = x_inicial
        self.y = y_inicial
        self.direction = 0
        self.color = Rojo
        self.speed = Alberto_speed
        self.scatter_target = scatter_targetA
        self.mode = "chase"
        self.directions = directions
        self.muros_grupo = muros_grupo
        self.rect = pygame.Rect(
            self.x - tamaño // 2,
            self.y - tamaño // 2,
            tamaño,
            tamaño
        )
        self.jaula_limite_y = self.y - 2 * tamaño
        self.mode_timer = 0
        self.mode_duration = {
            "chase": 20000,
            "scatter": 7000
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
        self.update_mode()
        self.target = pacman_pos if self.mode == "chase" else self.scatter_target
        direction_vectors = {
            0: (1, 0),  # derecha
            1: (-1, 0),  # izquierda
            2: (0, -1),  # arriba
            3: (0, 1)  # abajo
        }

        self.actualizar_turns(self.muros_grupo)

        posibles_dirs = [d for d in range(4) if self.turns[d]]

        if posibles_dirs:
            distancias = []
            direccion_opuesta = {
                0: 1,
                1: 0,
                2: 3,
                3: 2
            }

            for d in posibles_dirs:
                # Evitar girar 180º a menos que sea la única opción
                if d == direccion_opuesta[self.direction] and len(posibles_dirs) > 1:
                    continue
                dx, dy = direction_vectors[d]
                nueva_x = self.x + dx * self.speed
                nueva_y = self.y + dy * self.speed
                distancia = math.hypot(self.target[0] - nueva_x, self.target[1] - nueva_y)
                distancias.append((distancia, d))

            if distancias:
                distancias.sort(key=lambda x: x[0])
                self.direction = distancias[0][1]
        # Mover en la dirección elegida
        if self.turns[self.direction]:
            dx, dy = direction_vectors[self.direction]
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.center = (self.x, self.y)
        return self.x, self.y, self.direction

    def actualizar_turns(self, muros_group):
        self.rect.center = (self.x, self.y)
        # Chequear colisión probando mover Fantasma un paso en cada dirección
        self.turns = [False, False, False, False]
        step = self.speed  # o un valor pequeño

        # derecha
        self.rect.x += step
        self.turns[0] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.x -= step

        # izquierda
        self.rect.x -= step
        self.turns[1] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.x += step

        # arriba
        self.rect.y -= step
        self.turns[2] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.y += step

        # abajo
        self.rect.y += step
        self.turns[3] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.y -= step

    def draw(self, screen):
        """Dibuja al fantasma en la pantalla."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 7)