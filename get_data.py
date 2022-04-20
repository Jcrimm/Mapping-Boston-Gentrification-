# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:35:00 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

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

#%% Create API request for ACS five year estimate

# Import
api = 'https://api.census.gov/data/2019/acs/acs5'

#Select tracts of interest--only those in Boston! 
#for_clause = {"tract":tract_string2010}
#other for_clause: all tracts in Suffolk County
for_clause = "block group:*"

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

#%%#%% Convert to a dataframe

# Create a row list to hold all the data
row_list = response.json()

#Set the first row to be variable/column names
colnames = row_list[0]

#Set the rest of the rows to be observations
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2019 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
col_names = {"B01001_001E":"pop",
           "B03002_002E":"white",
           "B19013_001E":"income",
           "B25064_001E":"rent",
           "B15003_001E": "totaled",
           "B15003_022E": "bachelors",
           "B15003_023E":"masters",
           "B15003_024E": "professional", 
           "B15003_025E": "doctorate"}
data2019 = data2019.rename(columns=col_names)

#create GEOID
data2019["GEOID"] =  data2019["state"] + data2019["county"] + data2019["tract"] + data2019["block group"]

#drop state, county, tract and block group variables
drop_cols = ["NAME","state","county","tract","block group"]
data2019 = data2019.drop(columns=drop_cols)

#set index to GEOID
data2019.set_index("GEOID",inplace=True)

#%% Write 2019 data to csv file

data2019.to_csv("Suffolk_blckgrps_2019.csv",index=True)

#%% Now create API Request for 2014 ACS five year estimate

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

#%% Create dataframe

row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2014 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
data2014 = data2014.rename(columns=col_names)

#create GEOID
data2014["GEOID"] =  data2014["state"] + data2014["county"] + data2014["tract"] + data2014["block group"]

##drop state, county, tract and block group variables
data2014 = data2014.drop(columns=drop_cols)

#set index to GEOID
data2014.set_index("GEOID",inplace=True)

#%% Write 2014 data to CSV file
data2014.to_csv("Suffolk_blckgrps_2014.csv",index=True)

