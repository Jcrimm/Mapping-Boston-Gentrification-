# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:06:43 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

# Trial import
api = 'https://api.census.gov/data/2020/acs/acs5'
#Select all counties
for_clause = 'county:*'
#no in clause because looking at entire country
key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"
payload = {'get':"NAME,B01001_001E,B08201_001E", 'for':for_clause,'key':key_value}
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




