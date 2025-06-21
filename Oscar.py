import pygame
import math
from pygame.sprite import Sprite
from Config import *

class oscar(Sprite):
    def __init__(self, muros_grupo, x_inicial, y_inicial):
        super().__init__()
        self.x = x_inicial
        self.y = y_inicial
        self.direction = 0
        self.color = WHITE
        self.speed = Oscar_speed
        self.scatter_target = scatter_targetO
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
            "chase": 10000,
            "scatter": 15000
        }
        self.en_salida = True
        self.salida_ruta = [
            (self.x, self.y - tamaño),  # subir una celda
            (self.x, self.y - 2 * tamaño)  # subir otra celda
        ]
        self.salida_paso = 0
        self.salida_target = self.salida_ruta[0]
        # Temporizador de retardo para iniciar salida
        self.delay_inicio = 4000  # milisegundos
        self.tiempo_creacion = pygame.time.get_ticks()
        self.puede_salir = False
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

    def move(self, pacman_pos, puertas_group):
        if not self.puede_salir:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_creacion >= self.delay_inicio:
                self.puede_salir = True
            else:
                return  # Aún no se mueve
        if self.en_salida:
            target_x, target_y = self.salida_target

            # Vector hacia el objetivo
            dx = target_x - self.x
            dy = target_y - self.y

            distancia = math.hypot(dx, dy)

            # Si está cerca del objetivo, avanzar al siguiente paso
            if distancia < self.speed:
                self.x, self.y = target_x, target_y
                self.salida_paso += 1
                if self.salida_paso < len(self.salida_ruta):
                    self.salida_target = self.salida_ruta[self.salida_paso]
                else:
                    self.en_salida = False
                    self.mode_timer = pygame.time.get_ticks()
            else:
                # Movimiento normalizado hacia el objetivo
                if distancia != 0:
                    self.x += self.speed * dx / distancia
                    self.y += self.speed * dy / distancia

            self.rect.center = (self.x, self.y)
            return self.x, self.y, self.direction

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

                # Verificar si hay una puerta bloqueando esta dirección
                if puertas_group:
                    next_rect = self.rect.copy()
                    next_rect.center = (self.x + dx * self.speed, self.y + dy * self.speed)
                    bloqueado = False
                    for puerta in puertas_group:
                        if next_rect.colliderect(puerta.rect) and not puerta.permite_paso((dx, dy)):
                            bloqueado = True
                            break
                    if bloqueado:
                        continue  # Saltar esta dirección si la puerta no permite pasar

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

            if puertas_group:
                next_rect = self.rect.copy()
                next_rect.center = (self.x + dx * self.speed, self.y + dy * self.speed)
                for puerta in puertas_group:
                    if next_rect.colliderect(puerta.rect):
                        if not puerta.permite_paso((dx, dy)):
                            return self.x, self.y, self.direction  # Bloqueado por la puerta

            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.center = (self.x, self.y)
        return self.x, self.y, self.direction

    def actualizar_turns(self, muros_group):
        self.rect.center = (self.x, self.y)
        # Chequear colisión probando mover Blinky un paso en cada dirección
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