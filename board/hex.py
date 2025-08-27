class Hex:
    def __init__(self, q: int, r: int, terrain=None):
        self.q = q
        self.r = r
        self.terrain = terrain
        self.unit = None

    def __repr__(self):
        return f"Hex({self.x}, {self.y}, {self.terrain})"
