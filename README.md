# Flooded People: Vulnerability to floods and flood risk


## Project Goal:
[Flooded People](https://www.floodedpeople.org.uk) are interested in understanding where people who are particularly vulnerable to the impacts of flooding are most at risk of being flooded, or have experienced flooding in the past.

The project is inspired in part by the work of JRF, University of Manchester and others in building the [Climate Just](https://climatejust.org.uk) resource and website. It appears this was last updated in 2017.

While it would be fun and useful to try to reproduce that analysis on a UK-wide scale, the digital infrastructure for this scale of project is not available at this time. This project will focus on the following geographic areas:

-Leicester
-Hull
-Birmingham
-Dundee 
-Stirling 
-Alloa

For these municipalities, the project will try to identify neighbourhoods and areas where people are highly vulnerable to the impacts of flooding and where those people have been flooded in the past or are likely to be flooded in the future. FP are hoping to use this analysis to focus who they speak to as part of their project with the National Lottery.

The analysis will be used by community organisers and campaigners, so it is particularly important that the outputs are accessible and legibile to them. Possible ideas: identifying lists of postcodes, or layering on to googleMaps

## Available Data:

The project examines two broad concepts:
-vulnerability to the impacts of flooding
-flood exposure

### Vulnerability to flooding
The measure of vulnerability to flooding is the Neighbourhood Flooding Vulnerability Index, developed by Sayer and Partners for the UK's Climate Change Committee. The NFVI:

> considers the characteristics of people and the communities in which they live that would – if they were to be exposed to  a flood
hazard – make them more or less likely to experience a negative welfare outcome.

It is built using five different dimension of flood vulnerability. The measures are calculated using z-scores, so are relative rather than absolute measures. Scores below zero indicate a worse than average level of vulnerability to flooding.

The NFVI is measured at the [LSOA](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bsc-v4-2/about) level.

The latest NFVI was calculated in 2025, and a thorough discussion of the elements is available on the [UK Climate Risk website](https://www.ukclimaterisk.org/wp-content/uploads/2025/07/Sayers-et-al-2025-Climate-Vulnerability-Indicators-1.pdf). The dataset was sourced from the {same place}(https://www.ukclimaterisk.org/wp-content/uploads/2024/08/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx).

### Flood exposure

We're interested in several distinct dimensions of flood exposure. In particular:
-risk of flooding in the future
-whether a community/neighbourhood has been flooded in the past

Risk of flooding 
NAFRA2: the latest national flood risk assessment for England. Sending the link to the flood map for planning below. Might need to do a bit of wrangling on there to get the data set in terms of GiS files. Important to get surface water as well as river and sea, since most of the locations are urban. 
https://flood-map-for-planning.service.gov.uk/

SEPA NFRA: Since flood risk management is devolved and two of our target areas are in Scotland, we also need SEPA data. Their NFRA is here: https://informatics.sepa.org.uk/NFRA2018/

Neighborhood Flood Vulnerability index (NVFI): developer by Sayers and Partners, this gives you vulnerability based on census wards. The data is held on Climate Just: https://www.climatejust.org.uk/map.html. Can’t find the new data… it was posted widely by CCC but is now gone. Can send you the pdf report. It’s big. 

Flood histor 1y: This historic flood map by EA shows the outlines of the floods they know about. Would be great if we could get the dates in there. https://www.data.gov.uk/dataset/76292bec-7d8b-43e8-9c98-02734fd89c81/historic-flood-map1
