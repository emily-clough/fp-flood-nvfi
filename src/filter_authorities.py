## Filtering the local authority geojson to create a shapefile for grabbing the surface flood risk maps
import geopandas as gpd
import os

# Path to the input GeoJSON file
input_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/LAD_MAY_2025_UK_BFC_V2_481919774574330966.geojson"

# Authorities to filter (case-insensitive)
authorities = ["Kingston upon Hull, City of", "Glasgow City", "Dundee City", "Leicester", "Birmingham"]

# Read the GeoJSON file
gdf = gpd.read_file(input_path)

# Filter rows by authority (case-insensitive)
filtered_gdf = gdf[gdf["LAD25NM"].str.lower().isin([a.lower() for a in authorities])]

print(filtered_gdf) #just checking it isn't empty


# Export to shapefile
output_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # <-- This line creates the directory

print(f"Saving to: {output_path}")
print(f"Filtered rows: {len(filtered_gdf)}")

filtered_gdf.to_file(output_path, driver="ESRI Shapefile")