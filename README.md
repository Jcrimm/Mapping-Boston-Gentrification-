# Mapping Gentrification in Boston: 2010-2019

## Executive Summary
Over the last decade, major U.S. cities experienced large population growth, as well as more diverse. Boston Massachusetts is no exception: between 2010 and 2019, its population grew 9.4% and saw increases in nonwhite populations ([Hey, 2021](https://www.brookings.edu/research/2020-census-big-cities-grew-and-became-more-diverse-especially-among-their-youth/)). However, other studies have highlighted increasing income inequality and rising housing costs in the Boston metropolitan area ([Herman, Luberoff, Mccue, 2019](https://www.jchs.harvard.edu/sites/default/files/Harvard_JCHS_mapping_neighborhood_change_boston_january_2019.pdf)). Taken together, there have been large concerns about gentrification within Boston. Gentrification is a process of change in historically disinvested neighborhoods along economic lines, including real estate investment and higher-income households moving in, as well as changes in racial and educational attainment levels as well ([Urban Displacement Project at U.S. Berkely](https://www.urbandisplacement.org/about/what-are-gentrification-and-displacement/)). 

This project looks to visualize gentrification in Boston over the last decade. Its main output is a [heatmap of gentrification in Boston at the block group level](github.com/Jcrimm/Mapping-Boston-Gentrification-/blob/main/Boston%20Gentrificaton.png) using a "gentrification index." 
The data sources for this project include the Census's American Community Survey (ACS) five-year esimates, as well as geospatial data from the U.S. Census and the City of Boston. The project also includes a graph that checks for the robustness of the gentrification index when the racial indicator is removed.

## Instructions
The scripts should be run in the following order (see below). All geospatial data is provided within the repository, and the ACS data is retrieved in the first script through an API call. 

The index utilizes American Community Survey (ACS) five-year estimates for the following variables:
1. Percent of the population that is white nonhispanic
2. Median income
3. Median rent
4. Percent of the population over 25 that has a bachelor's degree or higher between 

