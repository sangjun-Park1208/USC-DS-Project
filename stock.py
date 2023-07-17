import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

# load data files
UFO_complete_df = pd.read_csv('./data/ufo/complete.csv', 
                              on_bad_lines='skip', 
                              dtype={
                                  'datetime': str,
                                  'city': str,
                                  'state': str,
                                  'country': str,
                                  'shape': str,
                                  'duration (seconds)': str,
                                  'duration (hours/min)': str,
                                  'comments': str,
                                  'date posted': str,
                                  'latitude': str,
                                  'longitude': str,
                                  }
                              )
UFO_scrubbed_df = pd.read_csv('./data/ufo/scrubbed.csv', 
                              on_bad_lines='skip',
                              dtype={
                                  'datetime': str,
                                  'city': str,
                                  'state': str,
                                  'country': str,
                                  'shape': str,
                                  'duration (seconds)': str,
                                  'duration (hours/min)': str,
                                  'comments': str,
                                  'date posted': str,
                                  'latitude': str,
                                  'longitude': str,
                                  }
                              )
AAL_df = pd.read_csv('./data/airline_stock/AAL.csv', on_bad_lines='skip')
DAL_df = pd.read_csv('./data/airline_stock/DAL.csv', on_bad_lines='skip')
LUV_df = pd.read_csv('./data/airline_stock/LUV.csv', on_bad_lines='skip')
UAL_df = pd.read_csv('./data/airline_stock/UAL.csv', on_bad_lines='skip')

# variable identification
# print('UFO_complete_df.head', UFO_df.head(), sep="\n")
# print('AAL_df.head', AAL_df.head(), sep="\n")


# count missing value in each column 
# print(UFO_complete_df.isna().sum())
# print(UFO_scrubbed_df.isna().sum())

# remove each row which has missing value
UFO_complete_df = UFO_complete_df.dropna()
UFO_scrubbed_df = UFO_scrubbed_df.dropna()
AAL_df = AAL_df.dropna()
DAL_df = DAL_df.dropna()
LUV_df = LUV_df.dropna()
UAL_df = UAL_df.dropna()

# sort dataframe by date format 'yyyy/mm/dd' & remove time element in datetime column
UFO_complete_df = UFO_complete_df.sort_values(by='datetime')
UFO_scrubbed_df = UFO_scrubbed_df.sort_values(by='datetime')

UFO_complete_df['datetime'] = pd.to_datetime(UFO_complete_df['datetime'], errors='coerce', format='%m/%d/%Y %H:%M').dt.date
UFO_scrubbed_df['datetime'] = pd.to_datetime(UFO_scrubbed_df['datetime'], errors='coerce', format='%m/%d/%Y %H:%M').dt.date

UFO_complete_df = UFO_complete_df.dropna(subset=['datetime'])
UFO_scrubbed_df = UFO_scrubbed_df.dropna(subset=['datetime'])

UFO_complete_df['datetime'] = pd.to_datetime(UFO_complete_df['datetime'], format='%Y/%m/%d')
UFO_scrubbed_df['datetime'] = pd.to_datetime(UFO_scrubbed_df['datetime'], format='%Y/%m/%d')

UFO_complete_df['datetime'] = UFO_complete_df['datetime'].dt.strftime('%Y/%m/%d')
UFO_scrubbed_df['datetime'] = UFO_scrubbed_df['datetime'].dt.strftime('%Y/%m/%d')

print('UFO_complete_df.head', UFO_complete_df.head(), sep="\n")
print('UFO_scrubbed_df.head', UFO_scrubbed_df.head(), sep="\n")


# visualize each dataframe's distribution
city_count = UFO_complete_df['city'].value_counts()
top_10 = city_count.nlargest(50)

country_count = UFO_complete_df['country'].value_counts()
top_50 = country_count.nlargest(50)
# print(type(city_count))

top_10.plot(kind='bar')
plt.xlabel('City')
plt.ylabel('Count')
plt.title('Cities UFO Frequence')
plt.show()

top_50.plot(kind='bar')
plt.xlabel('Country')
plt.ylabel('Count')
plt.title('Countries UFO Frequence')
plt.show()

# fig, ax = plt.subplots()
# city_count.plot(kind='bar', ax=ax)

# # 축 및 제목 설정
# ax.set_xlabel('datetime')
# ax.set_ylabel('city Frequency')
# ax.set_title('Distribution of city Frequency')

# # 그래프 표시
# plt.show()