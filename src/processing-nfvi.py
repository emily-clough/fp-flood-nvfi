import re

import geopandas as gpd
import pandas as pd
import os
import shapely
import numpy as np
from shapely.ops import transform


inpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx"
df = pd.read_excel(inpath, sheet_name="Indices - Integrated", skiprows=5, usecols='C, E, I', engine = "openpyxl" )
df.columns = ['zone_code', 'nfvi-national', 'nfvi-uk']


def clip_authorities(authort, code_var, name_var, nfvi, zones):
    pattern = r"|".join(fr"\b{re.escape(x)}\b" for x in authort)

    # boolean mask (case-insensitive). na=False avoids matching NaNs.
    mask = zones[name_var].astype(str).str.contains(pattern, case=False, na=False)

    # filtered GeoDataFrame
    zones = zones[mask].copy()

    zones = zones.rename(columns={code_var: "zone_code"})
    zones = zones.to_crs(epsg=4326)

    gbnfvi = zones.merge(nfvi, on='zone_code', how='left')
    gbnfvi = gbnfvi[["geometry", "nfvi-uk"]]
    #makes the geometries simpler for sending out kml
    #rounding coordinates 
    gbnfvi["geometry"] = gbnfvi.geometry.apply(lambda g: transform(lambda x, y, z=None: (np.round(x, 5), np.round(y, 5)), g) if g is not None else g)
    gbnfvi.dropna(inplace=True)

    gbnfvi["geometry"] = gbnfvi.simplify(tolerance=.00001, preserve_topology=True)

    conditions = [
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= 2.5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= 1.5) & (gbnfvi["nfvi-uk"] < 2.5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= .5) & (gbnfvi["nfvi-uk"] < 1.5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= -.5) & (gbnfvi["nfvi-uk"] < .5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= -1.5) & (gbnfvi["nfvi-uk"] < -.5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] >= -2.5) & (gbnfvi["nfvi-uk"] < -1.5),
        gbnfvi["nfvi-uk"].notna() & (gbnfvi["nfvi-uk"] <= -2.5), 

    ]
    labels = ["Acute Vulnerability", "Extremely High Vulnerability", "Relatively High Vulnerability", "Average Vulnerability",  "Relatively Low Vulnerability", "Extremely Low Vulnerability", "Slight Vulnerability"]
    gbnfvi["Name"] = np.select(conditions, labels, default=pd.NA)
    return gbnfvi




##English
lsoa_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Lower_layer_Super_Output_Areas_December_2021_Boundaries_EW_BFC_V10_-3788374532542394575.geojson"
lsoa = gpd.read_file(lsoa_path)

english_authorities = ["Kingston upon Hull", "Leicester", "Birmingham", "Tower Hamlets"]

eng_nfvi = clip_authorities(english_authorities,"LSOA21CD", "LSOA21NM", df, lsoa)
print(eng_nfvi.head())
eng_vuln = eng_nfvi[eng_nfvi["nfvi-uk"]>=.5]
eng_lessvuln = eng_nfvi[eng_nfvi["nfvi-uk"]<.5]

ev_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/eng-vuln.kml"
eng_vuln.to_file(ev_path, driver="KML", index=False)

elv_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/england/eng-lessvuln.kml"
eng_lessvuln.to_file(elv_path, driver="KML", index=False)



nfvie_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/nfvi-eng/nfvi-eng.shp"
os.makedirs(os.path.dirname(nfvie_path), exist_ok=True)  # <-- This line creates the directory
eng_vuln.to_file(nfvie_path, driver="ESRI Shapefile")

##scottish
inter_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/SG_IntermediateZoneBdry_2011/SG_IntermediateZone_Bdry_2011.shp"
inter = gpd.read_file(inter_path)

inter = inter.to_crs(4326)

##for scotland, we first need to make the list of relevant intermediate zones from the clipped authorities, because scotland doesn't have authority names in the data file
clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
local_authorities = gpd.read_file(clip_path)

#trying to take out the bitsy bits
clipped_authorities = gpd.clip(inter, local_authorities)
clipped_authorities = clipped_authorities.to_crs(epsg=27700)
clipped_authorities = clipped_authorities[clipped_authorities.area > 8000]

scot_codes = clipped_authorities["InterZone"]
scot_codes = scot_codes.drop_duplicates()

scot_nfvi = clip_authorities(scot_codes,"InterZone", "InterZone", df, inter)

scot_vuln = scot_nfvi[scot_nfvi["nfvi-uk"]>=.5]
scot_lessvuln = scot_nfvi[scot_nfvi["nfvi-uk"]<.5]

sv_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/scot-vuln.kml"
scot_vuln.to_file(sv_path, driver="KML", index=False)

slv_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/scotland/scot-lessvuln.kml"
scot_lessvuln.to_file(slv_path, driver="KML", index=False)


nfvis_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/nfvi-scot/nfvi-scot.shp"
os.makedirs(os.path.dirname(nfvis_path), exist_ok=True)  # <-- This line creates the directory
scot_vuln.to_file(nfvis_path, driver="ESRI Shapefile")
