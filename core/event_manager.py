import pygame
from utils.hex_helper import pixel_to_hex

class EventManager:
    def __init__(self, state, pathfinder):
        self.state = state
        self.pathfinder = pathfinder

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos, game)
        elif event.type == pygame.KEYUP:
            print(f"Key released: {event.key}")
        elif event.type == pygame.MOUSEMOTION:
            pass

    def handle_click(self, pos, game):
        col, row = pixel_to_hex(pos[0], pos[1], self.state.hex_size)
        h = self.state.grid.get_hex(col, row)
        if not h:
            return

        if self.state.selected_unit is None and h.unit:
            self.state.selected_hex = h
            self.state.selected_unit = h.unit
            self.state.highlighted_hexes = self.pathfinder.reachable_hexes(
                h, self.state.selected_unit.move_range
            )
        elif self.state.selected_unit and h in self.state.highlighted_hexes:
            path = self.pathfinder.find_path(self.state.selected_unit.position, h)
            if path:
                game.state.start_movement(self.state.selected_unit, path)
            self.state.selected_unit = None
            self.state.highlighted_hexes = []

    def handle_mouse_move(self):
        pass
