import sqlite3 as s3
import pandas as pd

con = s3.connect("fandom.sqlite")

test = pd.read_sql("SELECT * FROM census", con)
print(test.head())
