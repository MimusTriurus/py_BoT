import pygame
import math


def draw_unit(
        surface,
        hex_center,
        hex_size,
        unit,
        body_color=(0, 128, 0),
        nose_color=(0, 200, 0),
        turret_color=(0, 255, 0),
        barrel_color=(0, 255, 255)
):
    """
    Рисует юнит на Flat-top гексе:
    - шасси с острым носом (base_orientation)
    - башня + ствол (turret_orientation)
    """
    x, y = hex_center

    # --- Шасси ---
    body_w = hex_size * 0.9
    body_h = hex_size * 0.7
    rect = pygame.Surface((body_w, body_h), pygame.SRCALPHA)
    rect.fill(body_color)

    # --- Треугольник носа ---
    nose_w = body_w * 0.5
    nose_h = body_h
    nose_points = [
        (body_w, body_h/2),             # центр правый (нос)
        (body_w - nose_w, 0),           # верх левый
        (body_w - nose_w, body_h)       # низ левый
    ]
    pygame.draw.polygon(rect, nose_color, nose_points)

    # --- Поворот корпуса по направлению шасси ---
    base_angle_deg = unit.base_orientation * 60 - 90
    rotated_body = pygame.transform.rotate(rect, -base_angle_deg)
    body_rect = rotated_body.get_rect(center=(x, y))
    surface.blit(rotated_body, body_rect)

    # --- Башня ---
    turret_radius = body_h * 0.3
    turret_center = (x, y)
    pygame.draw.circle(surface, turret_color, turret_center, int(turret_radius))

    # --- Ствол башни ---
    barrel_length = body_w * 0.7
    turret_angle_deg = unit.turret_orientation * 60 - 90
    turret_angle_rad = math.radians(turret_angle_deg)
    end_x = turret_center[0] + math.cos(turret_angle_rad) * barrel_length
    end_y = turret_center[1] + math.sin(turret_angle_rad) * barrel_length
    pygame.draw.line(surface, barrel_color, turret_center, (end_x, end_y), 3)


def draw_hex(surface, center, size, hex_, highlight=False):
    # выбор цвета по типу поверхности
    terrain_colors = {
        "plain": (180, 220, 180),
        "swamp": (100, 150, 100),
        "rock":  (130, 130, 130),
        "water": (70, 100, 200)
    }

    color = terrain_colors.get(hex_.terrain, (200, 200, 200))

    # координаты углов гекса
    points = []
    for i in range(6):
        angle = math.radians(60 * i)
        dx = size * math.cos(angle)
        dy = size * math.sin(angle)
        points.append((center[0] + dx, center[1] + dy))

    # закраска
    pygame.draw.polygon(surface, color, points)
    # рамка: жёлтая если highlight
    pygame.draw.polygon(surface, (255, 255, 0) if highlight else (50, 50, 50), points, 2)

    # отрисовка текста (координаты)
    if False:
        font = pygame.freetype.SysFont(None, 12)
        text = f"[{hex_.q},{hex_.r}]"
        text_rect = font.get_rect(text)
        text_rect.center = center
        font.render_to(surface, (text_rect.x, text_rect.y), text, (255, 255, 255))

