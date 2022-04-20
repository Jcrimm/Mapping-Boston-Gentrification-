# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:06:43 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests
import numpy as np


#%% Bring in Variables of interest

#Variables of interest (Table Shells)
#"NAME"
#B01001_001E": total population
#"B03002_002E" : Not Hispanic or Latino: White Alone
#"B19013_001E" median income in the last 12 months, inflation adjusted
#"B25064_001E": Median Rent
#"B15003" educational attainment for population over 25 (table ID)
    # "B15003_001E" : total
    # "B15003_022E" : bachelor's degree
    # "B15003_023E" : master's degree
    # "B15003_024E" : professional degree
    # "B15003_025E" : doctoral degree


#Create a list of all the variables we want, exluding education.
var_list = ["NAME","B01001_001E","B03002_002E","B19013_001E","B25064_001E","B15003_001E","B15003_022E","B15003_023E","B15003_024E","B15003_025E"]

#create a string for all the variables
var_string = ",".join(var_list)


#%% Create API request for 2019 ACS 5-year estimate


# Trial import
api = 'https://api.census.gov/data/2019/acs/acs5'

#Select tracts of interest--only those in Boston! 
#for_clause = {"tract":tract_string2010}
#other for_clause: all tracts in Suffolk County
for_clause = "tract:*"

#For the in clause, want Massachusetts and Suffolk County
in_clause = "state:25 county:025"

#put in census API key. 
key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"

payload = {'get': var_string, 'for':for_clause,'in':in_clause,'key':key_value}
response = requests.get(api,payload)

#check whether it worked
if response.status_code==200:
    print(f"Success!")
else:
    print(response.status_code)
    print(response.text)
    assert False

#%% Convert to a dataframe

# Create a row list to hold all the data
row_list = response.json()

#Set the first row to be variable/column names
colnames = row_list[0]

#Set the rest of the rows to be observations
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2019 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
columns2019 = {"B01001_001E":"pop19",
               "B03002_002E":"white19",
               "B19013_001E":"income19",
               "B25064_001E":"rent19",
               "B15003_001E": "totaled",
               "B15003_022E": "bachelors",
               "B15003_023E":"masters",
               "B15003_024E": "professional", 
               "B15003_025E": "doctorate"}
data2019 = data2019.rename(columns=columns2019)

#create GEOID
data2019["GEOID"] =  data2019["state"] + data2019["county"] + data2019["tract"]

#set index to tract
data2019.set_index("tract",inplace=True)

#Convert all the missing data to nan
data2019 = data2019.replace("-666666666",np.nan)

#convert columns from strings to integers
numbers = ["pop19","white19","income19","rent19","totaled","bachelors","masters","professional","doctorate"]
data2019[numbers] = data2019[numbers].astype(float)

#%% Calculate the percentage of each tract that's white
data2019["pct_white_19"] = data2019["white19"]/data2019["pop19"]


#%% calculate proportion of tract that has bachelor's degree or higher
data2019["attain"] = data2019["bachelors"] + data2019["masters"] + data2019["professional"] + data2019["doctorate"]
data2019["bachplus19"] = data2019["attain"]/data2019["totaled"]

#drop all number columns except proportion of tract with bachelors or higher
data2019.drop(columns = ["totaled","bachelors","masters","professional","doctorate","attain"] ,inplace=True)

# reorder columns
data2019 = data2019.reindex(columns = ["NAME","pop19","white19","pct_white_19","income19","rent19","bachplus19","state","county","GEOID"])

#%% Write 2019 data to a csv file
data2019.to_csv("Suffolk_2019.csv")








