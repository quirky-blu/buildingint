from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, HTTPException, File, UploadFile
from io import BytesIO

import json

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

geojson_files = ["boxes_part1.geojson", "boxes_part2.geojson"]
all_features = []

for file in geojson_files:
    with open(file, "r") as f:
        data = json.load(f)
        all_features.extend(data["features"])


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
