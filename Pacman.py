from Config import *
import pygame
import os
from pygame.sprite import Sprite

class pacman(Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = SCREEN_HEIGHT // 2

        # Cargar y escalar imágenes una sola vez para cada dirección
        self.imagenes = {}
        direccion_rutas = {
            (1, 0): ["PacmanDerecha.png", "PacmanDerecha2.png"],
            (-1, 0): ["PacmanIzquierda.png", "PacmanIzquierda2.png"],
            (0, -1): ["PacmanArriba.png", "PacmanArriba2.png"],
            (0, 1): ["PacmanAbajo.png", "PacmanAbajo2.png"],
            (0, 0): ["PacmanDerecha.png"],  # Imagen por defecto cuando está detenido
        }
        for direccion, archivos in direccion_rutas.items(): #carga y prepara todas las imágenes necesarias para cada dirección
            lista_imagenes = []
            for archivo in archivos:
                imagen = pygame.image.load(os.path.join("Sprites", archivo)).convert_alpha()
                imagen = pygame.transform.scale(imagen, (tamaño_pacman, tamaño_pacman))
                lista_imagenes.append(imagen)
            self.imagenes[direccion] = lista_imagenes  # Guardamos lista de imágenes

        self.direccion_actual = (0, 0)
        self.direccion_objetivo = (0, 0)

        self.frame_animacion = 0  # Contador para frame actual de animación
        self.contador_animacion = 0  # Contador para controlar cambio de frame

        self.image = self.imagenes[self.direccion_actual][0] #Imagen inicial
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.velocidad = Pac_Vel

    def puede_moverse(self, nuevo_rect, puertas_group, muros, dx, dy):
        # Verifica muros
        if any(nuevo_rect.colliderect(muro.rect) for muro in muros):
            return False
        # Verifica puertas
        for puerta in puertas_group:
            if puerta.rect.colliderect(nuevo_rect):
                if hasattr(puerta, "permite_paso") and not puerta.permite_paso((dx, dy)):
                    return False
        return True
    def mover(self, muros, puertas_group):
        dx, dy = self.direccion_objetivo
        if dx != 0 or dy != 0:
            rect_prueba = self.rect.copy()
            rect_prueba.x += dx * self.velocidad
            rect_prueba.y += dy * self.velocidad
            if self.puede_moverse(rect_prueba, puertas_group, muros, dx, dy):
                self.direccion_actual = self.direccion_objetivo

        dx, dy = self.direccion_actual

        # Movimiento horizontal con chequeo de colisión
        dx, dy = self.direccion_actual
        nueva_x = self.x + dx * self.velocidad
        rect_x = self.rect.copy()
        rect_x.x = int(nueva_x)
        if not any(rect_x.colliderect(muro.rect) for muro in muros):
            self.x = nueva_x

        # Movimiento vertical con chequeo de colisión
        nueva_y = self.y + dy * self.velocidad
        rect_y = self.rect.copy()
        rect_y.y = int(nueva_y)
        if self.puede_moverse(rect_y, puertas_group, muros, dx, dy):
            self.y = nueva_y

        # Teletransporte lateral para túneles
        if self.rect.right < 0:
            self.x = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.x = -self.rect.width

        self.rect.topleft = (int(self.x), int(self.y))

        # Animación pacman actualizar frame cada 10 frames
        self.contador_animacion += 1
        if self.contador_animacion >= 13:
            self.contador_animacion = 0
            # Solo alternar si hay más de una imagen para esa dirección
            if len(self.imagenes[self.direccion_actual]) > 1:
                self.frame_animacion = (self.frame_animacion + 1) % len(self.imagenes[self.direccion_actual])
            else:
                self.frame_animacion = 0

        # Actualizar la imagen con el frame actual
        self.image = self.imagenes[self.direccion_actual][self.frame_animacion]

    def detener(self):
        self.direccion_actual = (0, 0)
        self.direccion_objetivo = (0, 0)
        self.frame_animacion = 0
        self.contador_animacion = 0
        self.image = self.imagenes[(0, 0)][0]

    def draw(self, ventana):
        ventana.blit(self.image, self.rect)