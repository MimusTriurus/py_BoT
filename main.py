import pygame
import math
import pygame.freetype
from board.hex_grid import HexGrid
from board.hex import Hex
from board.pathfinder import Pathfinder
from rendering import draw_hex, draw_unit
from units.tank import Tank
from utils.hex_helper import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEX_SIZE = 40

selected_unit = None
highlighted_hexes = []
selected_hex = None


def handle_click(pos, grid, pf):
    global selected_unit, highlighted_hexes, selected_hex

    hex_address = pixel_to_hex(pos[0], pos[1], HEX_SIZE)
    h = grid.get_hex(hex_address[0], hex_address[1])
    if selected_unit is None and h.unit:
        selected_hex = h
        selected_unit = h.unit
        highlighted_hexes = pf.reachable_hexes(h, selected_unit.move_range)
    elif selected_unit:
        if selected_hex:
            selected_hex.unit = None
        if h in highlighted_hexes:
            selected_unit.move(h)
        selected_unit = None
        highlighted_hexes = []
    return

    for row in grid.grid:
        for h in row:
            x, y = hex_to_pixel(h.q, h.r, HEX_SIZE)
            if (pos[0] - x) ** 2 + (pos[1] - y) ** 2 <= HEX_SIZE ** 2:
                if selected_unit is None and h.unit:
                    selected_hex = h
                    selected_unit = h.unit
                    highlighted_hexes = pf.reachable_hexes(h, selected_unit.move_range)
                elif selected_unit:
                    if selected_hex:
                        selected_hex.unit = None
                    if h in highlighted_hexes:
                        selected_unit.move(h)
                    selected_unit = None
                    highlighted_hexes = []
                return


def main():
    pygame.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hex Grid")

    cols, rows = hex_grid_fit(SCREEN_WIDTH, SCREEN_HEIGHT, HEX_SIZE)

    grid = HexGrid(cols, rows)
    pf = Pathfinder(grid)
    clock = pygame.time.Clock()

    tank = Tank()
    tank.base_orientation = 2
    tank.turret_orientation = 2

    start_hex = grid.get_hex(0, 0)
    start_hex.unit = tank

    running = True
    while running:
        screen.fill((30, 30, 30))

        for row in grid.grid:
            for hex in row:
                center = hex_to_pixel(hex.q, hex.r, HEX_SIZE)
                highlight = hex in highlighted_hexes
                if not highlight:
                    draw_hex(screen, center, HEX_SIZE, hex.q, hex.r, highlight=highlight)
                if hex.unit is not None:
                    draw_unit(screen, center, HEX_SIZE, hex.unit)

        for row in grid.grid:
            for hex in row:
                center = hex_to_pixel(hex.q, hex.r, HEX_SIZE)
                highlight = hex in highlighted_hexes
                if highlight:
                    draw_hex(screen, center, HEX_SIZE, hex.q, hex.r, highlight=highlight)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos, grid, pf)

                mx, my = pygame.mouse.get_pos()
                col, row = pixel_to_hex(mx, my, HEX_SIZE)
                if 0 <= col < grid.width and 0 <= row < grid.height:
                    selected_hex = (col, row)
                    print(selected_hex)

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
