from pygeovolume import calc_volume

print(calc_volume("/home/piero/Downloads/grass_example_halfcube/dsm.tif", 
                geojson_polygon="/home/piero/Downloads/grass_example_halfcube/area_file.geojson"))