import sqlite3 as s3
import pandas as pd
import os

processdir = "data/process"
dataname = "census_concat.csv"
datafile = os.path.join(processdir, dataname)

# read csv
dframe = pd.read_csv(datafile, header=0, index_col=False)
dframe = dframe.sort_values(["Id2","YEAR"],ascending = [True, False])
# connect to sqlite db
con = s3.connect("data/fandom.sqlite")
# write dframe to db
dframe.to_sql("census", con, if_exists='replace', index=False)
