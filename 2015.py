# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:56:23 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Create API Request for 2014 ACS five year estimate

api = 'https://api.census.gov/data/2014/acs/acs5'

payload = {'get': var_string, 'for':for_clause,'in':in_clause,'key':key_value}
response = requests.get(api,payload)

#check whether it worked
if response.status_code==200:
    print(f"Success!")
else:
    print(response.status_code)
    print(response.text)
    assert False

#%%Set row list
row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2014 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
columns = {"B01001_001E":"pop14",
           "B03002_002E":"white14",
           "B19013_001E":"income14",
           "B25064_001E":"rent14",
           "B15003_001E": "totaled",
           "B15003_022E": "bachelors",
           "B15003_023E":"masters",
           "B15003_024E": "professional", 
           "B15003_025E": "doctorate"}
data2014 = data2014.rename(columns=columns)

#create GEOID
data2014["GEOID"] =  data2014["state"] + data2014["county"] + data2014["tract"]

#set index to tract
data2014.set_index("tract",inplace=True)

#convert columns from strings to integers
numbers = ["pop14","white14","income14","rent14","totaled","bachelors","masters","professional","doctorate"]
data2014[numbers] = data2014[numbers].astype(int)

#%% calculate proportion of tract that has bachelor's degree or higher
data2014["attain"] = data2014["bachelors"] + data2014["masters"] + data2014["professional"] + data2014["doctorate"]
data2014["bachplus14"] = data2014["attain"]/data2014["totaled"]

#drop all number columns except proportion of tract with bachelors or higher
data2014.drop(columns = ["totaled","bachelors","masters","professional","doctorate","attain"] ,inplace=True)

# reorder columns
data2014 = data2014.reindex(columns = ["NAME", "pop14", "white14","income14","rent14","bachplus14","state","county","GEOID"])

#%% Write to csv file
data2014.to_csv("Suffolk_2014.csv")