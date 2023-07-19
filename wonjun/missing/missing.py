import pandas as pd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import seaborn as sns

# 문자열로 된 날짜를 datetime 형식으로 바꾸는 함수를 정의
def convert_to_datetime(date_str):
        # 특정한 형식(예: 'd/m/Y')으로 날짜를 변환하되, 오류가 발생하면 강제로 날짜를 변환
        try:
            return pd.to_datetime(date_str, format='%d/%m/%Y', errors='raise')
        except ValueError:
            return pd.to_datetime(date_str, errors='coerce')

# UFO와 실종자료 load
ufo_df = pd.read_csv('../../data/ufo_after/complete_after.csv')
missing_df = pd.read_csv('../../data/missing/Missing Females.csv',  encoding='ISO-8859-1')

# 미국의 위도와 경도 범위를 정의
lat_range = (24.396308, 49.384358)
lon_range = (-125.000000, -66.934570)

# UFO 데이터 전처리
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'])
# 1910년에서 2014년 사이의 데이터만 선택
ufo_df = ufo_df[(ufo_df['datetime'].dt.year >= 1910) & (ufo_df['datetime'].dt.year <= 2014)]
# 'time' 컬럼을 시간 형식으로 변환
ufo_df['time'] = pd.to_datetime(ufo_df['time'], format='%H:%M').dt.time
# 'latitude'와 'longitude' 컬럼을 숫자로 변환
ufo_df['latitude'] = pd.to_numeric(ufo_df['latitude'])
ufo_df['longitude'] = pd.to_numeric(ufo_df['longitude'])

# 미국 내의 위치로 UFO 데이터를 필터링
ufo_df = ufo_df[(ufo_df['latitude'] >= lat_range[0]) & (ufo_df['latitude'] <= lat_range[1]) &
                (ufo_df['longitude'] >= lon_range[0]) & (ufo_df['longitude'] <= lon_range[1])]

# 사용할 열만 선택
ufo_df = ufo_df[['datetime', 'time', 'latitude', 'longitude']]

# 미아 데이터 전처리
missing_df['Date'] = missing_df['Date'].astype(str)
missing_df = missing_df[~missing_df['Date'].str.contains('Seattle, Washington')]
missing_df['Date'] = missing_df['Date'].replace({'Februrary 8, 1992': 'February 8, 1992', 'Deptember 17, 1992': 'September 17, 1992'})
missing_df['Date'] = missing_df['Date'].apply(convert_to_datetime)
missing_df = missing_df[(missing_df['Date'].dt.year >= 1910) & (missing_df['Date'].dt.year <= 2014)]
missing_df['latitude'] = pd.to_numeric(missing_df['latitude'])
missing_df['longitude'] = pd.to_numeric(missing_df['longitude'])

# 미국 내의 위치로 미아 데이터를 필터링
missing_df = missing_df[(missing_df['latitude'] >= lat_range[0]) & (missing_df['latitude'] <= lat_range[1]) &
                        (missing_df['longitude'] >= lon_range[0]) & (missing_df['longitude'] <= lon_range[1])]

# 사용할 열만 선택
missing_df = missing_df[['Date', 'latitude', 'longitude']]

# 병합을 위해 열 이름을 변경
missing_df.rename(columns={'Date': 'datetime'}, inplace=True)

# NaN 값을 포함하는 행을 삭제
ufo_df = ufo_df.dropna(subset=['datetime'])
missing_df = missing_df.dropna(subset=['datetime'])

# 날짜를 기준으로 데이터를 병합
merged_df = pd.merge_asof(ufo_df.sort_values('datetime'), missing_df.sort_values('datetime'), on='datetime')

# NaN 값을 포함하는 행을 삭제
merged_df = merged_df.dropna()

# UFO 목격 장소와 사람이 실종된 장소 사이의 거리를 계산
merged_df['distance'] = merged_df.apply(lambda row: geodesic((row['latitude_x'], row['longitude_x']),
                                                             (row['latitude_y'], row['longitude_y'])).km, axis=1)

# 평균 거리를 출력
print('Mean distance:', merged_df['distance'].mean())

# 거리의 히스토그램
plt.hist(merged_df['distance'], bins=50)
plt.title('Histogram of Distances between UFO sightings and Missing Persons')
plt.xlabel('Distance')
plt.ylabel('Count')
plt.savefig('missing1.png', dpi=600)

# UFO 목격 장소와 실종자 위치의 산점도
plt.figure(figsize=(10, 6))
plt.scatter(ufo_df['longitude'], ufo_df['latitude'], color='blue', alpha=0.5, label='UFO sightings')
plt.scatter(missing_df['longitude'], missing_df['latitude'], color='red', alpha=0.5, label='Missing persons')
plt.legend()
plt.title('Locations of UFO Sightings and Missing Persons')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('missing2.png', dpi=600)

# 상관 행렬을 계산하고 출력
correlation_matrix = merged_df[['latitude_x', 'longitude_x', 'latitude_y', 'longitude_y', 'distance']].corr()
print(correlation_matrix)

# 상관 행렬의 히트맵
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix Heatmap')
plt.savefig('missing3.png', dpi=600)

# 임계값을 설정
threshold_distance = 100  # km
# 임계값 내에 있는 사건의 수를 계산
close_events = merged_df[merged_df['distance'] < threshold_distance]
# 임계값 내의 사건 비율을 계산
proportion_close = len(close_events) / len(merged_df)
# 계산된 비율을 출력
print(f"Proportion of events within {threshold_distance} km: {proportion_close}")

# UFO 목격과 실종 사건의 시계열 그래프
plt.figure(figsize=(10, 6))
ufo_df['datetime'].value_counts().resample('M').sum().plot(label='UFO sightings')
missing_df['datetime'].value_counts().resample('M').sum().plot(label='Missing persons')
# y축을 로그 스케일로 설정
plt.yscale('log')
plt.legend()
plt.title('Time Series of UFO Sightings and Missing Persons (Log Scale)')
plt.xlabel('Time')
plt.ylabel('Count (Log Scale)')
plt.savefig('missing4.png', dpi=600)
