import os
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

# read all attendance html files and fill dictionary with league names
leagueDict = dict()
for fname in os.listdir("html/att"):
    leagueName = fname.split('.')[0]
    with open("html/att/{0}".format(fname), 'r') as htmlFile:
        html = htmlFile.read()
    leagueDict[leagueName] = html

# debug parameters
ltest = 'mlb'
leagueDict = {ltest: leagueDict[ltest]}

# set up year regex
yearRe = re.compile(r'((19|20)\d{2})')
for league, html in leagueDict.items(): # iterate over each league and html page
    soup = BeautifulSoup(html, 'html.parser') # soupify
    if league == "nfl": # parse NFL
        attTables = dict()
        attRegex = re.compile(r'(attendance)') # get only headers with attendance, not 'notes'
        table_title = soup.find_all("span", class_="mw-headline") # find table titles
        for tbl in table_title: # loop over table titles
            year = tbl.contents[0] # get year
            if attRegex.search(year): # if year is present use this table title
                year = year.split(' ')[0] # get just the year from table title
                curTable = tbl.find_next("table") # get the neighboring table
                pdDframe = pd.read_html(str(curTable), header=0)[0].iloc[:,[0,1,3,4]] # read html table
                attTables[year] = pdDframe # save iteration to dict
        for year, tbl in attTables.items(): # add year column and concat all year frames
            tbl['year'] = year
            tbl.columns = [x.upper() for x in tbl.columns]
        longFrame = pd.concat(attTables.values())
        longFrame.to_csv("../../data/process/nfl.csv", index = False) # write to process/csv
    if league == "nba": # for nba
        tbls = soup.find("pre").text # tables are in one big '<pre>'
        for i, tbl in enumerate(tbls.split("FINAL")[1:]): # split on FINAL, tables have note text above them
            year = yearRe.search(str(tbl)).group(0) # get year from the resulting text chunk
            fname = 'text/nba_{}.txt'.format(year) # create a file name for the current year
            with open(fname,'w') as f: # save chunk to txt file
                f.write(tbl)
        attTables = list() # placeholder
        for tblFile in sorted(os.listdir("text")): # read sorted list of year table txt's
            yrTable = pd.read_fwf("text/{}".format(tblFile), widths=[30,6,10,10,6,8,8], header = None, # fixed with tables
                                  names = ['TEAM NAME', 'HOME GAMES', 'TOTAL HOME', 'AVG HOME', 'AWAY GAMES', 'TOTAL AWAY', 'AVG AWAY'])
            yrTable['YEAR'] = yearRe.search(tblFile).group(0) # table file name has year in it
            # ATL is the first team in all years, so look for its row number and cut the table starting there
            startRow = yrTable[yrTable['TEAM NAME'].str.contains("Atlanta")==True].index.tolist()
            yrTable = yrTable.iloc[startRow[0]:,:]
            # TODO: cut off rows after National Basketball Asso...
            attTables.append(yrTable) # append to list
        longFrame = pd.concat(attTables) # concat df list
        longFrame.to_csv("../../data/process/nba.csv", index = False) # write to process/csv
    if league == "mlb": # for mlb
        tbl = soup.find("table", class_="tableizer-table") # easy, well formatted HTML table
        pdDframe = pd.read_html(str(tbl), header=0)[0]  # read html table
        pdDframe.to_csv("../../data/process/mlb.csv", index = False)
    if league == "nhl": # for nhl


