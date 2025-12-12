import geopandas as gpd
import pandas as pd
import shapely
import numpy as np
from shapely.ops import transform

import os


#river flood risk
river_flood_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/SEPA_River_Flood_Maps_v3_0/Data/FRM_River_Flood_Hazard_Layers_v3_0.gdb"
scot_river_m = gpd.read_file(river_flood_path, layer='FRM_FH_RIVER_EXTENT_M')
scot_river_h = gpd.read_file(river_flood_path, layer='FRM_FH_RIVER_EXTENT_H')

#sea flood risk
sea_flood_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/SEPA_Coastal_Flood_Maps_v3_0/Data/FRM_Coastal_Flood_Hazard_Layers_v3_0.gdb"
scot_sea_m = gpd.read_file(sea_flood_path, layer='FRM_FH_COASTAL_EXTENT_M')
scot_sea_h = gpd.read_file(sea_flood_path, layer='FRM_FH_COASTAL_EXTENT_H')
#using built-up areas for clipping because scottish cities have a lot of green space 
clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
local_authorities = gpd.read_file(clip_path)


scot_river_sea_h = scot_river_sea_h.to_crs(27700)
scot_river_sea_m = scot_river_sea_m.to_crs(27700)
local_authorities = local_authorities.to_crs(27700)
#putting it all together so that it mirrors english flood data
scot_river_sea_h = pd.concat([scot_river_h, scot_sea_h], ignore_index=True)
scot_river_sea_m = pd.concat([scot_sea_m, scot_river_m], ignore_index=True)

scot_river_sea_h= scot_river_sea_h[["PROB", "geometry"]]
scot_river_sea_m= scot_river_sea_m[["PROB", "geometry"]]

local_scot_river_sea_h = scot_river_sea_h.clip(local_authorities)
local_scot_river_sea_m = scot_river_sea_m.clip(local_authorities)

local_scot_h_plus = local_scot_river_sea_h
local_scot_h_plus.geometry = local_scot_h_plus.buffer(.05)
local_scot_m_clip = local_scot_river_sea_m.overlay(local_scot_h_plus, how='difference')

local_scot_riversea = pd.concat([local_scot_river_sea_h, local_scot_m_clip], ignore_index=True)
local_scot_riversea.geometry = local_scot_riversea.geometry.buffer(0)

local_scot_riversea["PROB"] = local_scot_riversea["PROB"].replace({
    'M': 'Medium Risk of Flooding Rivers & Seas',
    'H': 'High Risk of Flooding Rivers & Seas'
})

local_scot_riversea = local_scot_riversea.to_crs(4326)

#saving the shapefile before simplification so that it can be used in the stage analysis
output_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/scotland-fz/scotland-fz.shp"
os.makedirs(os.path.dirname(output_path), exist_ok=True)  # <-- This line creates the directory
local_scot_riversea.to_file(output_path, driver="ESRI Shapefile")

local_scot_riversea = local_scot_riversea.to_crs(27700)

local_scot_riversea["geometry"] = local_scot_riversea.simplify(tolerance=4, preserve_topology=True)
local_scot_riversea.geometry = local_scot_riversea.buffer(0)


local_scot_riversea = local_scot_riversea.to_crs(4326)

fzpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/flood-zones-scot.kml"
local_scot_riversea.to_file(fzpath, driver="KML", index=False)


##SURFACE FLOOD RISK

#river flood risk
surface_flood_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/SEPA_Surface_Water_Flood_Maps_EXTENT_v3_0/Data/FRM_Surface_Water_Flood_Hazard_EXTENT_Layers_v3_0.gdb"
scot_surface_m = gpd.read_file(surface_flood_path, layer='FRM_FH_SURFACE_WATER_EXTENT_M')
scot_surface_h = gpd.read_file(surface_flood_path, layer='FRM_FH_SURFACE_WATER_EXTENT_H')


#using built-up areas for clipping because scottish cities have a lot of green space 
clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/built_up/built_up.shp"
local_authorities = gpd.read_file(clip_path)


scot_surface_m = scot_surface_m[["PROB", "geometry"]]
scot_surface_h = scot_surface_h[["PROB", "geometry"]]

#note: this is probably unnecessary, as medium risk includes high risk
#but I'm including it anyway for sake of consistency
scot_surface = pd.concat([scot_surface_m, scot_surface_h], ignore_index=True)

local_authorities = local_authorities.to_crs(27700)

glasgow = local_authorities[local_authorities["LAD25NM"] == "Glasgow City"]
dundee = local_authorities[local_authorities["LAD25NM"] == "Dundee City"]

glasgow_surface = scot_surface.clip(glasgow)
dundee_surface = scot_surface.clip(dundee)

#need to split glasgow east/west because it's too big
bounds = glasgow_surface.total_bounds
min_lon = bounds[0]
max_lon = bounds[2]
center_lon = (max_lon- min_lon) / 2.5 + min_lon


glasgow_west = glasgow_surface[glasgow_surface.geometry.centroid.x < center_lon]
glasgow_east = glasgow_surface[glasgow_surface.geometry.centroid.x >= center_lon]

def process_scot_surface(local_scot_surface, tol):

    local_scot_surface = local_scot_surface.to_crs(epsg=27700)
    local_scot_surface = local_scot_surface[["geometry"]]
    local_scot_surface.geometry = local_scot_surface.buffer(1)  
    local_scot_surface = local_scot_surface.dissolve()
    local_scot_surface = local_scot_surface[local_scot_surface.is_valid]
    local_scot_surface = local_scot_surface[~local_scot_surface.is_empty]
    local_scot_surface.geometry = local_scot_surface.buffer(0)


    local_scot_surface.geometry = local_scot_surface.geometry.buffer(0)  
    # simplify (tolerance in metres) - adjust tolerance to taste (e.g. 10m)
    local_scot_surface["geometry"] = local_scot_surface.simplify(tolerance=tol, preserve_topology=True)
    local_scot_surface.geometry = local_scot_surface.geometry.buffer(0)


    local_scot_surface = local_scot_surface.to_crs(4326)

    return local_scot_surface


wglasgow_surface = process_scot_surface(glasgow_west, 4)

gwsurfacepath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/flood-surface-glasgow-west.kml"
wglasgow_surface.to_file(gwsurfacepath, driver="KML", index=False)

eglasgow_surface = process_scot_surface(glasgow_east, 4)

gesurfacepath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/flood-surface-glasgow-east.kml"
eglasgow_surface.to_file(gesurfacepath, driver="KML", index=False)

dundee_surface = process_scot_surface(dundee_surface, .5)

dsurfacepath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/flood-surface-dundee.kml"
dundee_surface.to_file(dsurfacepath, driver="KML", index=False)

