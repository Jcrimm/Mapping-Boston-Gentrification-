# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:06:43 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Trial import censsus tracts of interest
boston = pd.read_csv("census-tract-data.csv",dtype=str)
#keep all rows except first one
boston = boston.iloc[1:]
tracts = boston["TRACT"].to_list()
tract_string = ",".join(tracts)


#%%
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
#Select Massachusetts
for_clause = tract_string
#Select tracts of interest
in_clause = "state:25"
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




