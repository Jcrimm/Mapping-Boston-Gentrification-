# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:15:09 2022

@author: jerem
"""

#%% Initial set-up
import pandas as pd
import requests

#%% Set up variable string for education 

#"B15003" educational attainment for population over 25 (table ID)
# "B15003_001E" : total
# "B15003_022E" : bachelor's degree
# "B15003_023E" : master's degree
# "B15003_024E" : professional degree
# "B15003_025E" : doctoral degree

# create variable list
attain_list = ["NAME","B15003_001E","B15003_022E","B15003_023E","B15003_024E","B15003_025E"]
attain_string = ",".join(attain_list)

#%% Create API request for 2019 ACS

api = 'https://api.census.gov/data/2019/acs/acs5'

#Select tracts of interest--only those in Boston! 
for_clause = {"tract:*"}

#For the in clause, want Massachusetts and Suffolk County
in_clause = "state:25 county:025"

#put in census API key. 
key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"

payload = {'get': attain_string, 'for':for_clause,'in':in_clause,'key':key_value}
response = requests.get(api,payload)

#check whether it worked
if response.status_code==200:
    print(f"Success!")
else:
    print(response.status_code)
    print(response.text)
    assert False

#%% Convert into dataframe

row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
educ19 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
attaincol19 = {"B15003_001E": "total19",
           "B15003_022E": "bachelors19",
           "B15003_023E":"masters19",
           "B15003_024E": "professional19", 
           "B15003_025E": "doctorate19"}
educ19 = educ19.rename(columns=attaincol19)

# convert columns into integers
numbers = ["total19","bachelors19","masters19","professional19","doctorate19"]
educ19[numbers] = educ19[numbers].astype(int)

# calculate proportion of tract that has bachelor's degree or higher
educ19["bachplus19"] = (educ19["bachelors19"] + educ19["masters19"] + educ19["professional19"] + educ19["doctorate19"])/educ19["total19"]

#drop all number columns except proportion of tract with bachelors or higher
educ19.drop(columns = numbers,inplace=True)

#create GEOID
educ19["GEOID"] = educ19["state"] + educ19["county"] + educ19["tract"]

#write to CSV

#%%


