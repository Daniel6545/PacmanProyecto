import pygame
import math
from pygame.sprite import Sprite
from Config import *
import os

class oscar(Sprite):
    def __init__(self, muros_grupo, x_inicial, y_inicial):
        super().__init__()
        self.x = x_inicial
        self.y = y_inicial
        self.direction = 0
        self.speed = Oscar_speed
        self.scatter_target = scatter_targetO
        self.mode = "chase"
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

        self.en_salida = True
        self.salida_ruta = [
            (self.x - tamaño, self.y),
            (self.x - tamaño, self.y - tamaño),
            (self.x - tamaño, self.y - 2 * tamaño)
        ]
        self.salida_paso = 0
        self.salida_target = self.salida_ruta[0]
        self.delay_inicio = 5000  # Temporizador de retardo para iniciar salida
        self.tiempo_creacion = pygame.time.get_ticks()
        self.puede_salir = False
        self.imagenes = {}
        direccion_rutas = {
            (1, 0): ["OscarDerecha.png", "OscarDerecha2.png"],
            (-1, 0): ["OscarIzquierda.png", "OscarIzquierda2.png"],
            (0, -1): ["OscarArriba.png", "OscarArriba2.png"],
            (0, 1): ["OscarAbajo.png", "OscarAbajo2.png"],
            (0, 0): ["OscarDerecha.png"]
        }


        for direccion, archivos in direccion_rutas.items():
            lista_imagenes = []
            for archivo in archivos:
                imagen = pygame.image.load(os.path.join("Sprites", archivo)).convert_alpha()
                imagen = pygame.transform.scale(imagen, (tamaño_fant, tamaño_fant))
                lista_imagenes.append(imagen)
            self.imagenes[direccion] = lista_imagenes

        # Imágenes modo superpoder (azul)
        self.imagenes_super = []
        for archivo in ["FantasmaSuperpoder.png", "FantasmaSuperpoder2.png"]:
            img = pygame.image.load(os.path.join("Sprites", archivo)).convert_alpha()
            img = pygame.transform.scale(img, (tamaño_fant, tamaño_fant))
            self.imagenes_super.append(img)

        # Imágenes de parpadeo (blanco)
        self.imagenes_parpadeo = []
        for archivo in ["FantasmaSuperpoderFinal.png", "FantasmaSuperpoderFinal2.png"]:
            img = pygame.image.load(os.path.join("Sprites", archivo)).convert_alpha()
            img = pygame.transform.scale(img, (tamaño_fant, tamaño_fant))
            self.imagenes_parpadeo.append(img)

        self.anim_frame = 0
        self.anim_speed = 10
        self.anim_counter = 0

        # Superpoder
        self.super_modo = False
        self.super_timer = 0
        self.super_duration = 7000
        self.parpadeo = False
        self.parpadeo_timer = 0
        self.parpadeo_interval = 300
        self.parpadeo_frame = 0

        self.speed_normal = self.speed
        self.speed_super = self.speed * 0.5

    def activar_superpoder(self):
        self.super_modo = True
        self.super_timer = pygame.time.get_ticks()
        self.parpadeo = False
        self.speed = self.speed_super

    activar_vulnerable = activar_superpoder
    def desactivar_superpoder(self):
        self.super_modo = False
        self.speed = self.speed_normal
        self.parpadeo = False

    desactivar_vulnerable = desactivar_superpoder
    def distance(self, pos1, pos2):
        """Calcula la distancia euclidiana entre dos puntos."""
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def update_mode(self):
        current_time = pygame.time.get_ticks()
        if self.mode == "chase" and current_time - self.mode_timer >= self.mode_duration["chase"]:
            self.mode = "scatter"
            self.mode_timer = current_time
        elif self.mode == "scatter" and current_time - self.mode_timer >= self.mode_duration["scatter"]:
            self.mode = "chase"
            self.mode_timer = current_time

    def move(self, pacman_pos, puertas_group):
        if self.super_modo:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_pasado = tiempo_actual - self.super_timer
            if tiempo_pasado >= self.super_duration:
                self.desactivar_superpoder()
            elif tiempo_pasado >= self.super_duration - 2000:
                self.parpadeo = True

        if not self.puede_salir:
            if pygame.time.get_ticks() - self.tiempo_creacion >= self.delay_inicio:
                self.puede_salir = True
            else:
                return #Aún no se mueve

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

                if puertas_group:
                    next_rect = self.rect.copy()
                    next_rect.center = (self.x + dx * self.speed, self.y + dy * self.speed)
                    bloqueado = any(next_rect.colliderect(p.rect) and not p.permite_paso((dx, dy)) for p in puertas_group)
                    if bloqueado:
                        continue

                nueva_x = self.x + dx * self.speed
                nueva_y = self.y + dy * self.speed
                distancia = math.hypot(self.target[0] - nueva_x, self.target[1] - nueva_y)
                distancias.append((distancia, d))

            if distancias:
                distancias.sort(key=lambda x: x[0])
                self.direction = distancias[0][1]

        if self.turns[self.direction]:
            dx, dy = direction_vectors[self.direction]
            if puertas_group:
                next_rect = self.rect.copy()
                next_rect.center = (self.x + dx * self.speed, self.y + dy * self.speed)
                for puerta in puertas_group:
                    if next_rect.colliderect(puerta.rect) and not puerta.permite_paso((dx, dy)):
                        return self.x, self.y, self.direction
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

        if self.super_modo:
            if self.parpadeo:
                current_time = pygame.time.get_ticks()
                if current_time - self.parpadeo_timer > self.parpadeo_interval:
                    self.parpadeo_timer = current_time
                    self.parpadeo_frame = (self.parpadeo_frame + 1) % 2
                imagen_actual = (
                    self.imagenes_super[self.anim_frame % len(self.imagenes_super)]
                    if self.parpadeo_frame == 0
                    else self.imagenes_parpadeo[self.anim_frame % len(self.imagenes_parpadeo)]
                )
            else:
                imagen_actual = self.imagenes_super[self.anim_frame % len(self.imagenes_super)]
        else:
            imagen_actual = self.imagenes[dir_vector][self.anim_frame]

        rect_imagen = imagen_actual.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(imagen_actual, rect_imagen)
