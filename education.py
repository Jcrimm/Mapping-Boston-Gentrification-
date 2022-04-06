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
attainment = education["unique_ID"].to_list()

#add "E" to to the end of each value in education
attainment = [n + "E" for n in attainment]