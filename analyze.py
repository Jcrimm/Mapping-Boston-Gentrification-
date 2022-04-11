# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:20:25 2022

@author: jerem
"""

#%% Set-up
import pandas as pd
import geopandas as gpd

#bring in 2019 data
data19 = pd.read_csv("Suffolk_2019.csv",dtype={"tract":str,"state":str,"county":str,"GEOID":str})
data19.set_index("tract",inplace=True)

#bring in 2014 data
data14 = pd.read_csv("Suffolk_2014.csv",dtype={"tract":str,"state":str,"county":str,"GEOID":str})
data14.set_index("tract",inplace=True)

#%% Now merge the datasets

