import json

def read_polygon(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)

    if data.get('type') == "FeatureCollection":
        features = data.get("features", [{}])
    else:
        features = [data]

    for feature in features:
        if not 'geometry' in feature:
            continue

        # Check if the feature geometry type is Polygon
        if feature['geometry']['type'] == 'Polygon':
            # Extract polygon coordinates
            coordinates = feature['geometry']['coordinates'][0]  # Assuming exterior ring
            return coordinates
    
    raise IOError("No polygons found in %s" % file)