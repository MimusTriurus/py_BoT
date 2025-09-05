import pygame
import pygame.freetype

from core.game import Game

def main():
    pygame.init()
    pygame.freetype.init()
    game = Game(800, 600, hex_size=40)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
