import pandas as pd

# load data files
UFO_complete_df = pd.read_csv('./data/ufo/complete.csv', on_bad_lines='skip')
UFO_scrubbed_df = pd.read_csv('./data/ufo/scrubbed.csv', on_bad_lines='skip')
AAL_df = pd.read_csv('./data/airline_stock/AAL.csv', on_bad_lines='skip')
DAL_df = pd.read_csv('./data/airline_stock/DAL.csv', on_bad_lines='skip')
LUV_df = pd.read_csv('./data/airline_stock/LUV.csv', on_bad_lines='skip')
UAL_df = pd.read_csv('./data/airline_stock/UAL.csv', on_bad_lines='skip')


# variable identification
# print('UFO_complete_df.head', UFO_df.head(), sep="\n")
# print('AAL_df.head', AAL_df.head(), sep="\n")


# count missing value in each column 
print(UFO_complete_df.isna().sum())
print(UFO_scrubbed_df.isna().sum())

# remove each row which has missing value
UFO_complete_df = UFO_complete_df.dropna()
UFO_scrubbed_df = UFO_scrubbed_df.dropna()
AAL_df = AAL_df.dropna()
DAL_df = DAL_df.dropna()
LUV_df = LUV_df.dropna()
UAL_df = UAL_df.dropna()

# visualize each dataframe's distribution

