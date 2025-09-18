import pygame

from board.hex import Hex
from board.hex_grid import HexGrid
from board.pathfinder import Pathfinder
from core.state import GameState, State
from utils.hex_helper import pixel_to_hex

class EventManager:
    def __init__(self, state: GameState, pathfinder: Pathfinder):
        self.state: GameState = state
        self.pathfinder: Pathfinder = pathfinder

    def handle_event(self, event, game):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos, game)
        elif event.type == pygame.KEYUP:
            self.handle_key_press(event.key, game)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_move(event.pos, game)

    def handle_click(self, pos, game):
        col, row = pixel_to_hex(pos[0], pos[1], self.state.hex_size)
        h = self.state.grid.get_hex(col, row)
        if not h:
            return

        if self.state.value == State.Base and h.unit:
            self.state.selected_hex = None
            self.state.selected_unit = h.unit
            self.state.highlighted_hexes = self.pathfinder.reachable_hexes(
                h, self.state.selected_unit.move_range
            )
            self.state.value = State.ReadyToMove
        elif self.state.value == State.ReadyToMove and h in self.state.highlighted_hexes:
            path = self.state.pathfinder_hexes
            if path:
                game.state.start_movement(self.state.selected_unit, path)
            self.state.selected_unit = None
            self.state.highlighted_hexes = []
            self.state.value = State.IsMoving

    def handle_mouse_move(self, pos, game):
        col, row = pixel_to_hex(pos[0], pos[1], self.state.hex_size)
        selected_hex = self.state.grid.get_hex(col, row)
        if not selected_hex:
            return

        if self.state.value == State.Base:
            if self.pathfinder.is_hex_reachable(selected_hex):
                self.state.selected_hex = selected_hex
            else:
                self.state.selected_hex = None
        elif self.state.value == State.ReadyToMove:
            self.state.pathfinder_hexes = self.pathfinder.find_path(self.state.selected_unit.position, selected_hex)

    def handle_key_press(self, key, game):
        if game.state.selected_unit:
            if key == 49:
                game.state.value = State.ReadyToMove
            elif key == 50:
                game.state.value  = State.ReadyToTurnBase
            elif key == 51:
                game.state.value  = State.ReadyToTurnTurret
