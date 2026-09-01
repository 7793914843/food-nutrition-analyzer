"""
FastAPI Backend for Food Nutrition Detector with Hybrid Recognition & Recalculation.
"""

import os
import io
import base64
import logging
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.food_pipeline import pipeline_instance
from app.nutrition_db import (
    NUTRITION_DATABASE,
    lookup_nutrition,
    calculate_dish_nutrition,
    calculate_plate_totals
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("food_api")

app = FastAPI(
    title="Food Nutrition Detector API",
    description="Hybrid AI Food Recognition Pipeline with Crop Classification & Nutrition Estimation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")


class RecalculateItem(BaseModel):
    id: str
    key: str
    quantity_g: float


class RecalculateRequest(BaseModel):
    items: List[RecalculateItem]


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Hybrid AI Food Nutrition Detector",
        "endpoints": {
            "analyze": "POST /api/analyze-food",
            "recalculate": "POST /api/recalculate-nutrition",
            "samples": "GET /api/sample-images"
        }
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "yolo_loaded": pipeline_instance.yolo_model is not None,
        "vit_loaded": pipeline_instance.vit_classifier is not None,
        "clip_loaded": pipeline_instance.clip_classifier is not None,
        "database_count": len(NUTRITION_DATABASE)
    }


@app.get("/api/food-classes")
def get_all_food_classes():
    """
    Returns available dish options for manual correction dropdowns.
    """
    options = []
    for key, val in NUTRITION_DATABASE.items():
        options.append({
            "key": key,
            "name": val["name"],
            "emoji": val.get("emoji", "🍽️"),
            "calories_per_100g": val["calories"],
            "typical_portion_g": val.get("typical_portion_g", 140)
        })
    return {"options": options}


@app.get("/api/sample-images")
def get_sample_images():
    samples = [
        {
            "id": "plate1_rice_chicken_dal_salad",
            "title": "Rice + Chicken Curry + Dal + Salad",
            "filename": "plate1_rice_chicken_dal_salad.jpg"
        },
        {
            "id": "plate2_salmon_rice_salad",
            "title": "Grilled Salmon + Rice + Salad",
            "filename": "plate2_salmon_rice_salad.jpg"
        }
    ]

    for s in samples:
        filepath = os.path.join(SAMPLES_DIR, s["filename"])
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                s["data_url"] = f"data:image/jpeg;base64,{b64}"
        else:
            s["data_url"] = None

    return {"samples": samples}


@app.post("/api/analyze-food")
async def analyze_food(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None)
):
    try:
        image_bytes = None
        filename = "plate.jpg"

        if file is not None:
            image_bytes = await file.read()
            filename = file.filename or "plate.jpg"
        elif sample_id:
            sample_path = os.path.join(SAMPLES_DIR, f"{sample_id}.jpg")
            if not os.path.exists(sample_path):
                sample_path = os.path.join(SAMPLES_DIR, sample_id)
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    image_bytes = f.read()
                filename = os.path.basename(sample_path)
            else:
                raise HTTPException(status_code=404, detail=f"Sample '{sample_id}' not found.")
        else:
            raise HTTPException(status_code=400, detail="Please upload an image file.")

        if not image_bytes or len(image_bytes) < 100:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        result = pipeline_instance.analyze_plate(image_bytes, filename=filename)
        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing plate: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/recalculate-nutrition")
def recalculate_nutrition(req: RecalculateRequest):
    """
    Live recalculates per-dish and total nutrition when user edits dish or portion size.
    """
    dishes_nutrition = []
    for item in req.items:
        nutr = calculate_dish_nutrition(item.key, item.quantity_g)
        nutr["id"] = item.id
        dishes_nutrition.append(nutr)

    totals = calculate_plate_totals(dishes_nutrition)
    return {
        "dishes_nutrition": dishes_nutrition,
        "total_nutrition": totals
    }
