"""
Unit test script for HybridFoodPipeline
"""

import os
import json
from app.food_pipeline import pipeline_instance

def test_analysis():
    sample_path = "app/samples/plate1_rice_chicken_dal_salad.jpg" if os.path.exists("app/samples/plate1_rice_chicken_dal_salad.jpg") else "backend/app/samples/plate1_rice_chicken_dal_salad.jpg"
    print(f"Testing hybrid analysis on: {sample_path}")
    with open(sample_path, "rb") as f:
        img_bytes = f.read()

    result = pipeline_instance.analyze_plate(img_bytes, filename="plate1_rice_chicken_dal_salad.jpg")
    print("\n--- HYBRID ANALYSIS RESULT ---")
    print(f"Success: {result['success']}")
    print(f"Detected dishes count: {len(result['detected_dishes'])}")
    for i, dish in enumerate(result['detected_dishes'], 1):
        print(f"\n{i}. {dish['name']} (Confidence: {dish['confidence']}%) - {dish['quantity_g']}g [Low Confidence: {dish['is_low_confidence']}]")
        print(f"   Top 3 predictions:")
        for rank, pred in enumerate(dish['top3_predictions'], 1):
            print(f"     {rank}. {pred['name']} — {pred['confidence']}%")
        print(f"   Nutrition: {dish['calories']} kcal | P: {dish['protein']}g | C: {dish['carbs']}g | F: {dish['fat']}g | Fib: {dish['fiber']}g")

    print("\n--- TOTAL NUTRITION OF THE PLATE ---")
    totals = result['total_nutrition']
    print(f"Total Weight: {totals['total_weight_g']} g")
    print(f"Total Calories: {totals['total_calories']} kcal")
    print(f"Total Protein: {totals['total_protein']} g")
    print(f"Total Carbohydrates: {totals['total_carbs']} g")
    print(f"Total Fat: {totals['total_fat']} g")
    print(f"Total Fiber: {totals['total_fiber']} g")

if __name__ == "__main__":
    test_analysis()
