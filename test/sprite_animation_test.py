import pygame


def extract_frames(sheet, padding=1):
    sheet_width, sheet_height = sheet.get_size()
    pixels = pygame.surfarray.pixels_alpha(sheet)
    visited = [[False]*sheet_height for _ in range(sheet_width)]
    frames = []

    def flood_fill(x, y):
        stack = [(x, y)]
        min_x, min_y, max_x, max_y = x, y, x, y

        while stack:
            cx, cy = stack.pop()
            if visited[cx][cy] or pixels[cx][cy] == 0:
                continue
            visited[cx][cy] = True
            min_x = min(min_x, cx)
            min_y = min(min_y, cy)
            max_x = max(max_x, cx)
            max_y = max(max_y, cy)

            for nx, ny in [(cx-1,cy),(cx+1,cy),(cx,cy-1),(cx,cy+1)]:
                if 0 <= nx < sheet_width and 0 <= ny < sheet_height:
                    stack.append((nx, ny))

        # Безопасный padding
        min_x = max(min_x - padding, 0)
        min_y = max(min_y - padding, 0)
        max_x = min(max_x + padding, sheet_width - 1)
        max_y = min(max_y + padding, sheet_height - 1)

        # Прямоугольник для subsurface
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        return pygame.Rect(min_x, min_y, width, height)

    for x in range(sheet_width):
        for y in range(sheet_height):
            if not visited[x][y] and pixels[x][y] != 0:
                rect = flood_fill(x, y)
                frame = sheet.subsurface(rect).copy()
                frames.append(frame)

    return frames


# ------------------ Pygame Setup ------------------
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Viewer")
clock = pygame.time.Clock()

# Загружаем атлас
sheet = pygame.image.load(r"D:\Projects\Python\PyBoT\assets\sprites\tank_heavy_turret.png").convert_alpha()
frames = extract_frames(sheet, padding=2)
print(f"Найдено {len(frames)} кадров")

current_frame = 0

# ------------------ Главный цикл ------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_frame = (current_frame + 1) % len(frames)
            elif event.key == pygame.K_LEFT:
                current_frame = (current_frame - 1) % len(frames)

    screen.fill((30, 30, 30))  # фон
    if frames:
        frame = frames[current_frame]
        rect = frame.get_rect(center=(400, 300))
        screen.blit(frame, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()