#this file is to process the NFVI data--pull it in and match it to the relevant LSOA


import pandas as pd
import geopandas

#extracting the relevant sheet from nvfi file

inpath = "/Users/eclough_98/flooded-people/fp-flood-nvfi/data/raw/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx"

df = pd.read_excel(inpath, sheet_name="Indices - Integrated", skiprows=5, usecols='C, E, I', engine = "openpyxl" )

df.columns = ['index', 'nfvi-national', 'nfvi-uk']

#pulling in LSOA geojson

lsoa = read


