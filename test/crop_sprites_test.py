import cv2
import numpy as np

# Загружаем атлас (с альфой)
atlas = cv2.imread(r"D:\Projects\Python\PyBoT\assets\sprites\tank_heavy.png", cv2.IMREAD_UNCHANGED)

h, w, c = atlas.shape
assert c == 4, "Нужен PNG с альфой (RGBA)"

cols, rows = 8, 8
frame_w = w // cols
frame_h = h // rows

sprites = []
max_w, max_h = 0, 0

# --- 1. Разрезаем по сетке ---
for r in range(rows):
    for c_ in range(cols):
        x1, x2 = c_ * frame_w, (c_+1) * frame_w
        y1, y2 = r * frame_h, (r+1) * frame_h
        frame = atlas[y1:y2, x1:x2, :]

        # --- 2. Обрезаем по альфе ---
        a = frame[:, :, 3]
        ys, xs = np.where(a > 0)
        if len(xs) == 0:
            continue
        bx1, bx2, by1, by2 = xs.min(), xs.max(), ys.min(), ys.max()
        crop = frame[by1:by2+1, bx1:bx2+1, :]
        sprites.append(crop)

        # Определяем общий размер
        max_w = max(max_w, crop.shape[1])
        max_h = max(max_h, crop.shape[0])

# --- 3. Центрируем ---
normalized = []
for s in sprites:
    canvas = np.zeros((max_h, max_w, 4), dtype=np.uint8)
    y_off = (max_h - s.shape[0]) // 2
    x_off = (max_w - s.shape[1]) // 2
    canvas[y_off:y_off+s.shape[0], x_off:x_off+s.shape[1], :] = s
    normalized.append(canvas)

# --- 4. Анимация (последовательное отображение) ---
idx = 0
while True:
    frame = normalized[idx]
    bgr = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    cv2.imshow("Animation", bgr)
    key = cv2.waitKey(0)  # ждем нажатие

    if key == 27:  # ESC = выход
        break
    elif key == 32:  # SPACE = следующий кадр
        idx = (idx + 1) % len(normalized)

cv2.destroyAllWindows()
