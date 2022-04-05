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

#%% Create API request for 2020 ACS 5-year estimate

# Trial import
api = 'https://api.census.gov/data/2020/acs/acs5'
#Variables of interest
#"NAME"
#""B01001_001E": total population
#"B01001A_001E": white alone
#"B01001B_001E" black alone
#"B01001D_001E" asian alone
#"B01001G_001E" two or more races
#"B01001I_002E" hispanic alone
#"B06011_001E" median income in the last 12 months
#"B25113_001E" median gross rent by when person moved into unit

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




