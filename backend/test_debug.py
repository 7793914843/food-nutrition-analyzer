import cv2
import numpy as np
from app.food_pipeline import pipeline_instance

img = cv2.imread("app/samples/plate1_rice_chicken_dal_salad.jpg")
h, w, _ = img.shape
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
zones = pipeline_instance._extract_food_zones(img, hsv, lab, np.ones((h, w), dtype=np.uint8))
for i, z in enumerate(zones):
    name, conf = pipeline_instance._classify_food_region(z['crop_bgr'], z['hsv_mean'], z['lab_mean'], z['area_ratio'])
    print(f"Zone {i} ({z['bbox']}): HSV={np.round(z['hsv_mean'], 1)} LAB={np.round(z['lab_mean'], 1)} -> {name} ({conf})")
