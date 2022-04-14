# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:22:05 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import geopandas as gpd

utm18n = 26986

#%% Read in files

# read in places file
places = gpd.read_file("cb_2019_25_place_500k.zip",dtype=str)

#bring in tracts data
tracts = gpd.read_file("cb_2019_25_tract_500k.zip",dtype=str)


#%% 

#project to the standard mass utm18n
places = places.to_crs(epsg=utm18n)
tracts = tracts.to_crs(epsg=utm18n)

#spatial join
#first do a spatial join of places onto tracts for any tracts that intersect
overlaps = tracts.sjoin(places,how="left",predicate="overlaps")

#then do a spatial join for all tracts that are within places
within = tracts.sjoin(places,how="left",predicate="within")

#Select only the rows for Boston
within_boston = within.query("GEOID_right=='2507000'")
overlap_boston = overlaps.query("GEOID_right=='2507000'")

#concacanate the two dataframes together
#result is all tracts that are within or intersect with Boston
tract_list = [within_boston,overlap_boston]

boston = pd.concat(tract_list)

boston = boston.reset_index()
boston = boston.drop(columns="index")

#%%
boston.to_file("boston.gpkg",layer="master",index=False)

#%% boston tracts
tracts_boston = boston["TRACTCE"]
print(len(tracts_boston))
tracts_boston.to_csv("boston_tracts.csv")


