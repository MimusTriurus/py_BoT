import heapq
import math

class Pathfinder:
    def __init__(self, grid):
        self.grid = grid
        self.terrain_costs = {
            "plain": 1,
            "swamp": 2,
            "rock": math.inf,
            "water": math.inf
        }

    def neighbors(self, hex_):
        if hex_.q % 2 == 0:
            deltas = [(+1, 0), (-1, 0), (0, -1), (0, +1), (+1, -1), (-1, -1)]
        else:  # odd-q
            deltas = [(+1, 0), (-1, 0), (0, -1), (0, +1), (+1, +1), (-1, +1)]

        result = []
        for dq, dr in deltas:
            n = self.grid.get_hex(hex_.q + dq, hex_.r + dr)
            if n and self.terrain_costs[n.terrain] != math.inf:
                result.append(n)
        return result

    def reachable_hexes(self, start_hex, move_range):
        visited = {}
        fringe = [(start_hex, 0)]
        reachable = []

        while fringe:
            current, dist = fringe.pop(0)
            if current in visited and visited[current] <= dist:
                continue
            visited[current] = dist

            cost = self.terrain_costs[current.terrain]
            if dist <= move_range and cost != math.inf:
                reachable.append(current)

            for neighbor in self.neighbors(current):
                if neighbor.unit is None:  # нельзя идти через занятый
                    new_dist = dist + self.terrain_costs[neighbor.terrain]
                    if new_dist <= move_range:
                        fringe.append((neighbor, new_dist))
        return reachable

    def heuristic(self, a, b):
        aq, ar = a.q, a.r
        bq, br = b.q, b.r
        s1 = -aq - ar
        s2 = -bq - br
        return max(abs(aq - bq), abs(ar - br), abs(s1 - s2))

    def find_path(self, start_hex, target_hex):
        if self.terrain_costs[target_hex.terrain] == math.inf:
            return None

        open_set = []
        counter = 0
        heapq.heappush(open_set, (0, counter, start_hex))
        came_from = {}
        g_score = {start_hex: 0}

        while open_set:
            _, _, current = heapq.heappop(open_set)
            if current == target_hex:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for neighbor in self.neighbors(current):
                if neighbor.unit is not None and neighbor != target_hex:
                    continue

                tentative_g = g_score[current] + self.terrain_costs[neighbor.terrain]
                if tentative_g == math.inf:
                    continue

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, target_hex)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor))
        return None