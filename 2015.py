# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 18:56:23 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Create API Request

api = 'https://api.census.gov/data/2015/acs/acs5'

#Select tracts of interest--only those in Boston! 
for_clause = {"tract":tract_string2010}

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

#%%Set row list
row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2015 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
columns2015 = {"B01001_001E":"pop2015","B03002_002E":"white2015","B19013_001E":"income2015","B25064_001E":"rent2015"}
data2015 = data2015.rename(columns=columns2015)

#set index to tract
data2015.set_index("tract",inplace=True)

#convert columns from strings to integers
numbers = ["pop2015","white2015","income2015","rent2015"]
data2015[numbers] = data2015[numbers].astype(int)