# -*- coding: utf-8 -*-

import os
import pandas as pd
import re
import sqlite3 as s3


attendPath = "../../data/process/attend"
capPath = "../../data/process/capacity"
sqlitePath = "../../fandom.sqlite"

##---- Clean Attendance Tables ----##
def clean_attendance():
    attendDict = dict()
    for datfile in os.listdir(attendPath):
        league = datfile.split("_")[0]
        attendDict[league] = pd.read_csv(os.path.join(attendPath, datfile), thousands=',')
        
    for league, dtable in attendDict.items():
        if league == 'nba':
            dtable = dtable.loc[-(
                    dtable['TEAM NAME'].isnull() | # is null or contains these strings
                    dtable['TEAM NAME'].str.contains('National|TOTAL|----')
                    )]
            for cols in dtable:
                if ("TOTAL" in cols or "AVG" in cols):
                    dtable.loc[:,cols] = dtable[cols].str.replace(",","").copy()

            dtable.drop(['HOME GAMES','AWAY GAMES'], inplace=True, axis=1)

            dtable.columns = ['Team', 'Total Home', 'Avg Home', 'Total Away', 'Avg Away', 'Year']
            dtable['League'] = league.upper()
            attendDict[league] = dtable


        if league == 'mlb':
            dtable = dtable.iloc[:30,:9] # Cut off text rows
            dtableM = pd.melt(dtable, id_vars=['Team','Ballpark'], value_vars=['2010','2011','2012','2013','2014','2015','2016'])
            dtableM.columns = ['Team','Stadium','Year','Total Home']
            attendDict[league] = dtableM

        if league == 'nfl':
            numCols = ['AVERAGE ATTENDANCE', 'TOTAL ATTENDANCE']
            for colname in numCols:
                dtable.loc[:,colname].replace(inplace=True,regex=True,to_replace=r'\D',value=r'')
#           dtableM = pd.melt(dtable,id_vars=['TEAM','STADIUM','YEAR'],value_vars=['TOTAL ATTENDANCE','AVERAGE ATTENDANCE'])
            dtable.columns = ['Team','Stadium','Avg Home','Total Home','Year']
            dtable['Stadium'] = dtable['Stadium'].str.replace(r'(\?{3})','-')
            dtable['Stadium'] = dtable['Stadium'].str.replace(r'(\*{2})', '')
            dtable['League'] = league.upper()
            attendDict[league] = dtable

        if league == 'nhl':
            dtable.columns = ['Team','Stadium','Avg Home','Total Home','Year']
            dtable['League'] = league.upper()
            attendDict[league] = dtable

    attframes = [frame for frame in attendDict.values()]
    allAtt = pd.concat(attframes)
    return(allAtt)

##---- Clean Capcity Tables ----##
def clean_capacities():
    capDict = dict()
    for datfile in os.listdir(capPath):
        league = datfile.split("_")[0]
        capDict[league] = pd.read_csv(os.path.join(capPath, datfile), thousands=',')

    for league, dtable in capDict.items():
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
            dtable.columns = ["Stadium","Location","Team","Capacity"]
            capDict[league] = dtable

        if league == 'mlb':
            dtable = dtable.ix[:,[0,1,2,4]]
            seating = dtable.ix[:,1]
            seating = seating.str.replace(",","") # remove commas
            seating = seating.str.replace("\[\d+\]$","") # remove ref brackets
            dtable.ix[:,1] = seating

            teams = dtable.ix[:,3]
            teams = teams.str.replace("\[(.+)\]$","")
            dtable.ix[:,3] = teams
            dtable.columns = ["Stadium", "Capacity", "Location", "Team"]
            capDict[league] = dtable


        if league == 'nfl':
            dtable = dtable.ix[:,[0,1,2,5]]

            dtable.columns = ["Stadium", "Capacity", "Location", "Team"]
            capDict[league] = dtable

        if league == 'nhl':
            dtable = dtable.ix[:,[0,1,2,3]]
            dtable.columns = ["Stadium", "Location", "Team", "Capacity"]
            capDict[league] = dtable

        dtable['League'] = league.upper() # for every table, give a league column for long format indicator

    capframes = [frame for frame in capDict.values()]
    allCaps = pd.concat(capframes)

    return(allCaps)


def write_stadi_tables(cleanAttend=None, cleanCap=None):
    # connect to sqlite db
    con = s3.connect(sqlitePath)
    # write dframe to db
    cleanAttend.to_sql("attendance", con, if_exists='replace', index=False)
    cleanCap.to_sql("capacity", con, if_exists='replace', index=False)


attFrame = clean_attendance()
capFrame = clean_capacities()

write_stadi_tables(cleanAttend=attFrame, cleanCap=capFrame)