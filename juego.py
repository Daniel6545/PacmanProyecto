import pygame
import sys
from Config import *
from Pacman import pacman
class Juego:
    def __init__(self):
        self.direccion_actual = (0, 0)
        self.ventana= pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #nombrar ventana
        pygame.display.set_caption("Pacman")

        #Bucle para saber si estas en el juego
        self.running= True
        #Crear jugador
        self.pacman= pacman()

    def update (self):
        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        # mantener dirección y priorizar horizontal en caso de tocar dos teclas
        if dx != 0:
            self.direccion_actual = (dx, 0)
        elif dy != 0:
            self.direccion_actual = (0, dy)
        #mover jugador
        self.pacman.mover(*self.direccion_actual)

    def eventos(self):
        for event in pygame.event.get():
        #para cerrar ventana:
            if event.type == pygame.QUIT:
                self.running= False
    def draw(self):
        self.ventana.fill(BLACK)
        self.pacman.draw(self.ventana)
        pygame.display.flip()
    def run(self):
        while self.running:
            self.eventos() #procesar eventos
            self.draw()
            self.update()
