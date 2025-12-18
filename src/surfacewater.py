import geopandas as gpd
import pandas as pd
import shapely
import numpy as np
from shapely.ops import transform
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPolygon

import os

#leicester
leicester_path1 = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/SK/RoFSW_SK50_v202509.gdb"
leicester_surface1 = gpd.read_file(leicester_path1, layer='RoFSW')

leicester_path2 = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/SP/RoFSW_SP55_v202509.gdb"
leicester_surface2 = gpd.read_file(leicester_path2, layer='RoFSW')

leicester_surface = pd.concat([leicester_surface1, leicester_surface2], ignore_index=True)

#birmingham
birmingham_path1 = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/SP/RoFSW_SP05_v202509.gdb"
birmingham_surface1 = gpd.read_file(birmingham_path1, layer='RoFSW')

birmingham_path2 = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/SO/RoFSW_SO55_v202509.gdb"
birmingham_surface2 = gpd.read_file(birmingham_path2, layer='RoFSW')

birmingham_surface = pd.concat([birmingham_surface1, birmingham_surface2], ignore_index=True)

# #hull
hull_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/TA/RoFSW_TA00_v202509.gdb"
hull_surface = gpd.read_file(hull_path, layer='RoFSW')

#tower hamlets
towerhamlets_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/RoFSW/TQ/RoFSW_TQ05_v202509.gdb"
towerhamlets_surface = gpd.read_file(towerhamlets_path, layer='RoFSW')

#concatenating all the england surface water flood risk data
# eng_list = [hull_surface, leicester_surface, birmingham_surface, towerhamlets_surface]
# eng_list = [birmingham_surface]
    #clipping by boundaries of built-up areas in the relevant authorities

clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/built_up/built_up.shp"
local_authorities = gpd.read_file(clip_path)
local_authorities = local_authorities.to_crs(surface.crs)


def process_roswf(surface, local_authorities):

    surface = surface[[ "Risk_band", "geometry" ]]

    #just the high and medium risk bands
    surface = surface[
        surface["Risk_band"].isin(["High", "Medium"])
    ]

    # surface['row_id'] = surface.index.to_series().astype(int)


    # # lfz = lfz.to_crs(epsg=27700)
    # # lfz = lfz[lfz.area > 8000]

    # fz_codes = lfz["row_id"]
    # fz_codes = fz_codes.drop_duplicates()

    # fz_list = fz_codes.astype(int).tolist() if len(fz_codes) > 0 else []
    # flood_by_id = surface[surface["row_id"].isin(fz_list)].copy()

    # lfz = surface.clip(local_authorities)
    surface_local = surface.clip(local_authorities)

    surface_local["geometry"] = surface_local.geometry.apply(lambda g: transform(lambda x, y, z=None: (np.round(x, 0), np.round(y, 0)), g) if g is not None else g)
    surface_local.dropna(inplace=True)


    # connecting adjacent polygons by buffering out and back in
    surface_local = surface_local.to_crs(epsg=27700)
    surface_local.geometry = surface_local.buffer(1)  
    surface_local = surface_local.dissolve()
    surface_local = surface_local[surface_local.is_valid]
    surface_local = surface_local[~surface_local.is_empty]
    surface_local.geometry = surface_local.buffer(0)


    surface_local['geometry'] = surface_local.geometry.apply(
        lambda geom: Polygon(geom.exterior)
        if geom.geom_type == 'Polygon' else (
            MultiPolygon(Polygon(p.exterior) for p in geom.geoms)
            if geom.geom_type == 'MultiPolygon' else geom
        )
    )

    # surface_local["geometry"] = surface_local.simplify(tolerance=10, preserve_topology=True)
    surface_local["geometry"] = surface_local.simplify_coverage(tolerance=12.5, simplify_boundary=True)

    surface_local.geometry = surface_local.buffer(0)
    surface_local = surface_local.to_crs(epsg=4326)

    return surface_local

birm_roswf = process_roswf(birmingham_surface, local_authorities)
print(birm_roswf.head())
#for the rest of the authorities, the simplification tolerance can be set to 5m
leic_roswf = process_roswf(leicester_surface, local_authorities)
print(leic_roswf.head())
hull_roswf = process_roswf(hull_surface, local_authorities)
print(hull_roswf.head())  
th_roswf = process_roswf(towerhamlets_surface, local_authorities)
print(th_roswf.head())

birm_roswf_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/roswf/birm_roswf.kml"
os.makedirs(os.path.dirname(birm_roswf_path), exist_ok=True)  # <-- This line creates the directory
birm_roswf.to_file(birm_roswf_path, driver="kml")


leic_roswf_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/roswf/leic_roswf.kml"
os.makedirs(os.path.dirname(leic_roswf_path), exist_ok=True)  # <-- This line creates the directory
leic_roswf.to_file(leic_roswf_path, driver="kml")


hull_roswf_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/roswf/hull_roswf.kml"
os.makedirs(os.path.dirname(hull_roswf_path), exist_ok=True)  # <-- This line creates the directory
hull_roswf.to_file(hull_roswf_path, driver="kml")

th_roswf_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/roswf/th_roswf.kml"
os.makedirs(os.path.dirname(th_roswf_path), exist_ok=True)  # <-- This line creates the directory
th_roswf.to_file(th_roswf_path, driver="kml")

