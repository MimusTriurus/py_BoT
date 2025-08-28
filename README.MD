hex_tactics/
│── main.py
│── settings.py
│
├── core/
│   ├── __init__.py
│   ├── game.py
│   ├── state.py
│   ├── turn_manager.py
│   ├── event_manager.py
│
├── board/
│   ├── __init__.py
│   ├── hex.py
│   ├── hex_grid.py
│   ├── terrain.py
│   ├── pathfinder.py
│
├── units/
│   ├── __init__.py
│   ├── base_unit.py
│   ├── tank.py
│   ├── apc.py
│   ├── artillery.py
│   ├── unit_factory.py
│
├── ai/
│   ├── __init__.py
│   ├── ai_controller.py
│   ├── ai_strategy.py
│
├── ui/
│   ├── __init__.py
│   ├── hud.py
│   ├── menu.py
│   ├── button.py
│   ├── panel.py
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py
│   ├── math_utils.py
│
├── assets/
│   ├── images/
│   ├── sounds/
│   ├── fonts/
│
└── saves/

# Hex directions:
0 — вверх
1 — вверх-вправо
2 — вниз-вправо
3 — вниз
4 — вниз-влево
5 — вверх-влево

# Keys
||Key||Code||Desc||
|1|49|movement|
|2|50|attack|
|3|51|rotate base|
|4|52|rotate turret|