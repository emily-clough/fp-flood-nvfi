# Flooded People: Vulnerability to floods and flood risk


## Project Goal:
[Flooded People](https://www.floodedpeople.org.uk) are interested in understanding where people who are particularly vulnerable to the impacts of flooding are most at risk of being flooded, or have experienced flooding in the past.

The project is inspired in part by the work of JRF, University of Manchester and others in building the [Climate Just](https://climatejust.org.uk) resource and website. It appears this was last updated in 2017.

While it would be fun and useful to try to reproduce that analysis on a UK-wide scale, the digital infrastructure for this scale of project is not available at this time. This project will focus on the following geographic areas:

- Leicester
- Hull
- Birmingham
- Dundee 
- Glasgow

For these council areas, the project will try to identify neighbourhoods and areas where people who are highly vulnerable to the impacts of flooding *and* have also been flooded in the past or are likely to be flooded in the future. FP are hoping to use this analysis to focus who they speak to as part of their project with the National Lottery.

The analysis will be used by community organisers and campaigners, so it is particularly important that the outputs are accessible and legibile to them. Possible ideas: identifying lists of postcodes, or layering on to GoogleMaps or OpenStreetMaps.

## Available Data:

The project examines two broad concepts:
- vulnerability to the impacts of flooding
- flood exposure

### Vulnerability to flooding
The measure of vulnerability to flooding is the Neighbourhood Flooding Vulnerability Index, developed by Sayer and Partners for the UK's Climate Change Committee. The NFVI:

> considers the characteristics of people and the communities in which they live that would – if they were to be exposed to  a flood hazard – make them more or less likely to experience a negative welfare outcome.

It is built using five different dimension of flood vulnerability. The measures are calculated using z-scores, so are relative rather than absolute measures. Scores below zero indicate a worse than average level of vulnerability to flooding. There are options to use the z-score relative to the country, or relative to the UK as a whole.

The NFVI is measured at the [2021 Lower layer Super Output Areas](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bsc-v4-2/about) level in England, and [2011 Intermediate Zone Boundaries](https://www.data.gov.uk/dataset/133d4983-c57d-4ded-bc59-390c962ea280/intermediate-zone-boundaries-2011) level in Scotland.

The latest NFVI was calculated in 2025 based on 2021 UK Census data (when available), and a thorough discussion of the elements is available on the [UK Climate Risk website](https://www.ukclimaterisk.org/wp-content/uploads/2025/07/Sayers-et-al-2025-Climate-Vulnerability-Indicators-1.pdf). The dataset was sourced from the [same place](https://www.ukclimaterisk.org/wp-content/uploads/2024/08/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx).

It is worth noting that the NVFI contains information about whether a neighbourhood has experienced flooding in the past. 

> Number of properties within historical flood boundary, based on query of property datasets and flood outlines as available in 2015; limited to past 50 years when date information available. Data updated to link to the 2021 census boundaries (Z-score only due to licence constraints). 

This could be helpful with looking at flood exposure, as below.

### Flood exposure

We're interested in several distinct dimensions of flood exposure. In particular:
- risk of flooding in the future
- whether a community/neighbourhood has been flooded in the past

### Risk of flooding 

The 2024 UK National Flood Risk Assessment ([Nafra](https://www.gov.uk/government/publications/national-assessment-of-flood-and-coastal-erosion-risk-in-england-2024/national-assessment-of-flood-and-coastal-erosion-risk-in-england-2024)) is the government's regular national flood risk assessment for England. 

Data for flood risk is availabe for both rivers and seas, and surface flooding.

##### England
Flood risks for river and sea flooding are shared on data.gov.uk, through the [Flood Map for Planning - Flood Zones](https://www.data.gov.uk/dataset/104434b0-5263-4c90-9b1e-e43b1d57c750/flood-map-for-planning-flood-zones1) page. For v 0.1 of this project, I'm using geo-json files.

Flood risks for surface water are published on data.gov.uk, through the [Risk of Flooding from Surface Water (RoFSW)](https://www.data.gov.uk/dataset/0d6fa1f4-0c82-4c91-8667-a549e8e3ca2d/risk-of-flooding-from-surface-water3). You can download the geojson from [here](https://environment.data.gov.uk/explore/b5aaa28d-6eb9-460e-8d6f-43caa71fbe0e?download=true), but it will not allow download of the whole country. I'll need to create a shapefile for the six listed council areas (or perhaps just those in England?) before attempting this again.


##### Scotland

Scotland has all flood risk data available on [SEPA's](https://www2.sepa.org.uk/flooddata/) website. This is all in .gdb data, which seems readily useable by geopandas.

### Flood history

This [historic flood map](https://www.data.gov.uk/dataset/76292bec-7d8b-43e8-9c98-02734fd89c81/historic-flood-map1) by EA shows the outlines of the floods EA knows about. It is readily available as a shapefile.  FP would like to know *when* the flood occurred.


## Next steps

- [] get all the data!
    - [x] shapefiles for the designated councils
    - []  flood risk for surface water downloads
- [] link flood vulnerability to the underlying lsoa shapefiles
- [] transform each of the three maps into a google layer