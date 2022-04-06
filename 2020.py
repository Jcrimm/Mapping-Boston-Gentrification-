# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 17:06:43 2022

@author: jerem
"""

#%%
#Import modules
import pandas as pd
import requests

#%% Create a string that has all census tracts of interest (2020 tracts)

#Import "census-tract-data.csv", which has basic information on all the censsu tracts in Boston in 2020. 
# For now, let's just use the GEOID, GEOCODE, STATE, COUNTY, and TRACT columns.
#use argument dtype=str to import them as strings
boston2020 = pd.read_csv("census-tract-data.csv",usecols=['GEOID','GEOCODE','STATE','COUNTY','TRACT'], dtype=str)

#keep all rows except first one, which has explainers of each variable
boston2020 = boston2020.iloc[1:]

#Write all the tracts to a list
tracts2020 = boston2020["TRACT"].to_list()

#Join the list into one string seperated by commas.
#this will be handy for when we make the API requests
tract_string2020 = ",".join(tracts2020)

#%% Create a string that has all census tracts of interest (2010 tracts)

# Import "Census_2010_Tracts.csv" has basic information on all the censsu tracts in Boston in 2010
boston2010 = pd.read_csv("Census_2010_Tracts.csv",dtype=str)

#Write all the tracts to a list
tracts2010 = boston2010["TRACTCE10"].to_list()

#Join the list into one string seperated by commas
#this will be handy for when we make the API requests
tract_string2010 = ",".join(tracts2010)


#%% Bring in Variables of interest

#Variables of interest (Table Shells)
#"NAME"
#""B01001_001E": total population
#"B03002_002" : Not Hispanic or Latino: White Alone
#"B19013_001" median income in the last 12 months, inflation adjusted
#"B15003" educational attainment for population over 25 (table ID)
#"B25064_001": Median Rent

#Create a list of all the variables we want, exluding education.
var_list = ["NAME", "B01001_001E","B03002_002","B19013_001","B25064_001"]

# For education, want the full table. Let's select all the variables using the table shell csv file
table = pd.read_csv("ACS2020_Table_Shells.csv",dtype=str)
#rename columns so they don't have spaces
table = table.rename(columns={"Table ID":"table_ID","Unique ID":"unique_ID"})
#select rows for educational attainment for populaton over 25
education = table.query("table_ID == 'B15003'")
#drop first two rows
education = education.iloc[2:]
#write the remaining variables to a list
attainment = education["unique_ID"].to_list()

#Join the education list onto var_list
var_list.extend(attainment)

#create a string for all the variables
var_string = ",".join(var_list)


#%% Create API request for 2020 ACS 5-year estimate


# Trial import
api = 'https://api.census.gov/data/2020/acs/acs5'

#Select tracts of interest--only those in Boston! 
for_clause = {"tract":tract_string2010}

#For the in clause, want Massachusetts and Suffolk County
in_clause = "state:25 County:025"
#put in census API key. 
key_value = "0a95ea1ddf62885731b2000925bbf002a1a803c2"
payload = {'get': var_string, 'for':for_clause,'in':in_clause,'key':key_value}
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
data2020 = pd.DataFrame(columns=colnames, data=datarows)

#rename population and cars


#convert population and cars into integers

#create cars per population





