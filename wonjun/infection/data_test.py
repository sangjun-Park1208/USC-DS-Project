import pandas as pd

# 이 부분을 추가해서 pandas 출력 설정을 변경합니다.
pd.set_option('display.max_rows', None)

# 가정: CSV 파일에는 헤더가 있으며 그 이름은 'datetime', 'time', 'city', 'state', 'country', 'shape', 'duration', 'latitude', 'longitude'입니다.
ufo_data = pd.read_csv('../../data/ufo_after/complete_after.csv')

ufo_data['datetime'] = pd.to_datetime(ufo_data['datetime'], errors='coerce')

ufo_data = ufo_data[['datetime', 'city', 'state', 'country', 'shape', 'latitude', 'longitude']]

ufo_data = ufo_data.dropna()

ufo_data['Year'] = ufo_data['datetime'].dt.year

ufo_counts_by_year = ufo_data.groupby('Year').size().reset_index(name='UFO_counts')

print("UFO sightings by year:\n")
print(ufo_counts_by_year)

# IQR method for outlier detection
Q1 = ufo_counts_by_year['Year'].quantile(0.25)
Q3 = ufo_counts_by_year['Year'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = ufo_counts_by_year[(ufo_counts_by_year['Year'] < lower_bound) | (ufo_counts_by_year['Year'] > upper_bound)]
print("\nOutlier Years:\n")
print(outliers)

# 연도별 UFO 발견 횟수가 6000건 이상인 연도
ufo_counts_above_6000 = ufo_counts_by_year[ufo_counts_by_year['UFO_counts'] >= 6000]
print("\nYears with 6000 or more sightings:\n")
print(ufo_counts_above_6000)
