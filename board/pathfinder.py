# board/pathfinder.py
class Pathfinder:
    def __init__(self, grid):
        self.grid = grid

    def neighbors(self, hex_):
        if hex_.q % 2 == 0:  # even-q
            deltas = [(+1, 0), (-1, 0), (0, -1), (0, +1), (+1, -1), (-1, -1)]
        else:  # odd-q
            deltas = [(+1, 0), (-1, 0), (0, -1), (0, +1), (+1, +1), (-1, +1)]

        result = []
        for dq, dr in deltas:
            n = self.grid.get_hex(hex_.q + dq, hex_.r + dr)
            if n:
                result.append(n)
        return result

    def reachable_hexes(self, start_hex, move_range):
        """Возвращает список гексов, куда может пойти юнит"""
        visited = set()
        fringe = [(start_hex, 0)]
        reachable = []

        while fringe:
            current, dist = fringe.pop(0)
            if current in visited or dist > move_range:
                continue
            visited.add(current)
            reachable.append(current)
            for neighbor in self.neighbors(current):
                if neighbor.unit is None:  # можно проходить только по пустым
                    fringe.append((neighbor, dist+1))
        return reachable
