from typing import Optional, List

import pygame

from board.hex import Hex
from board.hex_grid import HexGrid
from rendering import draw_hex, draw_unit
from units.base_unit import BaseUnit
from utils.hex_helper import hex_to_pixel
from enum import Enum

class State(Enum):
    Base = 0
    ReadyToMove = 1
    IsMoving = 2
    ReadyToTurnBase = 3
    ReadyToTurnTurret = 4


class GameState:
    def __init__(self, cols, rows, hex_size):
        self.grid: HexGrid = HexGrid(cols, rows)
        self.hex_size = hex_size

        self.selected_unit: Optional[BaseUnit] = None
        self.highlighted_hexes: List[Hex] = []
        self.pathfinder_hexes: List[Hex] = []
        self.selected_hex: Optional[Hex] = None

        self.active_movement = None

        self.value = State.Base

    def select_unit(self, unit: BaseUnit):
        self.selected_unit = unit

    def start_movement(self, unit: BaseUnit, path):
        if not path or len(path) < 2:
            return
        self.active_movement = {
            "unit": unit,
            "path": path,
            "index": 0,          # индекс сегмента пути
            "progress": 0.0      # от 0.0 до 1.0
        }

    def update(self, dt):
        """Обновление логики (dt — delta time в секундах)"""
        if self.active_movement:
            move = self.active_movement
            unit = move["unit"]
            path = move["path"]

            start_hex = path[move["index"]]
            end_hex = path[move["index"] + 1]

            # обновляем прогресс шага
            move["progress"] += dt * 2.0  # скорость = 2 сегмента/сек
            if move["progress"] >= 1.0:
                # шаг завершён
                end_hex.unit = unit
                start_hex.unit = None

                dq = end_hex.q - start_hex.q
                dr = end_hex.r - start_hex.r
                unit.update_orientation(dq, dr)

                unit.position = end_hex

                move["index"] += 1
                move["progress"] = 0.0
                # движение завершено
                if move["index"] >= len(path) - 1:
                    self.active_movement = None
                    self.value = State.Base
                    self.pathfinder_hexes.clear()

    def animate_movement(self, unit: BaseUnit, path, surface, fps=30):
        clock = pygame.time.Clock()
        for i in range(1, len(path)):
            start_hex = path[i - 1]
            end_hex = path[i]
            # print(f'move --> {end_hex}')
            start_x, start_y = hex_to_pixel(start_hex.q, start_hex.r, self.hex_size)
            end_x, end_y = hex_to_pixel(end_hex.q, end_hex.r, self.hex_size)
            dq = end_hex.q - start_hex.q
            dr = end_hex.r - start_hex.r
            unit.update_orientation(dq, dr)
            steps = 10
            for step in range(1, steps + 1):
                t = step / steps
                current_x = start_x + (end_x - start_x) * t
                current_y = start_y + (end_y - start_y) * t

                surface.fill((30, 30, 30))

                for row in self.grid.grid:
                    for hex_ in row:
                        center = hex_to_pixel(hex_.q, hex_.r, self.hex_size)
                        draw_hex(surface, center, self.hex_size, hex_, highlight=False)

                for row in self.grid.grid:
                    for hex_ in row:
                        if hex_.unit:
                            center = hex_to_pixel(hex_.q, hex_.r, self.hex_size)
                            if hex_ == unit.position:
                                draw_unit(surface, (current_x, current_y), self.hex_size, hex_.unit)
                            else:
                                draw_unit(surface, center, self.hex_size, hex_.unit)

                pygame.display.flip()
                clock.tick(fps)

            end_hex.unit = unit
            start_hex.unit = None
            unit.position = end_hex