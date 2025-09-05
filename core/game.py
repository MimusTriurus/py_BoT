import pygame
from board.pathfinder import Pathfinder
from rendering import draw_hex, draw_unit
from utils.hex_helper import hex_to_pixel, pixel_to_hex, hex_grid_fit
from units.tank import Tank
from core.state import GameState
from core.event_manager import EventManager
from core.turn_manager import TurnManager


class Game:
    def __init__(self, width, height, hex_size):
        self.width = width
        self.height = height
        self.hex_size = hex_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hex Strategy")

        cols, rows = hex_grid_fit(self.width, self.height, self.hex_size)
        self.state = GameState(cols, rows, hex_size)

        self.pathfinder = Pathfinder(self.state.grid)
        self.event_manager = EventManager(self.state, self.pathfinder)
        self.turn_manager = TurnManager(self.state)

        tank = Tank()
        tank.base_orientation = 2
        tank.turret_orientation = 2

        start_hex = self.state.grid.get_hex(0, 0)
        start_hex.unit = tank
        tank.set_base_position(start_hex)

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.event_manager.handle_event(event, self)

    def update(self, dt):
        self.state.update(dt)

    def render(self):
        self.screen.fill((30, 30, 30))

        for row in self.state.grid.grid:
            for hex_ in row:
                center = hex_to_pixel(hex_.q, hex_.r, self.hex_size)
                draw_hex(self.screen, center, self.hex_size, hex_, highlight=False)

        for row in self.state.grid.grid:
            for hex_ in row:
                center = hex_to_pixel(hex_.q, hex_.r, self.hex_size)
                highlight = hex_ in self.state.highlighted_hexes
                if highlight:
                    draw_hex(self.screen, center, self.hex_size, hex_, highlight=True)
                if hex_.unit:
                    draw_unit(self.screen, center, self.hex_size, hex_.unit)

        pygame.display.flip()
