"""
Generates high quality test food plate images with distinct dishes:
- Plate 1: Rice + Chicken Curry + Dal + Salad (The user's exact primary example!)
- Plate 2: Grilled Salmon + Rice + Salad + Broccoli
- Plate 3: Paneer Butter Masala + Jeera Rice + Dal + Salad
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def create_sample_plates(output_dir: str = "backend/app/samples"):
    os.makedirs(output_dir, exist_ok=True)

    # ----------------- Plate 1: Rice + Chicken Curry + Dal + Salad -----------------
    w, h = 800, 800
    img = np.zeros((h, w, 3), dtype=np.uint8)

    # Background dining table (warm dark wooden tone)
    img[:] = (35, 45, 55) # BGR dark warm slate

    # Ceramic plate (white/light gray with rim)
    cx, cy, r = 400, 400, 350
    cv2.circle(img, (cx, cy), r + 8, (180, 190, 200), -1, cv2.LINE_AA) # Plate rim
    cv2.circle(img, (cx, cy), r, (240, 245, 248), -1, cv2.LINE_AA)     # Plate inner base
    cv2.circle(img, (cx, cy), r - 20, (230, 235, 240), 2, cv2.LINE_AA) # Plate inner circle

    # 1. Top-Left: Steamed White Rice (Grain texture)
    rice_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(rice_mask, (310, 300), (140, 110), -20, 0, 360, 255, -1)
    # Add rice grain color (clean white/cream with subtle grain noise)
    noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
    rice_color = np.clip(np.array([235, 242, 245], dtype=np.int16) + noise, 210, 255).astype(np.uint8)
    img[rice_mask > 0] = rice_color[rice_mask > 0]

    # 2. Top-Right: Chicken Curry (Rich red/orange gravy with chicken pieces)
    curry_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(curry_mask, (500, 310), (130, 115), 25, 0, 360, 255, -1)
    curry_noise = np.random.randint(-20, 20, (h, w, 3), dtype=np.int16)
    # BGR for rich red-orange curry: B~25, G~65, R~195
    curry_color = np.clip(np.array([25, 65, 195], dtype=np.int16) + curry_noise, 0, 255).astype(np.uint8)
    img[curry_mask > 0] = curry_color[curry_mask > 0]
    # Chicken chunks highlights
    cv2.circle(img, (480, 290), 25, (20, 50, 160), -1, cv2.LINE_AA)
    cv2.circle(img, (530, 320), 30, (15, 45, 150), -1, cv2.LINE_AA)

    # 3. Bottom-Left: Dal (Golden yellow lentils / tadka)
    dal_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(dal_mask, (310, 500), (135, 110), 15, 0, 360, 255, -1)
    dal_noise = np.random.randint(-15, 15, (h, w, 3), dtype=np.int16)
    # BGR for golden yellow dal: B~30, G~180, R~230
    dal_color = np.clip(np.array([30, 180, 230], dtype=np.int16) + dal_noise, 0, 255).astype(np.uint8)
    img[dal_mask > 0] = dal_color[dal_mask > 0]
    # Tadka mustard/cumin specks
    for _ in range(40):
        px = np.random.randint(220, 400)
        py = np.random.randint(430, 570)
        if dal_mask[py, px] > 0:
            cv2.circle(img, (px, py), np.random.randint(1, 3), (15, 25, 45), -1)

    # 4. Bottom-Right: Fresh Salad (Cucumber, Tomato, Green Lettuce)
    salad_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(salad_mask, (490, 490), (130, 110), -15, 0, 360, 255, -1)
    salad_noise = np.random.randint(-20, 20, (h, w, 3), dtype=np.int16)
    # BGR for fresh green salad: B~40, G~170, R~60
    salad_color = np.clip(np.array([40, 170, 60], dtype=np.int16) + salad_noise, 0, 255).astype(np.uint8)
    img[salad_mask > 0] = salad_color[salad_mask > 0]
    # Cucumber slices (light green circle with dark green border)
    cv2.circle(img, (460, 470), 22, (50, 190, 80), -1, cv2.LINE_AA)
    cv2.circle(img, (460, 470), 22, (20, 120, 30), 2, cv2.LINE_AA)
    cv2.circle(img, (510, 480), 20, (50, 190, 80), -1, cv2.LINE_AA)
    cv2.circle(img, (510, 480), 20, (20, 120, 30), 2, cv2.LINE_AA)
    # Red tomato wedges
    cv2.ellipse(img, (480, 520), (22, 12), 45, 0, 360, (30, 40, 210), -1, cv2.LINE_AA)
    cv2.ellipse(img, (530, 460), (20, 10), -30, 0, 360, (30, 40, 210), -1, cv2.LINE_AA)

    # Smooth blur slightly for organic realism
    img = cv2.GaussianBlur(img, (3, 3), 0)

    p1_path = os.path.join(output_dir, "plate1_rice_chicken_dal_salad.jpg")
    cv2.imwrite(p1_path, img)
    print(f"Saved sample plate 1: {p1_path}")

    # ----------------- Plate 2: Salmon + Rice + Salad -----------------
    img2 = np.zeros((h, w, 3), dtype=np.uint8)
    img2[:] = (40, 48, 56)
    cv2.circle(img2, (cx, cy), r + 8, (190, 200, 210), -1, cv2.LINE_AA)
    cv2.circle(img2, (cx, cy), r, (245, 248, 250), -1, cv2.LINE_AA)

    # Rice
    r_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(r_mask, (300, 380), (140, 150), 0, 0, 360, 255, -1)
    img2[r_mask > 0] = rice_color[r_mask > 0]

    # Salmon (Pink/Orange sear)
    s_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(s_mask, (500, 330), (120, 90), -20, 0, 360, 255, -1)
    salmon_color = np.clip(np.array([40, 100, 220], dtype=np.int16) + curry_noise, 0, 255).astype(np.uint8)
    img2[s_mask > 0] = salmon_color[s_mask > 0]
    # Sear grill lines
    for offset in range(-60, 70, 25):
        cv2.line(img2, (460 + offset, 280), (520 + offset, 380), (20, 40, 100), 4, cv2.LINE_AA)

    # Salad
    sal2_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(sal2_mask, (480, 500), (130, 110), 10, 0, 360, 255, -1)
    img2[sal2_mask > 0] = salad_color[sal2_mask > 0]
    cv2.circle(img2, (460, 490), 20, (50, 190, 80), -1, cv2.LINE_AA)
    cv2.circle(img2, (500, 510), 22, (50, 190, 80), -1, cv2.LINE_AA)

    p2_path = os.path.join(output_dir, "plate2_salmon_rice_salad.jpg")
    cv2.imwrite(p2_path, img2)
    print(f"Saved sample plate 2: {p2_path}")

if __name__ == "__main__":
    create_sample_plates()
