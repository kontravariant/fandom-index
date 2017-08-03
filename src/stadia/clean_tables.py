# -*- coding: utf-8 -*-

import os
import pandas as pd

attendPath = "../../data/process/attend"
capPath = "../../data/process/capacity"

attends = dict()
for datfile in os.listdir(attendPath):
    league = datfile.split("_")[0]
    attends[league] = pd.read_csv(os.path.join(attendPath,datfile), thousands=',')
    
for league, dtable in attends.items():
    if league == 'nba':
        dtable = dtable.loc[-(
                dtable['TEAM NAME'].isnull() | # is null or contains these strings
                dtable['TEAM NAME'].str.contains('National|TOTAL|----')
                )]
        for cols in dtable:
            if ("TOTAL" in cols or "AVG" in cols):
                print(cols)
                dtable[cols] = dtable[cols].str.replace(",","")
        attends[league] = dtable
    
    ######if league == 'mlb':
            