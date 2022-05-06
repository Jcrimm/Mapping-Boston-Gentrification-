# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:31:55 2022

@author: jerem
"""

#%% Initial set up
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#bring in the boston gentrification data
gent = pd.read_csv("boston_gent.csv", dtype={"GEOID":str})

#set index to GEOID
gent.set_index("GEOID",inplace=True)

#drop the geographic data we don't need
drop = ["Unnamed: 0","ALAND","AWATER","geometry"]
gent = gent.drop(columns=drop)

#drop the block groups that don't have a gentrification index
missing = ["gent_index(w/race)","gent_index(norace)"]
gent = gent[missing].dropna()

#%% Now sort the values by the two gentrification indexes and assign values

#sort the values by gentrification index with race and then assign values by the rank 
gent = gent.sort_values("gent_index(w/race)")
gent["rank1"] = range(1,len(gent)+1)

#sort values by gentrification index without race and then assign values by ranking
gent = gent.sort_values("gent_index(norace)")
gent["rank2"] = range(1,len(gent)+1)

#%% How are the two indexes correlated?

#pearson
trim = gent[['rank1','rank2']]
corr_pearson = trim.corr(method='pearson')
print(f"The Pearson Correlation btwn Indexes: {corr_pearson}")

#use spearman
trim = gent[['rank1','rank2']]
corr_spearman = trim.corr(method='spearman')
print(f"The Spearman Correlation btwn Indexes: {corr_spearman}")

#%% plot the correlation
plt.rcParams['figure.dpi'] = 300

fg = sns.regplot('rank1',
            'rank2',
            data=gent,
            x_ci='ci',
            ci=95)

fg.set(xlabel='Gentrification Index with Race',
       ylabel='Gentrification Index Without Race',
       title='Correlation of Gentrification Indexes')

fg.figure.tight_layout()
fg.figure.savefig("Gent_Index_Regplot.png")




                
                            




