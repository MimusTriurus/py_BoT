from .base_unit import BaseUnit

class Tank(BaseUnit):
    def __init__(self):
        super().__init__(name="Tank", hp=100, attack=40, move_range=2)