from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastai.learner import load_learner
from fastai.vision.core import PILImage
from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from io import BytesIO

import json
try:
    learn = load_learner("floor_detector2.pkl")
    print("FastAI model loaded successfully.")
except Exception as e:
    print(f"Error loading FastAI model: {e}")
    learn = None
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

geojson_files = ["boxes_part1.geojson", "boxes_part2.geojson"]
all_features = []

for file in geojson_files:
    with open(file, "r") as f:
        data = json.load(f)
        all_features.extend(data["features"])

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if learn is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    image_bytes = await file.read()
    img = PILImage.create(BytesIO(image_bytes)).resize((224, 224))
    pred_class, pred_idx, probs = learn.predict(img)
    return {
        "predicted_class": str(pred_class),
        "class_index": int(pred_idx),
        "probabilities": [float(p) for p in probs]
    }
@app.get("/geojson")
def get_geojson(
    north: float = Query(...),
    south: float = Query(...),
    east: float = Query(...),
    west: float = Query(...)
):
    filtered = []
    for feature in all_features:
        try:
            coords = feature["geometry"]["coordinates"][0]
            lngs = [c[0] for c in coords]
            lats = [c[1] for c in coords]
            if (
                min(lats) <= north and max(lats) >= south and
                min(lngs) <= east and max(lngs) >= west
            ):
                filtered.append(feature)
        except Exception:
            continue

    return JSONResponse({
        "type": "FeatureCollection",
        "features": filtered
    })
