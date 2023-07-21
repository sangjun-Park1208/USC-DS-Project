import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
from scipy.spatial.distance import cdist
from sklearn.neighbors import BallTree

# 데이터 불러오기
earthquakes_df = pd.read_csv('../../data/earthquake/database.csv')
ufo_df = pd.read_csv('../data/ufo/scrubbed.csv', low_memory=False)
# 컬럼명의 공백 제거
ufo_df.columns = ufo_df.columns.str.strip()

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

# 필요한 컬럼만 선택
earthquakes_df = earthquakes_df[['Date', 'Latitude', 'Longitude', 'Magnitude']]
ufo_df = ufo_df[['datetime', 'city', 'state', 'country', 'shape', 'duration (seconds)', 'latitude', 'longitude']]

# UFO의 관측 위치와 지진 발생 위치의 상관관계를 분석
# haversine distance 함수 정의
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    res = R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)  # Output distance in kilometers

# UFO 데이터의 위도/경도를 2차원 배열로 변환
ufo_coords = ufo_df[['latitude', 'longitude']].values
# BallTree 객체를 생성합니다. 이 객체는 빠르게 최근접 이웃을 찾는데 사용됩니다.
tree = BallTree(ufo_coords, leaf_size=15, metric='haversine')

# 각 지진 데이터에 대해 가장 가까운 UFO 관측지점을 찾습니다.
def find_nearest_ufo(row):
    dist, ind = tree.query([[np.radians(row['Latitude']), np.radians(row['Longitude'])]], k=1)  # k=1은 가장 가까운 이웃 1개를 찾는 것입니다.
    return haversine(row['Latitude'], row['Longitude'], ufo_coords[ind[0][0]][0], ufo_coords[ind[0][0]][1])

earthquakes_df['NearestUfoDistance'] = earthquakes_df.apply(find_nearest_ufo, axis=1)

# 상관 계수 계산
correlation, p_value = scipy.stats.pearsonr(earthquakes_df['Magnitude'], earthquakes_df['NearestUfoDistance'])

print(f'Correlation coefficient: {correlation:.2f}')

# 산포도 그리기
plt.figure(figsize=(10, 6))
plt.scatter(earthquakes_df['Magnitude'], earthquakes_df['NearestUfoDistance'])
plt.xlabel('Earthquake Magnitude')
plt.ylabel('Distance to Nearest UFO (km)')
plt.title(f'Correlation between Earthquake Magnitude and Distance to Nearest UFO\nCorrelation coefficient: {correlation:.2f}')

# 데이터 이상치를 확인하기 위한 박스플롯 시각화
plt.figure(figsize=(6, 8))
plt.boxplot(earthquakes_df['Magnitude'])
plt.xlabel('Magnitude')
plt.ylabel('Magnitude Value')
plt.title('Box Plot of Earthquake Magnitude')
plt.savefig('earthquake_magnitude_boxplot.png', dpi=300)

# plt.show()
plt.savefig('earthquake.png', dpi=300)
plt.show()
