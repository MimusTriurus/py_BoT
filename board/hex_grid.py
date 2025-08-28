from .hex import Hex
import random

TERRAINS = ["plain", "swamp", "rock", "water"]

class HexGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self._generate_grid()

    def _generate_grid(self):
        grid = []
        for r in range(self.height):
            row = []
            for q in range(self.width):
                terrain = random.choices(
                    TERRAINS,
                    weights=[0.6, 0.2, 0.1, 0.1]  # вероятность выбора типа
                )[0]
                row.append(Hex(q, r, terrain=terrain))
            grid.append(row)
        return grid

    def get_hex(self, q: int, r: int):
        if 0 <= q < self.width and 0 <= r < self.height:
            return self.grid[r][q]
        return None