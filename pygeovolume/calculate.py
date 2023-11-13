import os
import rasterio
import rasterio.mask
from pyproj import CRS, Transformer
from scipy.interpolate import griddata
import numpy as np
import json


def calc_volume(input_dem, pts=None, pts_epsg=None, geojson_polygon=None,
                interp_method='cubic', decimals=4):
    if not os.path.isfile(input_dem):
        raise ValueError(f"{input_dem} does not exist")

    crs = None
    with rasterio.open(input_dem) as d:
        if d.crs is None:
            raise ValueError(f"{input_dem} does not have a CRS")
        crs = CRS.from_epsg(d.crs.to_epsg())
    
    if pts is None and pts_epsg is None and geojson_polygon is not None:
        # Read GeoJSON points
        pts = read_polygon(geojson_polygon)
        return calc_volume(input_dem, pts=pts, pts_epsg=4326)
    
    # Convert to DEM crs
    transformer = Transformer.from_crs(
        CRS.from_epsg(pts_epsg),
        crs
    )
    dem_pts = [transformer.transform(p[1], p[0]) for p in pts]
    
    # Some checks
    if len(dem_pts) < 2:
        raise ValueError("Insufficient points to form a polygon")

    # Close loop if needed
    if not np.array_equal(dem_pts[0], dem_pts[-1]):
        dem_pts.append(dem_pts[0])
    
    dem_pts = np.array(dem_pts)

    polygon = {"coordinates": [dem_pts], "type": "Polygon"}

    # Remove last point (loop close)
    dem_pts = dem_pts[:-1]
    
    with rasterio.open(input_dem) as d:
        px_w = d.transform[0]
        px_h = d.transform[4]

        # Area of a pixel in square units
        px_area = abs(px_w * px_h)

        rast_dem, transform = rasterio.mask.mask(d, [polygon], crop=True, all_touched=True, indexes=1, nodata=np.nan)
        h, w = rast_dem.shape

        # X/Y coordinates in transform coordinates
        ys, xs = np.array(rasterio.transform.rowcol(transform, dem_pts[:,0], dem_pts[:,1]))
        zs = rast_dem[ys,xs]

        if np.any(xs<0) or np.any(xs>=w) or np.any(ys<0) or np.any(ys>=h):
            raise ValueError("Points are out of bounds")
        
        # Create a grid for interpolation
        x_grid, y_grid = np.meshgrid(np.linspace(0, w - 1, w), np.linspace(0, h - 1, h))

        # Perform spline interpolation using griddata
        base = np.round(griddata(np.column_stack((xs, ys)), zs, (x_grid, y_grid), method=interp_method), decimals=9)

        # Calculate volume
        diff = rast_dem - base
        volume = np.nansum(diff) * px_area

        # import matplotlib.pyplot as plt
        # fig, ax = plt.subplots()
        # ax.imshow(diff)
        # plt.scatter(xs, ys, c=zs, cmap='viridis', s=50, edgecolors='k')
        # plt.colorbar(label='Z values')
        # plt.title('Debug')
        # plt.show()

        return np.round(volume, decimals=decimals)


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