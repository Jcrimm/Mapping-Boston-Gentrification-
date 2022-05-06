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
                      how="left",
                      validate="1:1",
                      indicator=True)

merged = merged.drop(columns="_merge")

#%% Write to geopackage and csv
merged.to_file("boston.gpkg",layer="gent",index=False)
merged.to_csv("boston_gent.csv")

