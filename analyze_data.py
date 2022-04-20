# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:53:57 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import numpy as np

# Bring in 2014 data
data14 = pd.read_csv("Suffolk_blckgrps_2014.csv",dtype=str)

#bring in 2019 data
data19 = pd.read_csv("Suffolk_blckgrps_2019.csv",dtype=str)

#%% Now create some new variables
#first is the percent of population that's white not hispanic
#second is percent of population that has at least bachelor's degree

#create list of the files to loop over
files = [data19, data14]

#create list of variables we want to change to floats
numbers = ["pop","white","income","rent","totaled","bachelors","masters","professional","doctorate"]

#create a list of the variables to drop at the end of the loop
drop_cols = ["pop","white","bachelors","masters","professional","doctorate","totaled"]

#loop over the two files
#convert the missing values to nan
#convert the list of number variables from integers to floats
#calculate the percent of population that's white not hispanic
#calculate the percent of the population over 25 that has at least a bachelor's degree
#drop the variables we don't need anymore
#set the index to GEOID
for file in files:
    file = file.replace("-666666666",np.nan)
    file[numbers] = file[numbers].astype(float)
    #file["pct_white"] = 100*(file['white']/file['pop'])
    #file ["high_ed"] = 100*(file["bachelors"] + file["masters"] + file["professional"] + file["doctorate"])/file["totaled"]
    #file.drop(columns=drop_cols,inplace=True)
    #file.set_index("GEOID",inplace=True)

#%% Rename the percent and high ed columns to match the year

#2014
data14 = data14.rename(columns={"pct_white":"pct_white14","high_ed":"high_ed14"})

#2019
data19 = data19.rename(columns={"pct_white":"pct_white19","high_ed":"high_ed19"})

#%%