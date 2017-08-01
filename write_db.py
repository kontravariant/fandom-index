import sqlite3 as s3
import pandas as pd
import os

datadir = "./data/process"
dataname = "census_concat.csv"
datafile = os.path.join(datadir, dataname)

# read csv
dframe = pd.read_csv(datafile, header=0, index_col=False)
print(dframe.head())
# connect to sqlite db
con = s3.connect("fandom.sqlite")
# write dframe to db
dframe.to_sql("census", con, if_exists='replace', index=False)
