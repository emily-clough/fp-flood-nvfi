## Filtering the local authority geojson to create a shapefile for grabbing the surface flood risk maps
import geopandas as gpd
import os

# Path to the input GeoJSON file
input_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/LAD_MAY_2025_UK_BFC_V2_481919774574330966.geojson"
# Authorities to filter (case-insensitive)
authorities = ["Kingston upon Hull, City of", "Glasgow City", "Dundee City", "Leicester", "Birmingham", "Tower Hamlets"]
gdf = gpd.read_file(input_path)

bu_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/BUA_2022_GB_2824430073212747649/BUA_2022_GB.shp"
built_up = gpd.read_file(bu_path)
built_up = built_up.to_crs(epsg=4326)

# Filter rows by authority (case-insensitive)
filtered_gdf = gdf[gdf["LAD25NM"].str.lower().isin([a.lower() for a in authorities])]
filtered_gdf = filtered_gdf.to_crs(epsg=4326)  

#filtering out the built up areas in england 
built_up_cities = filtered_gdf.clip(built_up)

print(filtered_gdf) #just checking it isn't empty


# Export to shapefile
localpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/local_authorities.kml"
filtered_gdf.to_file(localpath, driver="KML", index=False)

output_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # <-- This line creates the directory
filtered_gdf.to_file(output_path, driver="ESRI Shapefile")

bukmlpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/built-up.kml"
built_up_cities.to_file(bukmlpath, driver="KML", index=False)

buoutput_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/built_up/built_up.shp"
os.makedirs(os.path.dirname(buoutput_path), exist_ok=True)  # <-- This line creates the directory
built_up_cities.to_file(buoutput_path, driver="ESRI Shapefile")
