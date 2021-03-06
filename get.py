# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 09:35:00 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Create string of variables of interest

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

#Create a list of all the variables we want.
var_list = ["NAME","B01001_001E","B03002_002E","B19013_001E","B25064_001E","B15003_001E","B15003_022E","B15003_023E","B15003_024E","B15003_025E"]

#create a string for all the variables
var_string = ",".join(var_list)

#%% Create function for API requests and turning into dataframe

def get(year):
    api = f"https://api.census.gov/data/{year}/acs/acs5"
    for_clause = "block group:*"
    in_clause = "state:25 county:025"
    key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"
    payload = {'get': var_string, 'for':for_clause,'in':in_clause,'key':key_value}
    response = requests.get(api,payload)
    if response.status_code==200:
        print(f"Success!")
    else:
        print(response.status_code)
        print(response.text)
        assert False
    row_list = response.json()
    colnames = row_list[0]
    datarows = row_list[1:]
    year_data = pd.DataFrame(columns=colnames, data=datarows)
    return year_data
    
#%% Now run the function to get the 2014 and 2019 ACS five year estimate

#This dictionary will be used to rename the columns
col_names = {"B01001_001E":"pop",
           "B03002_002E":"white",
           "B19013_001E":"income",
           "B25064_001E":"rent",
           "B15003_001E": "totaled",
           "B15003_022E": "bachelors",
           "B15003_023E":"masters",
           "B15003_024E": "professional", 
           "B15003_025E": "doctorate"}

#This list will be the columns no longer needed after creating the GEOID
drop_cols = ["NAME","state","county","tract","block group"]

#create a list of the years we want the five year ACS estimate for
years = [2014,2019]

#loop over each year
#apply the get function, rename columns, create GEOID and drop columns not needed anymore
#set index to GEOID and then save to a csv file
for year in years:
    year_data = get(year)
    year_data = year_data.rename(columns=col_names)
    year_data["GEOID"] = year_data["state"] + year_data["county"] + year_data["tract"] + year_data["block group"]
    year_data = year_data.drop(columns=drop_cols)
    year_data.set_index("GEOID",inplace=True)
    year_data.to_csv(f"Suffolk_blckgrps_{year}.csv",index=True)

