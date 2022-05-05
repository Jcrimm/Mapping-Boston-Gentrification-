# Mapping Gentrification in Boston: 2010-2019

## Executive Summary
Over the last decade, major U.S. cities experienced large population growth, as well as more diverse. Boston Massachusetts is no exception: between 2010 and 2019, its population grew 9.4% and saw increases in nonwhite populations ([Hey, 2021](https://www.brookings.edu/research/2020-census-big-cities-grew-and-became-more-diverse-especially-among-their-youth/)). However, other studies have highlighted increasing income inequality and rising housing costs in the Boston metropolitan area ([Herman, Luberoff, Mccue, 2019](https://www.jchs.harvard.edu/sites/default/files/Harvard_JCHS_mapping_neighborhood_change_boston_january_2019.pdf)). Taken together, there have been large concerns about gentrification within Boston. Gentrification is a process of change in historically disinvested neighborhoods along economic lines, including real estate investment and higher-income households moving in, as well as changes in racial and educational attainment levels as well ([Urban Displacement Project at U.S. Berkely](https://www.urbandisplacement.org/about/what-are-gentrification-and-displacement/)). 

This project looks to visualize gentrification in Boston over the last decade. Its main output is a [heatmap of gentrification in Boston at the block group level](github.com/Jcrimm/Mapping-Boston-Gentrification-/blob/main/Boston%20Gentrificaton.png) using a "gentrification index" (see details on methodology below). It can also be used to create a second map highlighting changes in low-income block groups, those whose median income were below the 2010 citywide median income of $49,893 ([Boston's People and Economy](https://www.boston.gov/sites/default/files/embed/f/fy16-volume1-bostons-people-economy.pdf)).
The data sources for this project include the Census's American Community Survey (ACS) five-year esimates, as well as geospatial data from the U.S. Census and the City of Boston. The project also includes a graph that checks for the robustness of the gentrification index when the racial indicator is removed.

## Instructions
The scripts should be run in the order as indicated below. All geospatial data is provided within the repository, and the ACS data is retrieved in the first script through an API call. Other data files within the repository are created by the scripts and are provided for convenience. There is also a QGIS project within the repository which was used to create the maps.

### Script #1: get_data
This script defines a function called get which makes the API request for the ACS five-year estimates and turns it into a dataframe. It then loops through the years of interest (the 2014 and 2019 ACS five year estimate) applying the get function, creates a GEOID and sets it as the index, and saves each year as a csv file for use in the next script. 

The API request calls the following variables for all block groups in Suffolk County, MA. These will be used to create the gentrification index. 
1. Total population
2. Total population that is white nonhispanic
3. Median income
3. Median rent
4. Total educational attainment for the population over 25
5. Total number of individuals over 25 with a bachelor's degree
6. Total number of individuals over 25 with a master's degree
7. Total number of individuals over 25 with a professional degree
8. Total number of individuals over 25 with a doctorate degree

### Script #2: analyze_data
The script builds the gentrification index and saves the result as a CSV. 

It first reads in the csv files created in the get_data. It then loops through them, filling in missing data, calculating the percentage of the population that's white nonhispanic and the percentage of the population over 25 that has a bachelor's degree or higher. 

The script then builds a new dataframe, joined, that's the percentage change between the 2014 and 2019 datasets for the following variables for each block group. 
1. Percentage of the population that's nonwhite hispanic
2. Median income
3. Median rent
4. Percentage of the population over 25 with at least a bachelor's degree

Next, it loops through each column in joined, creates quintiles for each variable, and reads the result into a new dataframe called quint. Each column in quint will have a value of 1-5, with five indicating the highest quintile. Each value is summed across to create a gentrification index. The script also creates a second index that does not include the race variable. Higher values for the index indicate more gentrification. The script also creates a new dummy variable within quint that indicates whether the block group's median income was below the citywide median income in 2010. 

Finally, the script writes the quint dataframe to a csv file.

### Script #3: filter
This script builds the geographic data needed for the map and saves it to a geopackage. 

