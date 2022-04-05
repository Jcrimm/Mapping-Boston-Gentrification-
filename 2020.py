# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:06:43 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Create a string that has all census tracts of interest

#Import "census-tract-data.csv", which has basic information on all the censsu tracts in Boston. 
# For now, let's just use the GEOID, GEOCODE, STATE, COUNTY, and TRACT columns.
#use argument dtype=str to import them as strings
boston = pd.read_csv("census-tract-data.csv",usecols=['GEOID','GEOCODE','STATE','COUNTY','TRACT'], dtype=str)

#keep all rows except first one, which has explainers of each variable
boston = boston.iloc[1:]

#Write all the tracts to a list
tracts = boston["TRACT"].to_list()

#Join the list into one string seperated by commas.
#this will be handy for when we make the API requests
tract_string = ",".join(tracts)

#%% Bring in Variables of interest
table = pd.read_csv("ACS2020_Table_Shells.csv",dtype=str)
table = table.rename(columns={"Table ID":"table_ID","Unique ID":"unique_ID"})
#Variables of interest (Table Shells)
#"NAME"
#""B01001_001E": total population
#"B02001": Race (doesn't include Hispanic/Latino)
#"B03002": Hispanic origin
#"B19001" median income in the last 12 months
#"B15003" educational attainment for population over 25
#B25026 tenure for occupied units
#"B25063" gross rent
pop = table.query("unique_ID =='B01001_001'")
race = table.query("table_ID == 'B02001'")
hispanic = table.query("table_ID == 'B03002'")
median_income = table.query("table_ID == 'B19001'")
education = table.query("table_ID == 'B15003'")
tenure = table.query("table_ID == 'B25026'")
rent = table.query("table_ID == 'B25063'")


#%% Create API request for 2020 ACS 5-year estimate


# Trial import
api = 'https://api.census.gov/data/2020/acs/acs5'

#Select tracts of interest--only those in Boston! 
for_clause = {"tract":tract_string}

#For the in clause, want Massachusetts and Suffolk County
in_clause = "state:25 County:025"
key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"
payload = {'get':"NAME,B01001_001E,B08201_001E", 'for':for_clause,'in':in_clause,'key':key_value}
response = requests.get(api,payload)

#check whether it worked
if response.status_code==200:
    print(f"Success!")
else:
    print(response.status_code)
    print(response.txt)
    assert False

#%%
#Set row list
row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
cars_2020 = pd.DataFrame(columns=colnames, data=datarows)

#rename population and cars
cars_2020 = cars_2020.rename(columns={"B01001_001E":"Population","B08201_001E":"Cars"})

#convert population and cars into integers
cars_2020["Population"] = cars_2020["Population"].astype(float)
cars_2020["Cars"] = cars_2020["Cars"].astype(float)

#create cars per population
cars_2020["cars_per_person"] = cars_2020["Cars"]/cars_2020["Population"]




