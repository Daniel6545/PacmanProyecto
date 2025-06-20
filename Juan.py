import pygame
import math
from pygame.sprite import Sprite
from Config import *
import os

class juan(Sprite):
    def __init__(self, muros_grupo, x_inicial, y_inicial):
        super().__init__()
        self.x = x_inicial
        self.y = y_inicial
        self.direction = 0
        self.speed = Juan_speed  # Define en Config.py
        self.scatter_target = scatter_targetJ  # Define en Config.py
        self.mode = "chase"
        self.muros_grupo = muros_grupo

        self.rect = pygame.Rect(
            self.x - tamaño // 2,
            self.y - tamaño // 2,
            tamaño,
            tamaño
        )

        self.mode_timer = 0
        self.mode_duration = {
            "chase": 20000,
            "scatter": 7000
        }

        self.imagenes = {}
        direccion_rutas = {
            (1, 0): ["JuanDerecha.png", "JuanDerecha2.png"],
            (-1, 0): ["JuanIzquierda.png", "JuanIzquierda2.png"],
            (0, -1): ["JuanArriba.png", "JuanArriba2.png"],
            (0, 1): ["JuanAbajo.png", "JuanAbajo2.png"],
            (0, 0): ["JuanDerecha.png"],
        }
        for direccion, archivos in direccion_rutas.items():
            lista_imagenes = []
            for archivo in archivos:
                imagen = pygame.image.load(os.path.join("Sprites", archivo)).convert_alpha()
                imagen = pygame.transform.scale(imagen, (tamaño_fant, tamaño_fant))
                lista_imagenes.append(imagen)
            self.imagenes[direccion] = lista_imagenes

        self.anim_frame = 0
        self.anim_speed = 10
        self.anim_counter = 0

    def update_mode(self):
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
            0: (1, 0),
            1: (-1, 0),
            2: (0, -1),
            3: (0, 1)
        }

        self.actualizar_turns(self.muros_grupo)

        posibles_dirs = [d for d in range(4) if self.turns[d]]

        if posibles_dirs:
            distancias = []
            direccion_opuesta = {0: 1, 1: 0, 2: 3, 3: 2}

            for d in posibles_dirs:
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

        if self.turns[self.direction]:
            dx, dy = direction_vectors[self.direction]
            self.x += dx * self.speed
            self.y += dy * self.speed

        self.rect.center = (self.x, self.y)

        self.anim_counter += 1
        if self.anim_counter >= self.anim_speed:
            self.anim_counter = 0
            dir_vector = direction_vectors[self.direction]
            self.anim_frame = (self.anim_frame + 1) % len(self.imagenes[dir_vector])

        return self.x, self.y, self.direction

    def actualizar_turns(self, muros_group):
        self.rect.center = (self.x, self.y)
        self.turns = [False, False, False, False]
        step = self.speed

        self.rect.x += step
        self.turns[0] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.x -= step

        self.rect.x -= step
        self.turns[1] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.x += step

        self.rect.y -= step
        self.turns[2] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.y += step

        self.rect.y += step
        self.turns[3] = not pygame.sprite.spritecollideany(self, muros_group)
        self.rect.y -= step

    def draw(self, screen):
        direction_vectors = {
            0: (1, 0),
            1: (-1, 0),
            2: (0, -1),
            3: (0, 1)
        }
        dir_vector = direction_vectors[self.direction]
        imagen_actual = self.imagenes[dir_vector][self.anim_frame]
        rect_imagen = imagen_actual.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(imagen_actual, rect_imagen)
