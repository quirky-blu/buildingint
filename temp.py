import json

# Load the original GeoJSON
with open("boxes_updated.geojson", "r") as f:
    data = json.load(f)

features = data["features"]
midpoint = len(features) // 2

# Split into two parts
part1 = {
    "type": "FeatureCollection",
    "features": features[:midpoint]
}

part2 = {
    "type": "FeatureCollection",
    "features": features[midpoint:]
}

# Save the parts
with open("boxes_part1.geojson", "w") as f1:
    json.dump(part1, f1, indent=2)

with open("boxes_part2.geojson", "w") as f2:
    json.dump(part2, f2, indent=2)

print("GeoJSON split into boxes_part1.geojson and boxes_part2.geojson.")
