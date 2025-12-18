
import geopandas as gpd
import pandas as pd
import shapely
import numpy as np
from shapely.ops import transform

import os



flood_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Flood_Zones_2_3_Rivers_and_Sea.geojson"

flood_risk_sea = gpd.read_file(flood_path)

clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
local_authorities = gpd.read_file(clip_path)


flood_risk_sea['row_id'] = flood_risk_sea.index.to_series().astype(int)

clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
local_authorities = gpd.read_file(clip_path)
local_authorities = local_authorities.to_crs(flood_risk_sea.crs)
lfz = flood_risk_sea.clip(local_authorities)

lfz = lfz.to_crs(epsg=27700)
lfz = lfz[lfz.area > 8000] #this is to filter out those slices where tehre isn't a lot of overlap

fz_codes = lfz["row_id"]
fz_codes = fz_codes.drop_duplicates()

fz_list = fz_codes.astype(int).tolist() if len(fz_codes) > 0 else []
flood_by_id = flood_risk_sea[flood_risk_sea["row_id"].isin(fz_list)].copy()

local_floodzones = flood_by_id[["flood_zone", "geometry"]]
# local_floodzones["geometry"] = local_floodzones.geometry.buffer(0)
# local_floodzones = local_floodzones.dissolve(by="flood_zone")
#committing to shapefile before simplification to avoid topology errors

local_floodzones = local_floodzones.to_crs(epsg=4326)
output_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-fz/filtered-fz.shp"
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # <-- This line creates the directory
local_floodzones.to_file(output_path, driver="ESRI Shapefile")

##now simplifying so that the kml isn't enormous
local_floodzones = local_floodzones.to_crs(epsg=27700)
local_floodzones["geometry"] = local_floodzones.geometry.apply(lambda g: transform(lambda x, y, z=None: (np.round(x, 0), np.round(y, 0)), g) if g is not None else g)
local_floodzones.dropna(inplace=True)

local_floodzones["geometry"] = local_floodzones.simplify(tolerance=5, preserve_topology=True)

#rounding coordinates to reduce file size
# After dissolving, simplifying, and reducing precision

local_floodzones = local_floodzones.to_crs(4326)

local_floodzones.geometry = local_floodzones.buffer(0)

local_floodzones['flood_zone'] = local_floodzones['flood_zone'].replace({
    'FZ2': 'Flood Zone 2 Rivers and Seas',
    'FZ3': 'Flood Zone 3 Rivers and Seas'
})

local_authorities = local_authorities.to_crs(4326)
local_floodzones = local_floodzones.clip(local_authorities)

fzpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/flood-zones-england.kml"
local_floodzones.to_file(fzpath, driver="KML", index=False)
