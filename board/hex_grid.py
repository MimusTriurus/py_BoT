from .hex import Hex

class HexGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self._generate_grid()

    def _generate_grid(self):
        return [[Hex(q, r, terrain="plain") for q in range(self.width)] for r in range(self.height)]

    def get_hex(self, q: int, r: int):
        if 0 <= q < self.width and 0 <= r < self.height:
            return self.grid[r][q]
        return None

