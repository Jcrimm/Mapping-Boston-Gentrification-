# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:53:57 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import numpy as np

# Bring in 2014 & 2019 data. We'll convert to strings later on
data14 = pd.read_csv("Suffolk_blckgrps_2014.csv",dtype=str)
data19 = pd.read_csv("Suffolk_blckgrps_2019.csv",dtype=str)

#%% Now clean the data and create some variables
#first variable is the percent of population that's white not hispanic
#second variable is percent of population that has at least bachelor's degree

#create list of the files to loop over
files = [data14, data19]

#create list of variables we want to change to floats
numbers = ["pop","white","income","rent","totaled","bachelors","masters","professional","doctorate"]

#create a list of the variables to drop at the end of the loop
drop_cols = ["pop","white","bachelors","masters","professional","doctorate","totaled"]

#loop over the two files
#convert the missing values to nan
#convert the list of number variables to floats from strings
#calculate the percent of population that's white not hispanic
#calculate the percent of the population over 25 that has at least a bachelor's degree
#drop the variables we don't need anymore
#set the index to GEOID
for file in files:
    file.replace("-666666666",np.nan, inplace=True)
    file[numbers] = file[numbers].astype(float)
    file["pct_white"] = 100*(file['white']/file['pop'])
    file ["high_ed"] = 100*((file["bachelors"] + file["masters"] + file["professional"] + file["doctorate"])/file["totaled"])
    file.drop(columns=drop_cols,inplace=True)
    file.set_index("GEOID",inplace=True)

#%% Calculate percent changes for each variable across years
joined = 100*(data19-data14)/data14

#%%  Calculate quintiles for each column

#create empty dataframe to hold the quintiles values
quint = pd.DataFrame()

#loop through the columns of joined creating quintiles for each variable
for columns in joined:
    quint[columns] = pd.qcut(joined[columns],5,labels=[1,2,3,4,5])
    quint = quint.astype(float)

#create the gentrification index
#add the the values of each quintile to create a gentrification score
quint["gent_index"] = quint["income"] + quint["rent"] + quint["pct_white"] + quint["high_ed"]

#write to csv file
quint.to_csv("gent_by_block_grp.csv")




    
    
    
    

