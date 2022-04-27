# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:22:05 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import geopandas as gpd

#%% Read in files

# read in places file
city = gpd.read_file("cb_2019_25_place_500k.zip",dtype=str)

#bring in block groups data
block_grps = gpd.read_file("cb_2019_25_bg_500k.zip",dtype=str)


#%% Project the geographic data to the standard utn18n for massachusetts

# set the utm18n to 26986, the one used for Massachusetts 
utm18n = 26986

#project to the standard mass utm18n
city = city.to_crs(epsg=utm18n)
block_grps = block_grps.to_crs(epsg=utm18n)

#%% Join the block groups and city geographic data
#then clip the block group data on the city data to create the city boundary

#spatial join
#first do a spatial join of city onto block_grps for any block_grps that intersect
overlaps = block_grps.sjoin(city,how="inner",predicate="overlaps")

#then do a spatial join for all block_grps that are within the city
within = block_grps.sjoin(city,how="inner",predicate="within")

#Select only the rows for Boston. How many in each group? 
within_boston = within.query("GEOID_right=='2507000'")
print(f"Number of Block groups within Boston: {len(within_boston)}")
overlap_boston = overlaps.query("GEOID_right=='2507000'")
print(f"Number of Block groups overlapping Boston: {len(overlap_boston)}")

#concacanate the two dataframes together
#result is all tracts that are within or overlap with Boston
blckgrp_list = [within_boston,overlap_boston]
boston_grps = pd.concat(blckgrp_list)

# Now clip the boston_grps on the city boundary data
#boston clips the boston_grps with the city file
boston = boston_grps.clip(city,keep_geom_type=True)

#%% Keep just the data from the block groups dataset and rename columns
keep = ["GEOID_left","ALAND_left","AWATER_left",'geometry']
boston = boston[keep]

#rename the columns
boston = boston.rename(columns={"GEOID_left":"GEOID","ALAND_left":"ALAND","AWATER_left":"AWATER"})

#resent index and then set index to GEOID. Drop the old index 
boston = boston.reset_index()
boston.set_index("GEOID",inplace=True)
boston = boston.drop(columns="index")

#%% write to geopackage
boston.to_file("boston.gpkg",layer="master",index=True)




