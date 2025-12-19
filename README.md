# Flooded People: Vulnerability to floods and flood risk


## Project Goal:
[Flooded People](https://www.floodedpeople.org.uk) are interested in understanding where people who are particularly vulnerable to the impacts of flooding are most at risk of being flooded, or have experienced flooding in the past.

The project builds on the work of the [Climate Just](https://climatejust.org.uk) resource and website, developed by Joseph Rowntree Foundation and University of Manchester and others.. It appears this was last updated in 2017.

Flooded People are particularly working on a National Lottery Community Fund project that organises people in key flooded communities in England and Scotland:

- Leicester
- Hull
- Birmingham
- Tower Hamlets
- Dundee 
- Glasgow

For these council areas, the project identifies neighbourhoods and areas where people who are highly vulnerable to the impacts of flooding *and* have also been flooded in the past or are or at risk of flooding in the future. FP are hoping to use this analysis to focus who they speak to as part of their project with the National Lottery.

The analysis will be used by community organisers and campaigners, so it is particularly important that the outputs are accessible and legibile to them. The basic approach is therefore to build a series of KML maps from existing data and feed these into MyMaps in Google. This should allow FP and community organisers to use the maps to observe overall patterns in the communities, as well as an on-the-ground tool for navigating communities through the GoogleMaps app.


## Available Data:

The project examines two broad concepts:
- vulnerability to the impacts of flooding
- flood exposure

Data collection is a devolved matter, so data has been processed separately for England and Scotland. I've outlined below where I got the data and how I processed it before uploading to Google Mymaps.

### Vulnerability to flooding
The measure of vulnerability to flooding is the Neighbourhood Flooding Vulnerability Index, developed by Sayer and Partners for the UK's Climate Change Committee. The NFVI:

> considers the characteristics of people and the communities in which they live that would – if they were to be exposed to  a flood hazard – make them more or less likely to experience a negative welfare outcome.

It is built using five different dimension of flood vulnerability. The measures are calculated using z-scores, so are relative rather than absolute measures. Scores below zero indicate a worse than average level of vulnerability to flooding. There are options to use the z-score relative to the country, or relative to the UK as a whole.

The NFVI is measured at the [2021 Lower layer Super Output Areas](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bsc-v4-2/about) level in England, and [2011 Intermediate Zone Boundaries](https://www.data.gov.uk/dataset/133d4983-c57d-4ded-bc59-390c962ea280/intermediate-zone-boundaries-2011) level in Scotland.

The latest NFVI was calculated in 2025 based on 2021 UK Census data (when available), and a thorough discussion of the elements is available on the [UK Climate Risk website](https://www.ukclimaterisk.org/wp-content/uploads/2025/07/Sayers-et-al-2025-Climate-Vulnerability-Indicators-1.pdf). The dataset was sourced from the [same place](https://www.ukclimaterisk.org/wp-content/uploads/2024/08/Sayers-ClimateVulnerabilityIndicators_Neighbourhoods-06March2025-Submitted.xlsx).

In the maps, I've classified different areas based on the schema provided in the [Climate Just map](https://www.climatejust.org.uk/map.html):

- Acute Vulnerability: NFVI >= 2.5
- Extremely High Vulnerability: NFVI >= 1.5 & < 2.5
- Relatively High Vulnerability: NFVI >= .5 & < 1.5
- Average Vulnerability: NFVI >= -.5 & < .5
- Relatively Low Vulnerability: NFVI >= -1.5 & < -.5
- Extremely Low Vulnerability: NFVI >= -2.5 &  < -1.5
- Slight Vulnerability: NFVI <= -2.5

### Flood exposure

We're interested in several distinct dimensions of flood exposure. In particular:
- risk of flooding in the future
- whether a community/neighbourhood has been flooded in the past

### Risk of flooding 

##### England
The 2024 UK National Flood Risk Assessment ([Nafra](https://www.gov.uk/government/publications/national-assessment-of-flood-and-coastal-erosion-risk-in-england-2024/national-assessment-of-flood-and-coastal-erosion-risk-in-england-2024)) is the government's regular national flood risk assessment for England. 

##### Flood risk from river and sea
Flood risks for river and sea flooding are shared on data.gov.uk, through the [Flood Map for Planning - Flood Zones](https://www.data.gov.uk/dataset/104434b0-5263-4c90-9b1e-e43b1d57c750/flood-map-for-planning-flood-zones1) page. 

Flood from river and seas in England is classsified in three zones. This project concentrates on flood zones 2 & 3.
- Flood Zone 2: Land having between a 1% and 0.1% annual probability of river flooding; or land having between a 0.5% and 0.1% annual probability of sea flooding.
- Flood Zone 3: Land having a 1% or greater annual probability of river flooding; or Land having a 0.5% or greater annual probability of sea

##### Flood risk from surface water (RoSWF)
Flood risks for surface water files are huge, and thus need to be requested from data.gov.uk, through the [Risk of Flooding from Surface Water (RoFSW)](https://www.data.gov.uk/dataset/0d6fa1f4-0c82-4c91-8667-a549e8e3ca2d/risk-of-flooding-from-surface-water3). 

Flood risk from surface water has the same classification system as flood risk from river and sea.

In order to get the RoSWF files down to a workable size, I've combined surface water flood zones 2&3 on the map. I have also simplified the shapes of the flood zones considerably. These shapes should still give a reasonable sense of where surface water flooding is likely to occur.

##### Historic flooding

Historical flooding for England is available from  [Environment Agency]().

The map only shows historical flooding since 2000. 


#### Scotland
Flood data collection is a devolved power, and Scotland collects its flood data in slight different ways to 

##### Flood risk from river and sea

Unlike England and Wales, Scotland calculates flood risk from river and seas separately. Scottish flood data can be found [here](https://www2.sepa.org.uk/flooddata/). For this project, I've merged the river and sea flooding so that it is easier to relate to the England and Wales data.

Flood risk in Scotland is classified in two levels:

- High likelihood: A flood event is likely on average in the defined area once in every ten years (1:10). Or a 10% chance of happening in any one year.
- Medium likelihood: A flood event is likely in the defined area on average once in every two hundred years (1:200). Or a 0.5% chance of happening in any one year

##### Flood risk from surface water (RoSWF)

Risk of flooding from surface water in Scotland is classified in the same way as flood risk from rivers and seas. For practical reasons, the high and medium risk areas have been merged in the map.


##### Historic flooding
Scotland doesn't make historic flooding data available.

## Approach

Flooded People would like to use these as practical tools for reaching communities on the ground. In order to do this, I'm converting the resulting maps to KML and uploading them to a custom Google Map. In order to keep these files under 5MB, I've created one for England and one for Scotland. That also reflects the fact that the sources for these data are often quite different. This also means FP doesn't need to self-host the maps, which might be a bit of a faff for this project.

Reducing file sizes to 5MB has required some compromises in the presentation of the data, particularly for the surface water flooding data. These compromises can be found in the detail of the code. The maps produced here should not be used for in-depth analysis.

### Identifying those most vulnerable and most at risk

The multiple layers in the map provide some rich context, but they make it challenging to identify the most vulnerable communities where people are also the most at risk of flooding. I've created a further layer to reflect the categories that reflect these. These categories are defined as follows:

- Level 1: Extremely and Very Flood Vulnerable People in High Risk Floodzones
- Level 2: Relatively High Flood Vulnerable People in High Risk Floodzones *and* Extremely and Very Flood Vulnerable People in Medium Risk Floodzones
- Level 3: Relatively High Flood Vulnerable People in Medium Risk Floodzones


