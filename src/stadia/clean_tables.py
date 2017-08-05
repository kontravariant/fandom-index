# -*- coding: utf-8 -*-

import os
import pandas as pd
import re

attendPath = "../../data/process/attend"



##---- Clean Attendance Tables ----##
attendDict = dict()
for datfile in os.listdir(attendPath):
    league = datfile.split("_")[0]
    attendDict[league] = pd.read_csv(os.path.join(attendPath,datfile), thousands=',')


def clean_attendance(attends):
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
            attends[league] = dtable.loc[:30,:] # Cut off text rows

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

        if league == 'nhl':
            pass #Clean Already
    return

##---- Clean Capcity Tables ----##
capPath = "../../data/process/capacity"
capDict = dict()
for datfile in os.listdir(capPath):
    league = datfile.split("_")[0]
    capDict[league] = pd.read_csv(os.path.join(capPath,datfile), thousands=',')

def clean_capacities(caps):
    for league, dtable in caps.items():
        if league == 'nba':
            LAregex = re.compile(r"^([0-9||,]+) (.+) ([0-9||,]+) (.+)$")
            dtable = dtable.ix[:,0:4]
            staple = dtable.loc[dtable['Arena']=='Staples Center']
            dtable.loc[dtable['Arena']=='Staples Center','Team(s)'] = 'Los Angeles Clippers'
            clipsCap = LAregex.search(dtable.loc[dtable['Arena'] == 'Staples Center']['Capacity'].item()).groups()[0].replace(',','')
            lakerCap = LAregex.search(dtable.loc[dtable['Arena'] == 'Staples Center']['Capacity'].item()).groups()[2].replace(',','')
            dtable.loc[dtable['Arena'] == 'Staples Center','Capacity'] = clipsCap
            staple['Team(s)'] = 'Los Angeles Lakers'
            staple['Capacity'] = lakerCap
            dtable = dtable.append(staple)
            dtable.sort_values(by='Arena',inplace=True)
            caps[league] = dtable

        if league == 'mlb':
            pass

        if league == 'nfl':
            pass

        if league == 'nhl':
            pass

    return
#print(capacities)


devel = True
if devel == True:
    league = 'nhl'
    attendDict = {league: attendDict[league]}
    clean_capacities(capDict)
    #print(capDict)