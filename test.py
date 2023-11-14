from pygeovolume import calc_volume

# print(calc_volume("/home/piero/Downloads/grass_example_degen/dsm.tif", 
#                 geojson_polygon="/home/piero/Downloads/grass_example_degen/area_file.geojson"))

# print(calc_volume("/home/piero/Downloads/grass_example/dsm.tif", 
#                 geojson_polygon="/home/piero/Downloads/grass_example/area_file.geojson"))
for method in ["average", "custom", "plane", "triangulate", "highest", "lowest"]:
    print(method, calc_volume(input_dem="/home/piero/Downloads/grass_example_halfcube/dsm.tif", 
                    # geojson_polygon="/home/piero/Downloads/grass_example_halfcube/area_file.geojson",
                    pts=[[-91.994009, 46.84234], [-91.994009, 46.842316], [-91.993973, 46.842316], [-91.993976, 46.84234], [-91.994009, 46.84234]],
                    pts_epsg=4326,
                    base_method=method,
                    custom_base_z=24.35))