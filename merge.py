# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:58:40 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import geopandas as gpd

#%% Read in data files

#read in demographic data
gent = pd.read_csv("gent_by_block_grp.csv",dtype={"GEOID":str})

#read in geographic data
boston = gpd.read_file("boston.gpkg",layer="master")


#%% Now merge the two datafiles together

merged = boston.merge(gent,
                      on="GEOID",
                      how="outer",
                      validate="1:1",
                      indicator=True)

print(merged["_merge"].value_counts())

#merged = merged.drop(columns="_merge")

#%% Write to geopackage
merged.to_file("within_boston.gpkg",layer="gent",index=False)

