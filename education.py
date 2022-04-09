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

# For education, want the full table. Let's select all the variables using the table shell csv file
table = pd.read_csv("ACS2020_Table_Shells.csv",dtype=str)
#rename columns so they don't have spaces
table = table.rename(columns={"Table ID":"table_ID","Unique ID":"unique_ID"})
#select rows for educational attainment for populaton over 25
education = table.query("table_ID == 'B15003'")
#drop first two rows
education = education.iloc[2:]
#write the remaining variables to a list
attain = education["unique_ID"].to_list()

#add "E" to to the end of each value in education
attain = [n + "E" for n in attain]

#Add "NAME" to the list and then create a string for the api request
attain = ["NAME"] + attain
attain_string = ",".join(attain)

#%% Create API request

api = 'https://api.census.gov/data/2015/acs/acs5'

#Select tracts of interest--only those in Boston! 
for_clause = {"tract":tract_string2010}

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
educ2020 = pd.DataFrame(columns=colnames, data=datarows)

