import pandas as pd
import os

# get list of just csv's of interest
data_dir = 'data/'
process_dir = os.path.join(data_dir, 'process')
census_dir = os.path.join(data_dir, 'raw/census')
census_list = os.listdir(census_dir)
datafile_list = list()
for f in census_list:
    if f.endswith("nn.csv"):
        # append csvs to list for reading
        datafile_list.append(f)

# read metadata
metadata_fname = "meta2015.csv"
mdata_loc = os.path.join(process_dir, metadata_fname)  # metadata file location
mdata = pd.read_csv(mdata_loc, header=None)  # read metadata, simple table
rowdex = mdata[mdata[3] == 'X'].index.tolist()  # get all rows flagged with 'X'
colnames = mdata[2].iloc[rowdex]
# del colnames['index']

for r, val in colnames.iteritems():
    if pd.isnull(val):
        colnames[r] = mdata[1][r]

colnames = colnames.tolist()
# TODO: make rowdex subset by ANY string, i.e. not("")


frame_list = list()
for fname in datafile_list:  # for all data csv's
    f_loc = os.path.join(census_dir, fname)
    yr_x = '20{00}'.format(fname[4:6])  # get year from file name
    infile = pd.read_csv(f_loc, header=None, skiprows=2, names=colnames, usecols=rowdex)
    infile['YEAR'] = yr_x  # add year indicator column
    frame_list.append(infile)  # add to list of frames

# concatenate all years together, reset index and write to csv
outfile = pd.concat(frame_list)
outfile = outfile.reset_index()
del outfile['index']
outname = "census_concat.csv"
outpath = os.path.join(process_dir, outname)
outfile.to_csv(outpath, index=False)





# pd.read_excel()
