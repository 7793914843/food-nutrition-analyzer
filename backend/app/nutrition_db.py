"""
Comprehensive Nutrition Database (USDA FoodData Central + IFCT)
Provides nutritional values per 100g and helper functions for portion calculation.
"""

from typing import Dict, Any, List, Optional
import re

# Comprehensive nutritional profiles per 100g
# Values: calories (kcal), protein (g), carbs (g), fat (g), fiber (g), density (g/cm^3), typical portion (g)
NUTRITION_DATABASE: Dict[str, Dict[str, Any]] = {
    # ------------------ INDIAN FOODS ------------------
    "rice": {
        "name": "White Rice (Steamed)",
        "calories": 130.0,
        "protein": 2.7,
        "carbs": 28.2,
        "fat": 0.3,
        "fiber": 0.4,
        "density": 1.0,
        "typical_portion_g": 180,
        "emoji": "🍚",
        "keywords": ["rice", "white rice", "steamed rice", "boiled rice", "chawal", "bhat", "plain rice"]
    },
    "biryani": {
        "name": "Biryani",
        "calories": 185.0,
        "protein": 9.5,
        "carbs": 23.5,
        "fat": 6.5,
        "fiber": 1.4,
        "density": 1.05,
        "typical_portion_g": 250,
        "emoji": "🍲",
        "keywords": ["biryani", "chicken biryani", "mutton biryani", "veg biryani", "hyderabadi biryani"]
    },
    "dal": {
        "name": "Dal (Yellow Lentils / Tadka)",
        "calories": 115.0,
        "protein": 7.0,
        "carbs": 16.5,
        "fat": 2.8,
        "fiber": 4.0,
        "density": 1.02,
        "typical_portion_g": 140,
        "emoji": "🥣",
        "keywords": ["dal", "dal tadka", "dal fry", "yellow dal", "toor dal", "moong dal", "lentils", "dhal", "daal"]
    },
    "roti": {
        "name": "Roti / Chapati (Whole Wheat)",
        "calories": 260.0,
        "protein": 9.0,
        "carbs": 52.0,
        "fat": 3.0,
        "fiber": 7.5,
        "density": 0.65,
        "typical_portion_g": 80, # 2 rotis
        "emoji": "🫓",
        "keywords": ["roti", "chapati", "phulka", "whole wheat flatbread", "rotis", "chapatis"]
    },
    "chicken_curry": {
        "name": "Chicken Curry",
        "calories": 165.0,
        "protein": 15.2,
        "carbs": 4.2,
        "fat": 9.8,
        "fiber": 1.1,
        "density": 1.05,
        "typical_portion_g": 160,
        "emoji": "🍗",
        "keywords": ["chicken curry", "chicken gravy", "murgh curry", "chicken masala", "kori gassi", "chicken korma"]
    },
    "paneer_curry": {
        "name": "Paneer Curry (Butter Masala)",
        "calories": 210.0,
        "protein": 9.2,
        "carbs": 8.5,
        "fat": 15.8,
        "fiber": 1.8,
        "density": 1.05,
        "typical_portion_g": 160,
        "emoji": "🧀",
        "keywords": ["paneer curry", "paneer butter masala", "shahi paneer", "kadai paneer", "matar paneer", "paneer"]
    },
    "sambar": {
        "name": "Sambar",
        "calories": 75.0,
        "protein": 3.4,
        "carbs": 12.0,
        "fat": 1.6,
        "fiber": 3.0,
        "density": 1.0,
        "typical_portion_g": 150,
        "emoji": "🍲",
        "keywords": ["sambar", "sambhar", "south indian sambar"]
    },
    "idli": {
        "name": "Idli (Steamed)",
        "calories": 130.0,
        "protein": 4.0,
        "carbs": 26.5,
        "fat": 0.5,
        "fiber": 1.5,
        "density": 0.8,
        "typical_portion_g": 100, # 2 idlis
        "emoji": "⚪",
        "keywords": ["idli", "idlis", "steamed idli"]
    },
    "dosa": {
        "name": "Dosa / Masala Dosa",
        "calories": 170.0,
        "protein": 4.2,
        "carbs": 28.5,
        "fat": 4.8,
        "fiber": 2.0,
        "density": 0.7,
        "typical_portion_g": 130,
        "emoji": "🥞",
        "keywords": ["dosa", "masala dosa", "plain dosa", "crispy dosa"]
    },
    "upma": {
        "name": "Upma (Rava Savory Porridge)",
        "calories": 135.0,
        "protein": 3.5,
        "carbs": 24.0,
        "fat": 3.2,
        "fiber": 1.8,
        "density": 0.85,
        "typical_portion_g": 150,
        "emoji": "🥣",
        "keywords": ["upma", "rava upma", "sooji upma"]
    },
    "poha": {
        "name": "Poha (Flattened Rice)",
        "calories": 140.0,
        "protein": 3.0,
        "carbs": 26.0,
        "fat": 3.0,
        "fiber": 1.5,
        "density": 0.8,
        "typical_portion_g": 150,
        "emoji": "🥣",
        "keywords": ["poha", "kanda poha", "flattened rice", "aval"]
    },
    "salad": {
        "name": "Fresh Salad (Greens, Cucumber, Tomato)",
        "calories": 35.0,
        "protein": 1.5,
        "carbs": 5.8,
        "fat": 0.6,
        "fiber": 2.6,
        "density": 0.4,
        "typical_portion_g": 90,
        "emoji": "🥗",
        "keywords": ["salad", "green salad", "garden salad", "cucumber salad", "fresh salad", "sliced salad", "kachumber"]
    },

    # ------------------ COMMON GLOBAL FOODS ------------------
    "pizza": {
        "name": "Pizza (Margherita / Cheese)",
        "calories": 266.0,
        "protein": 11.2,
        "carbs": 33.0,
        "fat": 10.1,
        "fiber": 2.3,
        "density": 0.75,
        "typical_portion_g": 180,
        "emoji": "🍕",
        "keywords": ["pizza", "cheese pizza", "margherita pizza", "pepperoni pizza", "slice of pizza"]
    },
    "burger": {
        "name": "Burger / Cheeseburger",
        "calories": 250.0,
        "protein": 13.0,
        "carbs": 24.5,
        "fat": 12.0,
        "fiber": 1.6,
        "density": 0.7,
        "typical_portion_g": 180,
        "emoji": "🍔",
        "keywords": ["burger", "cheeseburger", "veggie burger", "chicken burger", "hamburger"]
    },
    "pasta": {
        "name": "Pasta (Tomato / Arrabiata)",
        "calories": 160.0,
        "protein": 5.8,
        "carbs": 31.0,
        "fat": 1.8,
        "fiber": 2.0,
        "density": 0.9,
        "typical_portion_g": 200,
        "emoji": "🍝",
        "keywords": ["pasta", "spaghetti", "penne", "macaroni", "lasagna", "fettuccine"]
    },
    "sandwich": {
        "name": "Sandwich / Club Sandwich",
        "calories": 230.0,
        "protein": 10.2,
        "carbs": 28.0,
        "fat": 9.2,
        "fiber": 2.2,
        "density": 0.65,
        "typical_portion_g": 160,
        "emoji": "🥪",
        "keywords": ["sandwich", "club sandwich", "grilled sandwich", "veg sandwich", "toast"]
    },
    "french_fries": {
        "name": "French Fries",
        "calories": 312.0,
        "protein": 3.4,
        "carbs": 41.0,
        "fat": 15.0,
        "fiber": 3.8,
        "density": 0.6,
        "typical_portion_g": 120,
        "emoji": "🍟",
        "keywords": ["french fries", "fries", "potato wedges", "chips"]
    },
    "fried_chicken": {
        "name": "Fried Chicken",
        "calories": 260.0,
        "protein": 22.0,
        "carbs": 8.0,
        "fat": 16.0,
        "fiber": 0.5,
        "density": 1.0,
        "typical_portion_g": 150,
        "emoji": "🍗",
        "keywords": ["fried chicken", "crispy chicken", "chicken wings", "chicken tenders"]
    },
    "eggs": {
        "name": "Eggs (Boiled / Scrambled / Omelette)",
        "calories": 155.0,
        "protein": 13.0,
        "carbs": 1.1,
        "fat": 11.0,
        "fiber": 0.0,
        "density": 1.0,
        "typical_portion_g": 100,
        "emoji": "🍳",
        "keywords": ["egg", "eggs", "boiled egg", "scrambled eggs", "omelette", "fried egg"]
    },
    "banana": {
        "name": "Banana",
        "calories": 89.0,
        "protein": 1.1,
        "carbs": 22.8,
        "fat": 0.3,
        "fiber": 2.6,
        "density": 0.9,
        "typical_portion_g": 120,
        "emoji": "🍌",
        "keywords": ["banana", "yellow banana"]
    },
    "apple": {
        "name": "Apple",
        "calories": 52.0,
        "protein": 0.3,
        "carbs": 13.8,
        "fat": 0.2,
        "fiber": 2.4,
        "density": 0.85,
        "typical_portion_g": 150,
        "emoji": "🍎",
        "keywords": ["apple", "red apple", "green apple"]
    }
}

# Candidate target classes for Food Classifier
CANDIDATE_FOOD_LABELS = [
    # Indian
    "steamed white rice",
    "chicken biryani",
    "yellow dal tadka",
    "whole wheat roti chapati",
    "spicy chicken curry",
    "paneer butter masala curry",
    "sambar lentil stew",
    "steamed idli",
    "crispy dosa",
    "semolina upma",
    "flattened rice poha",
    "fresh cucumber and tomato salad",
    # Global
    "slice of cheese pizza",
    "beef or chicken burger",
    "pasta with tomato sauce",
    "grilled sandwich",
    "crispy french fries",
    "fried chicken pieces",
    "boiled or scrambled eggs",
    "fresh ripe banana",
    "fresh red apple"
]

# Mapping candidate label phrases to canonical database keys
LABEL_TO_KEY = {
    "steamed white rice": "rice",
    "chicken biryani": "biryani",
    "yellow dal tadka": "dal",
    "whole wheat roti chapati": "roti",
    "spicy chicken curry": "chicken_curry",
    "paneer butter masala curry": "paneer_curry",
    "sambar lentil stew": "sambar",
    "steamed idli": "idli",
    "crispy dosa": "dosa",
    "semolina upma": "upma",
    "flattened rice poha": "poha",
    "fresh cucumber and tomato salad": "salad",
    "slice of cheese pizza": "pizza",
    "beef or chicken burger": "burger",
    "pasta with tomato sauce": "pasta",
    "grilled sandwich": "sandwich",
    "crispy french fries": "french_fries",
    "fried chicken pieces": "fried_chicken",
    "boiled or scrambled eggs": "eggs",
    "fresh ripe banana": "banana",
    "fresh red apple": "apple"
}


def lookup_nutrition(food_name: str) -> Dict[str, Any]:
    """
    Finds nutrition profile by key or keyword.
    """
    clean_name = food_name.lower().strip()
    clean_name = re.sub(r'[^a-z0-9\s]', ' ', clean_name)

    if clean_name in NUTRITION_DATABASE:
        return NUTRITION_DATABASE[clean_name]

    for key, data in NUTRITION_DATABASE.items():
        for kw in data.get("keywords", []):
            if kw == clean_name or kw in clean_name or clean_name in kw:
                return data

    words = clean_name.split()
    best_match = None
    best_score = 0
    for key, data in NUTRITION_DATABASE.items():
        score = 0
        all_kws = " ".join(data.get("keywords", [])) + " " + data["name"].lower()
        for word in words:
            if len(word) >= 3 and word in all_kws:
                score += 1
        if score > best_score:
            best_score = score
            best_match = data

    if best_match and best_score > 0:
        return best_match

    return {
        "name": food_name.title(),
        "calories": 140.0,
        "protein": 5.0,
        "carbs": 20.0,
        "fat": 5.0,
        "fiber": 2.0,
        "density": 0.8,
        "typical_portion_g": 150,
        "emoji": "🍽️"
    }


def calculate_dish_nutrition(dish_name: str, grams: float) -> Dict[str, Any]:
    profile = lookup_nutrition(dish_name)
    factor = grams / 100.0

    return {
        "dish": profile["name"],
        "key": profile.get("key", dish_name),
        "emoji": profile.get("emoji", "🍽️"),
        "quantity_g": round(grams, 0),
        "calories": round(profile["calories"] * factor, 1),
        "protein": round(profile["protein"] * factor, 1),
        "carbs": round(profile["carbs"] * factor, 1),
        "fat": round(profile["fat"] * factor, 1),
        "fiber": round(profile["fiber"] * factor, 1),
        "per_100g": {
            "calories": profile["calories"],
            "protein": profile["protein"],
            "carbs": profile["carbs"],
            "fat": profile["fat"],
            "fiber": profile["fiber"]
        }
    }


def calculate_plate_totals(dishes_nutrition: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_grams = round(sum(d["quantity_g"] for d in dishes_nutrition), 1)
    total_calories = round(sum(d["calories"] for d in dishes_nutrition), 1)
    total_protein = round(sum(d["protein"] for d in dishes_nutrition), 1)
    total_carbs = round(sum(d["carbs"] for d in dishes_nutrition), 1)
    total_fat = round(sum(d["fat"] for d in dishes_nutrition), 1)
    total_fiber = round(sum(d["fiber"] for d in dishes_nutrition), 1)

    return {
        "total_weight_g": total_grams,
        "total_calories": total_calories,
        "total_protein": total_protein,
        "total_carbs": total_carbs,
        "total_fat": total_fat,
        "total_fiber": total_fiber
    }
