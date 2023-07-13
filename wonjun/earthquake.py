import numpy as np
import pandas as pd

# 데이터 불러오기
earthquakes_df = pd.read_csv('../data/earthquake/database.csv')
ufo_df = pd.read_csv('../data/ufo/scrubbed.csv', low_memory=False)
# 컬럼명의 공백 제거
ufo_df.columns = ufo_df.columns.str.strip()

# 다시 컬럼 이름 확인
# print(ufo_df.columns)

# 날짜 형식 통일
earthquakes_df['Date'] = pd.to_datetime(earthquakes_df['Date'], format='%m/%d/%Y', errors='coerce')
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# 'duration (seconds)' 열의 숫자가 아닌 값들을 NaN으로 변환합니다.
ufo_df['duration (seconds)'] = ufo_df['duration (seconds)'].apply(lambda x: float(x) if is_number(x) else None)


# 결측치를 제거합니다.
ufo_df.dropna(subset=['duration (seconds)'], inplace=True)

# 이제 다시 실수형으로 변환을 시도합니다.
ufo_df['duration (seconds)'] = ufo_df['duration (seconds)'].astype(float)

# 결측치 처리
earthquakes_df.dropna(subset=['Date', 'Latitude', 'Longitude', 'Magnitude'], inplace=True)
ufo_df.dropna(subset=['datetime', 'latitude', 'longitude', 'duration (seconds)'], inplace=True)

# 이상치 처리
ufo_df['duration (seconds)'] = ufo_df['duration (seconds)'].astype(float)
ufo_df = ufo_df[ufo_df['duration (seconds)'] <= 3600]


# 데이터 타입 변환
earthquakes_df['Latitude'] = earthquakes_df['Latitude'].astype(float)
earthquakes_df['Longitude'] = earthquakes_df['Longitude'].astype(float)
ufo_df['latitude'] = pd.to_numeric(ufo_df['latitude'], errors='coerce')
ufo_df['longitude'] = pd.to_numeric(ufo_df['longitude'], errors='coerce')

# NaN 값 제거
ufo_df.dropna(subset=['latitude', 'longitude'], inplace=True)

# 필요한 컬럼만 선택
earthquakes_df = earthquakes_df[['Date', 'Latitude', 'Longitude', 'Magnitude']]
ufo_df = ufo_df[['datetime', 'city', 'state', 'country', 'shape', 'duration (seconds)', 'latitude', 'longitude']]

# print("Earthquakes data:")
# print(earthquakes_df.head())
# print("\nUFO data:")
# print(ufo_df.head())


## 시간관계
# 'Year', 'Month', 'Day' 컬럼 생성
earthquakes_df['Year'] = earthquakes_df['Date'].dt.year
earthquakes_df['Month'] = earthquakes_df['Date'].dt.month
earthquakes_df['Day'] = earthquakes_df['Date'].dt.day

ufo_df['Year'] = ufo_df['datetime'].dt.year
ufo_df['Month'] = ufo_df['datetime'].dt.month
ufo_df['Day'] = ufo_df['datetime'].dt.day

# 지진 발생 빈도
earthquake_frequency = earthquakes_df.groupby(['Year', 'Month', 'Day']).size()
# UFO 관측 빈도
ufo_frequency = ufo_df.groupby(['Year', 'Month', 'Day']).size()

# 빈도 데이터를 데이터프레임으로 변환
earthquake_frequency = earthquake_frequency.reset_index(name='Earthquake_Count')
ufo_frequency = ufo_frequency.reset_index(name='UFO_Count')

# 두 데이터프레임 병합
combined_df = pd.merge(earthquake_frequency, ufo_frequency, on=['Year', 'Month', 'Day'], how='outer')

# 결측값을 0으로 채우기
combined_df.fillna(0, inplace=True)

# 상관관계 계산
correlation = combined_df['Earthquake_Count'].corr(combined_df['UFO_Count'])
print(f"Correlation between earthquake and UFO sighting frequencies: {correlation}")




## UFO의 관측 위치와 지진 발생 위치의 상관관계를 분석
# from scipy.spatial.distance import cdist
# from sklearn.neighbors import BallTree
#
# # haversine distance 함수 정의
# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371  # Earth's radius in kilometers
#     phi1 = np.radians(lat1)
#     phi2 = np.radians(lat2)
#     delta_phi = np.radians(lat2 - lat1)
#     delta_lambda = np.radians(lon2 - lon1)
#     a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
#     res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
#     return np.round(res, 2)  # Output distance in kilometers
#
# # UFO 데이터의 위도/경도를 2차원 배열로 변환
# ufo_coords = ufo_df[['latitude', 'longitude']].values
# # BallTree 객체를 생성합니다. 이 객체는 빠르게 최근접 이웃을 찾는데 사용됩니다.
# tree = BallTree(ufo_coords, leaf_size=15, metric='haversine')
#
# # 각 지진 데이터에 대해 가장 가까운 UFO 관측지점을 찾습니다.
# def find_nearest_ufo(row):
#     dist, ind = tree.query([[np.radians(row['Latitude']), np.radians(row['Longitude'])]], k=1)  # k=1은 가장 가까운 이웃 1개를 찾는 것입니다.
#     return haversine(row['Latitude'], row['Longitude'], ufo_coords[ind[0][0]][0], ufo_coords[ind[0][0]][1])
#
# earthquakes_df['NearestUfoDistance'] = earthquakes_df.apply(find_nearest_ufo, axis=1)
#
# # 결과를 확인합니다.
# # print(earthquakes_df.head())
#
# import scipy.stats
# import matplotlib.pyplot as plt
#
# # 상관 계수 계산
# correlation, p_value = scipy.stats.pearsonr(earthquakes_df['Magnitude'], earthquakes_df['NearestUfoDistance'])
#
# print(f'Correlation coefficient: {correlation:.2f}')
#
# # 산포도 그리기
# plt.figure(figsize=(10, 6))
# plt.scatter(earthquakes_df['Magnitude'], earthquakes_df['NearestUfoDistance'])
# plt.xlabel('Earthquake Magnitude')
# plt.ylabel('Distance to Nearest UFO (km)')
# plt.title(f'Correlation between Earthquake Magnitude and Distance to Nearest UFO\nCorrelation coefficient: {correlation:.2f}')
# plt.show()





























