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


#%% 

# set the utm18n to 26986, the one used for Massachusetts 
utm18n = 26986

#project to the standard mass utm18n
city = city.to_crs(epsg=utm18n)
block_grps = block_grps.to_crs(epsg=utm18n)

#spatial join
#first do a spatial join of city onto block_grps for any block_grps that intersect
overlaps = block_grps.sjoin(city,how="left",predicate="overlaps")

#then do a spatial join for all block_grps that are within the city
within = block_grps.sjoin(city,how="left",predicate="within")

#Select only the rows for Boston. How many in each group? 
within_boston = within.query("GEOID_right=='2507000'")
print(f"Number of Block groups within Boston: {len(within_boston)}")
overlap_boston = overlaps.query("GEOID_right=='2507000'")
print(f"Number of Block groups overlapping Boston: {len(overlap_boston)}")

#concacanate the two dataframes together
#result is all tracts that are within or intersect with Boston
tract_list = [within_boston,overlap_boston]

boston_grps = pd.concat(tract_list)

#intersect the city boundaries with the block groups file
intersect = block_grps.sjoin(city,how="left",predicate="intersects")
#select only those that intersect w/ Boston
intersect = intersect.query("GEOID_right=='2507000'")

#try two different clips
#boston1 clips intersect with the city file
boston1 = intersect.clip(city,keep_geom_type=True)
#boston 2 clips the boston_grps with the city file
boston2 = boston_grps.clip(city,keep_geom_type=True)

#check that the boston_grps is the same length as boston
print(f"Number of records in clipped data using intersection: {len(boston1)}")
print (f"Number of records in clipped data using the concant: {len(boston2)}")


#%% Keep just the tracts from the tracts dataset
keep = ["GEOID_left","ALAND_left","AWATER_left",'geometry']
within_boston = within_boston[keep]

#rename the columns
within_boston = within_boston.rename(columns={"GEOID_left":"GEOID","ALAND_left":"ALAND","AWATER_left":"AWATER"})


#%% write to geopackage
within_boston.to_file("within_boston.gpkg",layer="master",index=False)




