# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:22:05 2022

@author: jerem
"""

#%% Initial set-up
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
#join places onto tracts
boston = tracts.sjoin(places,how="left",predicate="within")

#remove missing values
boston = boston.query("GEOID_right=='2507000'")
boston = boston.reset_index()
boston = boston.drop(columns="index")


#%% boston tracts
tracts_boston = boston["TRACTCE"]
print(len(tracts_boston))
tracts_boston.to_csv("boston_tracts.csv")


