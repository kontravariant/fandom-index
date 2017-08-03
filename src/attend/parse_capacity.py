from bs4 import BeautifulSoup
import os
import re
import pandas as pd

cap_outPath = "../../data/process/cap"
cap_htmlPath = "html/cap"

leagueDict = dict()
for fname in os.listdir(cap_htmlPath):
    leagueName = fname.split('_cap.')[0]
    with open(os.path.join(cap_htmlPath,fname), 'r') as htmlFile:
        html = htmlFile.read()
    leagueDict[leagueName] = html

devel = False
# debug parameters
if devel == True:
    ltest = 'mlb'
    leagueDict = {ltest: leagueDict[ltest]}

# output path
writepath = "../../data/process/capacity"
# set up year regex
yearRe = re.compile(r'((19|20)\d{2})')
for league, html in leagueDict.items(): # iterate over each league and html page
    print(league)
    soup = BeautifulSoup(html, 'html.parser') # soupify
    tbl = soup.select("table.wikitable.sortable") # use css selector
    pdDframe = pd.read_html(str(tbl), header=0, flavor='lxml')[0].iloc[:,1:] # slice after image col
    pdDframe.to_csv(os.path.join(writepath,"{0}_cap.csv".format(league)),index=False) # write to csv
