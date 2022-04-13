# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:20:25 2022

@author: jerem
"""

#%% Set-up
import pandas as pd
import geopandas as gpd
import numpy as np

#bring in 2019 data
data19 = pd.read_csv("Suffolk_2019.csv",dtype={"tract":str,"state":str,"county":str,"GEOID":str})
data19.set_index("tract",inplace=True)

#bring in 2014 data
data14 = pd.read_csv("Suffolk_2014.csv",dtype={"tract":str,"state":str,"county":str,"GEOID":str})
data14.set_index("tract",inplace=True)

#%% Now merge the datasets

joined = data19.merge(data14,
                      on=["tract","NAME","state","county","GEOID"],
                      how="inner",
                      validate="1:1",
                      indicator=True)

# drop the merge columns
joined.drop(columns="_merge",inplace=True)

#%% Calculate percent changes for each variable

#For percent white
joined["change_white"] = 100*(joined["pct_white_19"] - joined["pct_white_14"])/joined["pct_white_14"]

# For income
joined["change_inc"] = 100*(joined["income19"] - joined["income14"])/joined["income14"]

# for rent
joined["change_rent"] = 100*(joined["rent19"] - joined["rent14"])/joined["rent14"]

#for education
joined["change_educ"] = 100*(joined["bachplus19"] - joined["bachplus14"])/joined["bachplus14"]

#%% Keep just the change columns
drop = ["pop19","white19","pct_white_19","income19","rent19","bachplus19","pop14","white14","pct_white_14","income14","rent14","bachplus14"]
joined = joined.drop(columns=drop)

#%% Group tracts into quintiles based on each variable

# quintiles for percent white
joined["white_quint"] = pd.qcut(joined["change_white"],5,labels=[1,2,3,4,5])

# quintiles for income
joined["inc_quint"] = pd.qcut(joined["change_inc"],5,labels=[1,2,3,4,5])

#quintiles for rent
joined["rent_quint"] = pd.qcut(joined["change_rent"],5,labels=[1,2,3,4,5])

#quntiles for education
joined["educ_quint"] = pd.qcut(joined["change_educ"],5,labels=[1,2,3,4,5])

#%% Now create index by adding each score up

#convert quintile value to a float
quintiles = ["white_quint","inc_quint","rent_quint","educ_quint"]
joined[quintiles] = joined[quintiles].astype(float)

# first disregard any records that do not have a value for at least one of the quintiles
bad_quintiles = joined[quintiles]
if bad_quintiles==False:
    
    





    

