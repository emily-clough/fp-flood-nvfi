#bringing in the historic flood maps, filtering by year and outputting to KML
#this is for England only

import geopandas as gpd
import pandas as pd
import shapely
import numpy as np
from shapely.ops import transform

import os


flood_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Recorded_Flood_Outlines.shp/Recorded_Flood_Outlines.shp"
flood = gpd.read_file(flood_path)

#print(flood.head())

#flood.plot(figsize=(8,8))

print(flood["start_date"].dtype)

flood["start_ts"] = pd.to_datetime(flood["start_date"], errors="coerce")   # converts strings, handles NaT
flood["start_year"] = flood["start_ts"].dt.year.astype("Int64")
flood = flood.to_crs(epsg=4326)

# print(flood.head())
# print(flood.columns)
flood_2015 = flood[["start_year", "rec_out_id", "geometry"]]
flood_2015 =  flood_2015[flood_2015["start_year"] >= 2000] 


clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
local_authorities = gpd.read_file(clip_path)

local_authorities = local_authorities.to_crs(flood_2015.crs)

flood_2015clipped = gpd.clip(flood_2015, local_authorities)

hf_codes = flood_2015clipped["rec_out_id"]
hf_codes = hf_codes.drop_duplicates()

hf_list = hf_codes.astype(int).tolist() if len(hf_codes) > 0 else []
flood_2015_local = flood_2015[flood_2015["rec_out_id"].isin(hf_codes)].copy()


# reproject to a metric CRS for simplification (British National Grid)
flood_2015_local = flood_2015_local.to_crs(epsg=27700)

# simplify (tolerance in metres) - adjust tolerance to taste (e.g. 10m)
flood_2015_local["geometry"] = flood_2015_local.simplify(tolerance=10, preserve_topology=True)

#rounding coordinates to reduce file size
# After dissolving, simplifying, and reducing precision
flood_2015_local["geometry"] = flood_2015_local.geometry.apply(lambda g: transform(lambda x, y, z=None: (np.round(x, 5), np.round(y, 5)), g) if g is not None else g)
flood_2015_local.dropna(inplace=True)


flood_2015_local['name'] = flood_2015_local['start_year'].apply(lambda x: f'Historic Flooding {x}')
flood_2015_local = flood_2015_local[["name", "geometry"]]

local_authorities = local_authorities.to_crs(epsg=27700)
local_plus10 = local_authorities.copy()
local_plus10.geometry = local_plus10.geometry.buffer(500)

flood_2015_local = flood_2015_local.clip(local_plus10)

flood_2015_local = flood_2015_local.to_crs(4326)

# flood_2015_local.geometry = flood_2015_local.buffer(0)

flood_2015_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/flood_2000.kml"
flood_2015_local.to_file(flood_2015_path, driver="kml")
