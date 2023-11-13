import os
import rasterio
from pyproj import CRS, Transformer
from .geojson import read_polygon

def calc_volume(input_dem, pts=None, pts_epsg=None, geojson_polygon=None):
    if not os.path.isfile(input_dem):
        raise IOError(f"{input_dem} does not exist")

    crs = None
    with rasterio.open(input_dem) as d:
        if d.crs is None:
            raise IOError(f"{input_dem} does not have a CRS")
        crs = CRS.from_epsg(d.crs.to_epsg())
    
    if pts is None and pts_epsg is None and geojson_polygon is not None:
        # Read GeoJSON points
        pts = read_polygon(geojson_polygon)
        
        # Convert to DEM crs
        transformer = Transformer.from_crs(
            CRS.from_epsg(4326),
            crs
        )

        trans_pts = [transformer.transform(p[1], p[0]) for p in pts]
        return calc_volume(input_dem, trans_pts, 4326)

    buffer = 0
    with rasterio.open(input_dem) as d:
        # Convert input points to pixel coordinates
        pixel_coords = [d.index(*p) for p in pts]
        
        # Determine the window bounds
        min_y = max(0, min(coord[0] for coord in pixel_coords) - buffer)
        min_x = max(0, min(coord[1] for coord in pixel_coords) - buffer)
        max_y = min(d.width, max(coord[0] for coord in pixel_coords) + buffer)
        max_x = min(d.height, max(coord[1] for coord in pixel_coords) + buffer)

        w = rasterio.windows.Window.from_slices((min_y, max_y), (min_x, max_x))
        transform = d.window_transform(w)

        rast = d.read(1, window=w)

        print(min_x, min_y, max_x, max_y)
        print(rast)

        with rasterio.open(input_dem + "out.tif", "w", width=w.width, height=w.height, dtype=rast.dtype, count=1, transform=transform) as out:
            out.write(rast, 1)
    return "OK"