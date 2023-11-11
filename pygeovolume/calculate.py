import os

def calc_volume(input_dem, pts=None, pts_epsg=None, points_geojson=None):
    if not os.path.isfile(input_dem):
        raise IOError(f"{input_dem} does not exist")
    
    if pts is None and pts_epsg is None and points_geojson is not None:
        # Read GeoJSON points
        pts = []

        return calc_volume(input_dem, pts, 4326)

    return "OK"