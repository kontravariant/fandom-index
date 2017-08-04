# -*- coding: utf-8 -*-

import os
import pandas as pd

attendPath = "../../data/process/attend"
capPath = "../../data/process/capacity"

##---- Clean Attendance Tables
attends = dict()
for datfile in os.listdir(attendPath):
    league = datfile.split("_")[0]
    attends[league] = pd.read_csv(os.path.join(attendPath,datfile), thousands=',')

devel = True
if devel == True:
    league = 'nfl'
    attends = {league: attends[league]}

for league, dtable in attends.items():
    if league == 'nba':
        dtable = dtable.loc[-(
                dtable['TEAM NAME'].isnull() | # is null or contains these strings
                dtable['TEAM NAME'].str.contains('National|TOTAL|----')
                )]
        for cols in dtable:
            if ("TOTAL" in cols or "AVG" in cols):
                dtable.loc[:,cols] = dtable[cols].str.replace(",","").copy()

        dtable.drop(['HOME GAMES','AWAY GAMES'], inplace=True, axis=1)
        if devel == True:
            print(dtable)
        attends[league] = dtable
    
    if league == 'mlb':
        attends[league] = dtable.loc[:30,:]

        if devel == True:
            print(attends[league])

    if league == 'nfl':
        numCols = ['AVERAGE ATTENDANCE', 'TOTAL ATTENDANCE']
        for colname in numCols:
            dtable.loc[:,colname].replace(inplace=True,regex=True,to_replace=r'\D',value=r'')
            dtableM = pd.melt(dtable,id_vars=['TEAM','STADIUM'],value_vars=['TOTAL ATTENDANCE','AVERAGE ATTENDANCE'])
        if devel == True:
            print(dtableM)
        attends[league] = dtableM

    ###-----
        # if league == 'nhl':


            