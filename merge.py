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
gent = pd.read_csv("gent_by_id.csv",dtype={"GEOID":str})
gent = gent.drop(columns="Unnamed: 0")

#read in geographic data
boston = gpd.read_file("within_boston.gpkg",layer="master")


#%% Now merge the two datafiles together

merged = boston.merge(gent,
                      on="GEOID",
                      how="left",
                      validate="1:1",
                      indicator=True)

merged = merged.drop(columns="_merge")

#%% Write to geopackage
merged.to_file("within_boston.gpkg",layer="gent",index=False)

