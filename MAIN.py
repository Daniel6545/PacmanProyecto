import pygame
import sys
from juego import Juego

def main():
    try:
        #abrir juego
        pygame.init()
        #crear y correr juego
        juego = Juego()
        juego.run()
    except Exception as e:
        print(f"Error:{e}")
        sys.exit(1)
    finally:
        pygame.QUIT()
        sys.exit()

if __name__ == "__main__":
    main()







