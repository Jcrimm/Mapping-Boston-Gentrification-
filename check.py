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

#%% Now create relplot of both rankings to see if they match up

plt.rcParams['figure.dpi'] = 300

fg = sns.relplot(data=gent,
                 x='rank1',
                 y='rank2',
                 palette="paired",
                 facet_kws={'despine':False,"subplot_kws":{'title':'Scatter Gentrification Indexes'}})

fg.set_axis_labels('Gentrification Index with Race','Gentrification Index Without Race')

fg.tight_layout()
fg.savefig('Gent_Index_relplot.png')

#%% Create a scatterplot

fig1,ax1 = plt.subplots()
gent.plot.scatter("rank1","rank2",ax=ax1)
ax1.set_xlabel('Gentrification Index with Race')
ax1.set_ylabel('Gentrification Index Without Race')
ax1.set_title('Correlation of Gentrification Indexes')
fig1.tight_layout()
fg.savefig('Gent_Index_scatter.png')




                
                            




