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
places = gpd.read_file("cb_2019_25_place_500k.zip",dtype=str)

#bring in tracts data
tracts = gpd.read_file("cb_2019_25_tract_500k.zip",dtype=str)


#%% 

# set the utm18n to 26986, the one used for Massachusetts 
utm18n = 26986

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
#tract_list = [within_boston,overlap_boston]

#boston = pd.concat(tract_list)

#boston = boston.reset_index()
#boston = boston.drop(columns="index")


#%% Keep just the tracts from the tracts dataset
keep = ["GEOID_left","ALAND_left","AWATER_left",'geometry']
within_boston = within_boston[keep]

#rename the columns
within_boston = within_boston.rename(columns={"GEOID_left":"GEOID","ALAND_left":"ALAND","AWATER_left":"AWATER"})


#%% write to geopackage
within_boston.to_file("within_boston.gpkg",layer="master",index=False)

#this is for all tracts that are within and overlap Boston
#boston.to_file("boston.gpkg",layer="master",index=False)

#%% boston tracts
tracts_boston = boston["TRACTCE"]
print(len(tracts_boston))
tracts_boston.to_csv("boston_tracts.csv")


