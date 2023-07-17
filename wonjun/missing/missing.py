import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns

def convert_to_datetime(date_str):
    if "Fall" in date_str:
        year = date_str.split(" ")[-1]
        return pd.to_datetime(f"{year}-09-01")
    else:
        try:
            return pd.to_datetime(date_str, format='%d/%m/%Y', errors='raise')
        except ValueError:
            return pd.to_datetime(date_str, errors='coerce')

# Load data
ufo_df = pd.read_csv('../../data/ufo_after/complete_after.csv')
missing_df = pd.read_csv('../../data/missing/Missing Females.csv',  encoding='ISO-8859-1')

# Preprocess UFO data
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'])
ufo_df['time'] = pd.to_datetime(ufo_df['time'], format='%H:%M').dt.time
ufo_df['latitude'] = pd.to_numeric(ufo_df['latitude'])
ufo_df['longitude'] = pd.to_numeric(ufo_df['longitude'])
ufo_df = ufo_df[['datetime', 'time', 'latitude', 'longitude']]

# Preprocess missing data
missing_df['Date'] = missing_df['Date'].astype(str)
missing_df = missing_df[~missing_df['Date'].str.contains('Seattle, Washington')]
missing_df['Date'] = missing_df['Date'].replace({'Februrary 8, 1992': 'February 8, 1992', 'Deptember 17, 1992': 'September 17, 1992'})
missing_df['Date'] = missing_df['Date'].apply(convert_to_datetime)
missing_df['latitude'] = pd.to_numeric(missing_df['latitude'])
missing_df['longitude'] = pd.to_numeric(missing_df['longitude'])
missing_df = missing_df[['Date', 'latitude', 'longitude']]

# Rename columns for merge
missing_df.rename(columns={'Date': 'datetime'}, inplace=True)

# Drop rows with NaN values
ufo_df = ufo_df.dropna(subset=['datetime'])
missing_df = missing_df.dropna(subset=['datetime'])

# Merge data
merged_df = pd.merge_asof(ufo_df.sort_values('datetime'), missing_df.sort_values('datetime'), on='datetime')

# Drop rows with NaN values
merged_df = merged_df.dropna()

# Calculate the distance between the UFO sightings and missing persons
merged_df['distance'] = merged_df.apply(lambda row: geodesic((row['latitude_x'], row['longitude_x']),
                                                             (row['latitude_y'], row['longitude_y'])).km, axis=1)

# Print the mean distance
print('Mean distance:', merged_df['distance'].mean())

# Plot histogram of distances
plt.hist(merged_df['distance'], bins=50)
plt.title('Histogram of Distances between UFO sightings and Missing Persons')
plt.xlabel('Distance')
plt.ylabel('Count')
plt.savefig('missing1.png', dpi=600)
# plt.show()

# Scatter Plot for Locations of UFO Sightings and Missing Persons
plt.figure(figsize=(10, 6))
plt.scatter(ufo_df['longitude'], ufo_df['latitude'], color='blue', alpha=0.5, label='UFO sightings')
plt.scatter(missing_df['longitude'], missing_df['latitude'], color='red', alpha=0.5, label='Missing persons')
plt.legend()
plt.title('Locations of UFO Sightings and Missing Persons')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('missing2.png', dpi=600)
# plt.show()

# Calculate and print the correlation matrix
correlation_matrix = merged_df[['latitude_x', 'longitude_x', 'latitude_y', 'longitude_y', 'distance']].corr()
print(correlation_matrix)

# Heatmap for Correlation Matrix
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix Heatmap')
plt.savefig('missing3.png', dpi=600)
# plt.show()

# Calculate the proportion of UFO sightings and missing persons events that occurred within a certain distance
threshold_distance = 100  # you can adjust this value
close_events = merged_df[merged_df['distance'] < threshold_distance]
proportion_close = len(close_events) / len(merged_df)

print(f"Proportion of events within {threshold_distance} km: {proportion_close}")

# Time Series Plot
plt.figure(figsize=(10, 6))
ufo_df['datetime'].value_counts().resample('M').sum().plot(label='UFO sightings')
missing_df['datetime'].value_counts().resample('M').sum().plot(label='Missing persons')
plt.legend()
plt.title('Time Series of UFO Sightings and Missing Persons')
plt.xlabel('Time')
plt.ylabel('Count')
plt.savefig('missing3.png', dpi=600)
# plt.show()
