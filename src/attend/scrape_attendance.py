import requests
import json

linksFile = "attendance_links.json"
with open(linksFile, 'r') as json_file:
    linkDict = json.load(json_file)
    json_file.close()
print(linkDict)

soupDict = dict()
for league, htmlref in linkDict.items():
    r = requests.get(htmlref)
    if r.status_code == 200:
        with open("html/att/{0}.html".format(league), 'w') as curfile:
            contents = r.text
            curfile.write(contents)

capFile = "capacity_links.json"
with open(capFile, 'r') as json_file:
    linkDict = json.load(json_file)
    json_file.close()
print(linkDict)

capDict = dict()
for league, htmlref in linkDict.items():
    r = requests.get(htmlref)
    if r.status_code == 200:
        with open("html/cap/{0}.html".format(league), 'w') as curfile:
            contents = r.text
            curfile.write(contents)

