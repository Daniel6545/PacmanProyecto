import pygame
import sys
from Config import *
from Pacman import pacman
from Pared import Muro
from Coin import Coin
from Superpoder import superpoder
from Alberto import alberto
from Oscar import oscar
from Juan import juan
from Puerta import puerta


class Juego:
    def __init__(self):
        self.direccion_actual = (0, 0)
        self.ventana = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.datos = datos
        self.tile_size = tile_size
        self.colores_paredes = colores_paredes

        self.running = True

        self.muro_grupo = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.superpoder_group = pygame.sprite.Group()  # Grupo para superpoderes
        self.fantasmas_group = pygame.sprite.Group()
        self.puertas_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.fuente = pygame.font.SysFont("Calibri", 20)
        self.puntuacion = 0
        self.vidas = 3  # vidas PacMan
        self.mostrar_ready = True

        self.superpoder_activo = False  # Estado del superpoder (activo)
        self.tiempo_superpoder = 0  # Marca el tiempo en que se activa

        # Para controlar fantasmas en reaparición {fantasma: tiempo_comido}
        self.fantasmas_en_reaparicion = {}

        self.mapa_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.crearmapa()

    def crearmapa(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                pos = (x * self.tile_size, y * self.tile_size)

                if celda in self.colores_paredes:
                    muro = Muro(pos[0], pos[1])
                    muro.image.fill(self.colores_paredes[celda])  # Pinta el muro con el color correcto
                    self.muro_grupo.add(muro)

                elif celda == "0":
                    cx = x * self.tile_size + self.tile_size // 2
                    cy = y * self.tile_size + self.tile_size // 2
                    moneda = Coin(cx, cy)
                    self.coin_group.add(moneda)

                elif celda == "S":
                    sp_x = x * self.tile_size + self.tile_size // 2
                    sp_y = y * self.tile_size + self.tile_size // 2
                    self.superpoder = superpoder(sp_x, sp_y)
                    self.superpoder_group.add(self.superpoder)

                elif celda == "P":
                    pac_x = x * self.tile_size + self.tile_size // 2
                    pac_y = y * self.tile_size + self.tile_size // 2
                    self.pacman = pacman(pac_x, pac_y)
                    self.pacman_group = pygame.sprite.Group(self.pacman)

                elif celda == "A":
                    alberto_x = x * self.tile_size + self.tile_size // 2
                    alberto_y = y * self.tile_size + self.tile_size // 2
                    self.alberto = alberto(self.muro_grupo, alberto_x, alberto_y)
                    self.fantasmas_group.add(self.alberto)

                elif celda == "O":
                    oscar_x = x * self.tile_size + self.tile_size // 2
                    oscar_y = y * self.tile_size + self.tile_size // 2
                    self.oscar = oscar(self.muro_grupo, oscar_x, oscar_y)
                    self.fantasmas_group.add(self.oscar)

                elif celda == "J":
                    juan_x = x * self.tile_size + self.tile_size // 2
                    juan_y = y * self.tile_size + self.tile_size // 2
                    self.juan = juan(self.muro_grupo, juan_x, juan_y)
                    self.fantasmas_group.add(self.juan)

                elif celda == "x":
                    self.puerta = puerta(pos[0], pos[1], self.tile_size)
                    self.puertas_group.add(self.puerta)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.pacman.direccion_objetivo = (1, 0)
            self.direccion_actual = (1, 0)
        elif keys[pygame.K_LEFT]:
            self.pacman.direccion_objetivo = (-1, 0)
            self.direccion_actual = (-1, 0)
        elif keys[pygame.K_UP]:
            self.pacman.direccion_objetivo = (0, -1)
            self.direccion_actual = (0, -1)
        elif keys[pygame.K_DOWN]:
            self.pacman.direccion_objetivo = (0, 1)
            self.direccion_actual = (0, 1)

        if self.mostrar_ready and self.direccion_actual != (0, 0):
            self.mostrar_ready = False
            self.pacman.direccion = self.direccion_actual

        if not self.mostrar_ready:
            self.pacman.mover(self.muro_grupo, self.puertas_group)

        tiempo_actual = pygame.time.get_ticks()

        # Mover fantasmas solo si ya empezó el juego (mostrar_ready == False)
        if not self.mostrar_ready:
            for fantasma in self.fantasmas_group:
                if fantasma in self.fantasmas_en_reaparicion:
                    tiempo_comido = self.fantasmas_en_reaparicion[fantasma]
                    # Si pasaron 1.5 segundos reaparece
                    if tiempo_actual - tiempo_comido >= 1500:
                        fantasma.reaparecer()
                        fantasma.visible = True
                        fantasma.vulnerable = self.superpoder_activo
                        del self.fantasmas_en_reaparicion[fantasma]
                    else:
                        # Fantasma oculto sin mover mientras espera reaparecer
                        fantasma.visible = False
                else:
                    fantasma.move((self.pacman.x, self.pacman.y), self.puertas_group)
                    fantasma.visible = True  # Aseguramos que esté visible si no está en reaparición
        else:
            # Fantasmas visibles pero sin moverse antes de empezar (opcional)
            for fantasma in self.fantasmas_group:
                fantasma.visible = True

        # Colisiones monedas normales
        if pygame.sprite.spritecollide(self.pacman, self.coin_group, True):
            self.puntuacion += 10
            print(f"Puntuación: {self.puntuacion}")

        # Colisión con superpoder
        colision_sp = pygame.sprite.spritecollide(self.pacman, self.superpoder_group, True)
        if colision_sp:
            self.superpoder_activo = True
            self.tiempo_superpoder = tiempo_actual
            print("Superpoder activado!")
            # Cambiar estado fantasmas a vulnerables y reducir velocidad
            for fantasma in self.fantasmas_group:
                fantasma.activar_vulnerable()

        # Control duración superpoder y parpadeo
        if self.superpoder_activo:
            tiempo_transcurrido = tiempo_actual - self.tiempo_superpoder
            tiempo_restante = 7000 - tiempo_transcurrido

            # Parpadeo en últimos 2 segundos
            if tiempo_restante <= 2000:
                parpadeo = (tiempo_actual // 300) % 2 == 0
                for fantasma in self.fantasmas_group:
                    if fantasma not in self.fantasmas_en_reaparicion:
                        fantasma.visible = parpadeo
            else:
                for fantasma in self.fantasmas_group:
                    if fantasma not in self.fantasmas_en_reaparicion:
                        fantasma.visible = True

            # Fin superpoder
            if tiempo_transcurrido >= 7000:
                self.superpoder_activo = False
                print("Superpoder terminado.")
                for fantasma in self.fantasmas_group:
                    fantasma.desactivar_vulnerable()
                    fantasma.visible = True

        # Colisión Pac-Man con fantasmas
        fantasmas_en_colision = pygame.sprite.spritecollide(self.pacman, self.fantasmas_group, False)
        if fantasmas_en_colision:
            for fantasma in fantasmas_en_colision:
                if self.superpoder_activo and fantasma.vulnerable:
                    # Pacman se come al fantasma
                    self.puntuacion += 200
                    print(f"Fantasma comido! +200 puntos. Puntuación: {self.puntuacion}")
                    # Ponemos al fantasma en estado de reaparición
                    fantasma.visible = False
                    self.fantasmas_en_reaparicion[fantasma] = tiempo_actual
                    fantasma.en_reaparicion = True
                    fantasma.puede_salir = False
                else:
                    # Pacman pierde vida (fantasma normal lo atrapa)
                    self.vidas -= 1
                    print(f"¡Te ha atrapado un fantasma! Vidas restantes: {self.vidas}")
                    pygame.time.delay(1500)
                    if self.vidas <= 0:
                        print("GAME OVER")
                        self.running = False
                    else:
                        self.reiniciar_pacman()
                        self.reiniciar_fantasmas()
                    break  # Para no procesar múltiples colisiones simultáneas

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reiniciar_pacman(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                if celda == "P":
                    pac_x = x * self.tile_size + self.tile_size // 2
                    pac_y = y * self.tile_size + self.tile_size // 2

                    self.pacman.x = pac_x - self.pacman.rect.width // 2
                    self.pacman.y = pac_y - self.pacman.rect.height // 2
                    self.pacman.rect.topleft = (self.pacman.x, self.pacman.y)
                    self.pacman.direccion_actual = (0, 0)
                    if hasattr(self.pacman, "detener"):
                        self.pacman.detener()
                    return

    def reiniciar_fantasmas(self):
        for y, fila in enumerate(self.datos):
            for x, celda in enumerate(fila):
                cx = x * self.tile_size + self.tile_size // 2
                cy = y * self.tile_size + self.tile_size // 2

                if celda == "A" and hasattr(self, "alberto"):
                    self.alberto.x = cx
                    self.alberto.y = cy
                    self.alberto.rect.topleft = (self.alberto.x, self.alberto.y)
                    self.alberto.direccion_actual = (0, 0)
                    self.alberto.vulnerable = False
                    self.alberto.desactivar_vulnerable()

                if celda == "O" and hasattr(self, "oscar"):
                    self.oscar.x = cx
                    self.oscar.y = cy
                    self.oscar.rect.topleft = (self.oscar.x, self.oscar.y)
                    self.oscar.direccion_actual = (0, 0)
                    self.oscar.vulnerable = False
                    self.oscar.desactivar_vulnerable()

                if celda == "J" and hasattr(self, "juan"):
                    self.juan.x = cx
                    self.juan.y = cy
                    self.juan.rect.topleft = (self.juan.x, self.juan.y)
                    self.juan.direccion_actual = (0, 0)
                    self.juan.vulnerable = False
                    self.juan.desactivar_vulnerable()

    def draw(self):
        self.ventana.fill(BLACK)  # Limpiar pantalla con negro o color de fondo
        self.ventana.blit(self.mapa_surface, (0, 0))

        # Dibujar monedas normales
        self.coin_group.draw(self.ventana)
        # Dibujar superpoderes
        self.superpoder_group.draw(self.ventana)

        # Dibujar fantasmas
        for fantasma in self.fantasmas_group:
            fantasma.draw(self.ventana)
        # Dibujar muros
        self.muro_grupo.draw(self.ventana)

        # Dibujar Pac-Man
        self.pacman.draw(self.ventana)

        # Mostrar puntuación
        texto = self.fuente.render(f"SCORE: {self.puntuacion}", True, WHITE)
        self.ventana.blit(texto, (10, 10))

        # Mostrar vidas y mini Pac-Man
        sprite_vida = pygame.transform.scale(self.pacman.imagenes[(1, 0)][0], (20, 20))
        for i in range(self.vidas):
            x = SCREEN_WIDTH - 60 + i * 20
            y = 10
            self.ventana.blit(sprite_vida, (x, y))

        # Mostrar READY! al inicio
        if self.mostrar_ready:
            ready_text = self.fuente.render("R E A D Y !", True, Rojo)
            ready_x = tile_size * 13.5
            ready_y = tile_size * 18.5
            text_rect = ready_text.get_rect(center=(ready_x, ready_y))
            self.ventana.blit(ready_text, text_rect)

        # Dibujar puertas
        for puerta in self.puertas_group:
            puerta.draw(self.ventana)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.eventos()
            self.update()
            self.draw()
            self.clock.tick(60)

def main():
    try:
        pygame.init()
        juego = Juego()
        juego.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
        main()
