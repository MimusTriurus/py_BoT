class BaseUnit:
    def __init__(self, name: str, hp: int, attack: int, move_range: int,
                 base_orientation: int = 0, turret_orientation: int = 0):
        """
        :param base_orientation: направление шасси/базы 0-5 по часовой стрелке
        :param turret_orientation: направление башни 0-5 по часовой стрелке
        """
        self.name = name
        self.hp = hp
        self.attack = attack
        self.move_range = move_range
        self.position = None  # ссылка на Hex
        self.base_orientation = base_orientation % 6
        self.turret_orientation = turret_orientation % 6

    def move(self, target_hex):
        if self.position:
            self.position.unit = None
        target_hex.unit = self
        self.position = target_hex

    def attack_unit(self, other):
        other.hp -= self.attack
        print(f"{self.name} атакует {other.name}, у {other.name} осталось {other.hp} HP")

    def set_base_orientation(self, orientation):
        """Задаёт направление шасси/базы 0-5"""
        self.base_orientation = orientation % 6

    def set_turret_orientation(self, orientation):
        """Задаёт направление башни 0-5"""
        self.turret_orientation = orientation % 6
