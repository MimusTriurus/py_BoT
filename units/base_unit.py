class BaseUnit:
    def __init__(
            self,
            name: str,
            hp: int,
            attack: int,
            move_range: int,
            attack_range: int,
            base_orientation: int = 0,
            turret_orientation: int = 0
    ):
        self.name = name
        self.hp = hp
        self.attack = attack

        self.move_range = move_range
        self.attack_range = attack_range

        self.position = None  # ссылка на Hex

        self.base_orientation = base_orientation % 6
        self.turret_orientation = turret_orientation % 6

    def update_orientation(self, dq, dr):
        if self.position.q % 2 == 0:
            deltas = [(0,-1),(1,-1),(1,0),(0,1),(-1,0),(-1,-1)]
        else:
            deltas = [(0,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        for i, (dx, dy) in enumerate(deltas):
            if (dq, dr) == (dx, dy):
                opposite = (self.base_orientation + 3) % 6
                if i != opposite:
                    self.base_orientation = i
                break

    def move(self, target_hex):
        if self.position:
            dq = target_hex.q - self.position.q
            dr = target_hex.r - self.position.r

            # Выбираем delta для текущей колонки (odd-q layout)
            if self.position.q % 2 == 0:
                deltas = [
                    (0, -1),  # 0 вверх
                    (1, -1),  # 1 вверх-вправо
                    (1, 0),  # 2 вниз-вправо
                    (0, 1),  # 3 вниз
                    (-1, 0),  # 4 вниз-влево
                    (-1, -1)  # 5 вверх-влево
                ]
            else:
                deltas = [
                    (0, -1),  # 0 вверх
                    (1, 0),  # 1 вверх-вправо
                    (1, 1),  # 2 вниз-вправо
                    (0, 1),  # 3 вниз
                    (-1, 1),  # 4 вниз-влево
                    (-1, 0)  # 5 вверх-влево
                ]

            # Определяем направление шасси
            for i, (dx, dy) in enumerate(deltas):
                if (dq, dr) == (dx, dy):
                    # Проверяем: если движение не «назад», обновляем ориентацию
                    # Назад — это противоположное направление
                    opposite = (self.base_orientation + 3) % 6
                    if i != opposite:
                        self.base_orientation = i
                    break

            # Освобождаем текущий hex
            self.position.unit = None
        print(self.base_orientation)
        # Занимаем новый hex
        target_hex.unit = self
        self.position = target_hex

    def attack_unit(self, other):
        other.hp -= self.attack
        print(f"{self.name} атакует {other.name}, у {other.name} осталось {other.hp} HP")

    def set_base_orientation(self, orientation):
        """Задаёт направление шасси/базы 0-5"""
        self.base_orientation = orientation % 6

    def set_base_position(self, target_hex):
        self.position = target_hex

    def set_turret_orientation(self, orientation):
        """Задаёт направление башни 0-5"""
        self.turret_orientation = orientation % 6
