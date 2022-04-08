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


#%% Bring in Variables of interest excluding education

#Variables of interest (Table Shells)
#"NAME"
#B01001_001E": total population
#"B03002_002E" : Not Hispanic or Latino: White Alone
#"B19013_001E" median income in the last 12 months, inflation adjusted
#"B25064_001E": Median Rent

#Create a list of all the variables we want, exluding education.
var_list = ["NAME","B01001_001E","B03002_002E","B19013_001E","B25064_001E"]

#create a string for all the variables
var_string = ",".join(var_list)


#%% Create API request for 2020 ACS 5-year estimate


# Trial import
api = 'https://api.census.gov/data/2020/acs/acs5'

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

#%%
#Set row list
row_list = response.json()

#Set colnames to the first row of row_list via row_list[0]
colnames = row_list[0]

#Set datarows to the remaining rows via row_list[1:]
datarows = row_list[1:]

#Convert the data into a Pandas dataframe
data2020 = pd.DataFrame(columns=colnames, data=datarows)

#rename columns
columns2020 = {"B01001_001E":"pop2020","B03002_002E":"white2020","B19013_001E":"income2020","B25064_001E":"rent2020"}
data2020 = data2020.rename(columns=columns2020)

#set index to tract
data2020.set_index("tract",inplace=True)

#convert columns from strings to integers
numbers = ["pop2020","white2020","income2020","rent2020"]
data2020[numbers] = data2020[numbers].astype(int)

#%%
#Check how many tracts don't have any population
missing = data2020.query("pop2020==0").count()
print(f"Tracts with no population: {missing} \n")

#negative income or rent
negative = data2020.query("income2020<=0 and rent2020<=0")
print(f"Tracts with negative income or rent: {negative.index} \n")






