#this file is to process the NFVI data--pull it in and match it to the relevant LSOA


import pandas as pd
import geopandas
import simplekml
import shapely
import numpy as np


from shapely.ops import unary_union, polygonize
from shapely.geometry import Polygon, MultiPolygon


#extracting the relevant sheet from nvfi file

inpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx"

df = pd.read_excel(inpath, sheet_name="Indices - Integrated", skiprows=5, usecols='C, E, I', engine = "openpyxl" )

df.columns = ['zone_code', 'nfvi-national', 'nfvi-uk']
print(df.columns)

#pulling in LSOA geojson
lsoa_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/LSOA_Dec_2001_EW_BFC_2022_1969373978000391918.geojson"
lsoa = geopandas.read_file(lsoa_path)

inter_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/SG_IntermediateZoneBdry_2011/SG_IntermediateZone_Bdry_2011.shp"
inter = geopandas.read_file(inter_path)

#reprojecting scottish data to english CRS
inter = inter.to_crs(lsoa.crs)

inter = inter.rename(columns={"InterZone": "zone_code", "Name": "zone_name"})
lsoa = lsoa.rename(columns={"LSOA01CD": "zone_code", "LSOA01NM": "zone_name"})

inter["nation"] = "Scotland"
lsoa["nation"] = "England"

scot_eng = geopandas.GeoDataFrame(
    pd.concat([inter, lsoa], ignore_index=True),
    crs=lsoa.crs
)

gb = scot_eng[["zone_code", "geometry", "nation"]]
#print(scot_eng.columns)

gbnfvi = gb.merge(df, on='zone_code', how='left')

#trying to clean up so that the geometry works for kml export
gbnfvi["geometry"] = gbnfvi.buffer(0)
gbnfvi = gbnfvi.explode(index_parts=False, ignore_index=True)


#pulling out the vulnerable bits
gb_vuln =  gbnfvi[gbnfvi["nfvi-uk"] < -.15] #should be .27, changing in order to test--at .27 the file is too big
gb_vuln = gb_vuln[["geometry", "nfvi-uk"]]

print(gb_vuln['nfvi-uk'].quantile([0.25, 0.5, 0.75,1]))
#.25: -1.035, .5: -.609, .75: -.273, 1: 0



#gb_vuln.plot(figsize=(8,8))
#gb.plot(figsize=(8,8))

clip_path = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/processing/filtered-authorities/filtered-authorities.shp"
clip = geopandas.read_file(clip_path)

##GPT defined functions for cleaning and clipping these geographies
def report_geoms(gdf, name="gdf"):
    print(f"--- {name} ---")
    print("rows:", len(gdf))
    print("null geometries:", int(gdf.geometry.isnull().sum()))
    print("empty geometries:", int(gdf.geometry.is_empty.sum()))
    print("invalid geometries:", int((~gdf.geometry.is_valid).sum()))
    print("geom types:\n", gdf.geometry.geom_type.value_counts())

def clean_and_clip(gdf, mask, keep_geom_type=True, min_area=1e-9):
    # 1) Keep original indices so we can debug drops
    gdf = gdf.copy()
    gdf["_orig_index"] = gdf.index

    # 2) Ensure both use the same CRS
    if gdf.crs != mask.crs:
        mask = mask.to_crs(gdf.crs)

    # 3) Clip using geopandas.clip
    clipped = geopandas.clip(gdf, mask, keep_geom_type=keep_geom_type)

    report_geoms(gdf, "original")
    report_geoms(clipped, "after clip")

    # 4) Remove explicit null/empty geometries
    clipped = clipped[clipped.geometry.notna()].copy()
    clipped = clipped[~clipped.geometry.is_empty].copy()

    # 5) Try to repair invalid geometries
    # prefer shapely.make_valid if available (Shapely >= 1.8/2.0), fallback to buffer(0)
    try:
        # shapely >= 2.0 style
        from shapely.validation import make_valid as shapely_make_valid
        clipped['geometry'] = clipped.geometry.apply(lambda g: shapely_make_valid(g) if g is not None else g)
    except Exception:
        try:
            # older shapely or fallback: buffer(0) often fixes self-intersections
            clipped['geometry'] = clipped.geometry.buffer(0)
        except Exception:
            # last resort: leave as-is but warn
            print("Warning: couldn't run make_valid or buffer(0) to fix geometries")

    # 6) Explode multiparts into singleparts (keeps attributes)
    # use index_parts=False to avoid hierarchical index (geopandas >= 0.11)
    clipped = clipped.explode(index_parts=False).reset_index(drop=True)

    # 7) Remove tiny or zero-area geometries created by numeric precision issues
    clipped['__area__'] = clipped.geometry.area
    clipped = clipped[clipped['__area__'] > min_area].copy()
    clipped = clipped.drop(columns='__area__')

    # ensure geometry column is set and GeoDataFrame class is preserved
    if 'geometry' not in clipped.columns:
        # try to find a geometry-like column
        geom_cols = [c for c in clipped.columns if clipped[c].dtype.name == 'geometry' or clipped[c].apply(lambda x: hasattr(x, 'geom_type')).any()]
        if geom_cols:
            clipped = clipped.set_geometry(geom_cols[0])
        else:
            raise RuntimeError("No geometry column found after cleaning")

    clipped = geopandas.GeoDataFrame(clipped, geometry='geometry', crs=gdf.crs)

    report_geoms(clipped, "after cleaning")
    return clipped

clip_nfvi = clean_and_clip(gb_vuln, clip)

#trying to categorise before sending to kml
bins = [float('-inf'), -1, -.6, float('inf')]
labels = ["Vulnerable", "Very Vulnerable", "Most vulnerable"]

clip_nfvi["category"] = pd.cut(clip_nfvi["nfvi-uk"], bins=bins, labels=labels)

color_map = {
    "Most Vulnerable": "7F0000FF",     # dark red, semi-transparent
    "Very Vulnerable": "4C0000FF", # medium red, more transparent
    "Vulnerable": "1A0000FF"      # light red, very transparent
}

kml = simplekml.Kml()

for _, row in clip_nfvi.iterrows():
    geom = row.geometry
    cat = row["category"]
    #color = color_map[cat]

    if geom.geom_type == "Polygon":
        pol = kml.newpolygon(name=cat)
        pol.outerboundaryis = list(geom.exterior.coords)
        #pol.style.polystyle.color = color
        pol.style.linestyle.color = "FF000000"  # black outline
        pol.style.linestyle.width = 1
    elif geom.geom_type == "MultiPolygon":
        for part in geom:
            pol = kml.newpolygon(name=cat)
            pol.outerboundaryis = list(part.exterior.coords)
            #pol.style.polystyle.color = color
            pol.style.linestyle.color = "FF000000"
            pol.style.linestyle.width = 1



kml.save("/Users/eclough_98/flooded-people/fp-flood-nvfi/data/clean/flood_vulnerability.kml")
