class TurnManager:
    def __init__(self, state):
        self.state = state
        self.current_player = 1

    def next_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1
        # сброс очков действий юнитов и т.п.