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


def animate_movement(unit, path, surface, grid, hex_size, fps=30):
    clock = pygame.time.Clock()
    for i in range(1, len(path)):
        start_hex = path[i - 1]
        end_hex = path[i]
        # print(f'move --> {end_hex}')
        start_x, start_y = hex_to_pixel(start_hex.q, start_hex.r, hex_size)
        end_x, end_y = hex_to_pixel(end_hex.q, end_hex.r, hex_size)
        dq = end_hex.q - start_hex.q
        dr = end_hex.r - start_hex.r
        unit.update_orientation(dq, dr)
        steps = 10
        for step in range(1, steps + 1):
            t = step / steps
            current_x = start_x + (end_x - start_x) * t
            current_y = start_y + (end_y - start_y) * t

            surface.fill((30, 30, 30))

            for row in grid.grid:
                for hex_ in row:
                    center = hex_to_pixel(hex_.q, hex_.r, hex_size)
                    highlight = hex_ in highlighted_hexes
                    draw_hex(surface, center, hex_size, hex_, highlight=highlight)

            for row in grid.grid:
                for hex_ in row:
                    if hex_.unit:
                        if hex_ == unit.position:
                            draw_unit(surface, (current_x, current_y), hex_size, hex_.unit)
                        else:
                            draw_unit(surface, center, hex_size, hex_.unit)

            pygame.display.flip()
            clock.tick(fps)
        # update unit position
        end_hex.unit = unit
        start_hex.unit = None
        unit.position = end_hex


def handle_click(pos, grid, pf):
    global selected_unit, highlighted_hexes, selected_hex

    hex_address = pixel_to_hex(pos[0], pos[1], HEX_SIZE)
    h = grid.get_hex(hex_address[0], hex_address[1])
    if selected_unit is None and h.unit:
        selected_hex = h
        selected_unit = h.unit
        highlighted_hexes = pf.reachable_hexes(h, selected_unit.move_range)
    elif selected_unit and h in highlighted_hexes:
        path = pf.find_path(selected_unit.position, h)
        if path:
            # print('==> start animation')
            animate_movement(selected_unit, path, screen, grid, HEX_SIZE)
            # print('==> stop animation')
        selected_unit = None
        highlighted_hexes = []


def main():
    global screen
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

    tank.set_base_position(start_hex)

    running = True

    while running:
        screen.fill((30, 30, 30))

        for row in grid.grid:
            for hex in row:
                center = hex_to_pixel(hex.q, hex.r, HEX_SIZE)
                highlight = hex in highlighted_hexes
                if not highlight:
                    draw_hex(screen, center, HEX_SIZE, hex, highlight=False)

        for row in grid.grid:
            for hex in row:
                center = hex_to_pixel(hex.q, hex.r, HEX_SIZE)
                highlight = hex in highlighted_hexes
                if highlight:
                    draw_hex(screen, center, HEX_SIZE, hex, highlight=highlight)
                if hex.unit is not None:
                    draw_unit(screen, center, HEX_SIZE, hex.unit)

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
                    # print(selected_hex)
            elif event.type == pygame.KEYUP:
                print(event)

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
