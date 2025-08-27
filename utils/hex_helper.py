import math

from board.hex import Hex


def hex_to_pixel(q, r, size):
    x = size * (3 / 2 * q) + size
    y = size * (3 ** 0.5 * (r + 0.5 * (q % 2))) + size
    return int(x), int(y)


def hex_round(q, r):
    s = -q - r
    rq = round(q)
    rr = round(r)
    rs = round(s)

    q_diff = abs(rq - q)
    r_diff = abs(rr - r)
    s_diff = abs(rs - s)

    if q_diff > r_diff and q_diff > s_diff:
        rq = -rr - rs
    elif r_diff > s_diff:
        rr = -rq - rs
    else:
        rs = -rq - rr

    col = int(rq)
    row = int(rr)
    return col, row


def pixel_to_hex(px, py, size):
    q = int(px / (1.5 * size))
    r = int((py / (math.sqrt(3) * size)) - 0.5 * (q % 2))
    return q, r


def hex_grid_fit(screen_width, screen_height, hex_size):
    step_x = 1.5 * hex_size
    step_y = math.sqrt(3) * hex_size

    cols = int(screen_width // step_x)
    rows = int(screen_height // step_y)

    return cols, rows
