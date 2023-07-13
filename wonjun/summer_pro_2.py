
import pandas as pd

# 데이터 로드
earthquakes_df = pd.read_csv('/content/drive/MyDrive/summer_project/earth/database.csv')
ufo_df = pd.read_csv('/content/drive/MyDrive/summer_project/earth/database.csv', error_bad_lines=False)

print(earthquakes_df['Date'].dtypes)

# 날짜 변환
earthquakes_df['Date'] = pd.to_datetime(earthquakes_df['Date'], format='%Y-%m-%d', errors='coerce', utc=True)
# 먼저, datetime 컬럼을 문자열 형태로 변환합니다.
ufo_df['datetime'] = ufo_df['datetime'].astype(str)

# 각 datetime 값을 공백을 기준으로 분할하고 첫 번째 요소만 선택합니다.
ufo_df['datetime'] = ufo_df['datetime'].apply(lambda x: x.split()[0])

# 이제 datetime 컬럼을 pandas datetime 객체로 변환할 수 있습니다.
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'], utc=True)

# 컬럼명을 소문자로 통일합니다.
ufo_df.columns = map(str.lower, ufo_df.columns)
earthquakes_df.columns = map(str.lower, earthquakes_df.columns)

# 이후 'latitude'와 'longitude' 컬럼을 숫자로 변환합니다.
earthquakes_df['latitude'] = pd.to_numeric(earthquakes_df['latitude'])
earthquakes_df['longitude'] = pd.to_numeric(earthquakes_df['longitude'])
ufo_df['latitude'] = pd.to_numeric(ufo_df['latitude'])
ufo_df['longitude'] = pd.to_numeric(ufo_df['longitude'])

# 필요한 열만 남기기
earthquakes_df = earthquakes_df[['date', 'latitude', 'longitude']]
ufo_df = ufo_df[['datetime', 'latitude', 'longitude']]

# 결측값 확인
print('Earthquakes Missing Values:')
print(earthquakes_df.isnull().sum())
print('\nUFO Sightings Missing Values:')
print(ufo_df.isnull().sum())

# 결측값이 있는 행 삭제
earthquakes_df = earthquakes_df.dropna()
ufo_df = ufo_df.dropna()

print('\nAfter Removing Missing Values:')
print('Earthquakes Missing Values:')
print(earthquakes_df.isnull().sum())
print('\nUFO Sightings Missing Values:')
print(ufo_df.isnull().sum())

# 두 데이터셋을 날짜로 정렬
earthquakes_df = earthquakes_df.sort_values(by=['date'])
ufo_df = ufo_df.sort_values(by=['datetime'])

# 시각화를 위한 라이브러리
import matplotlib.pyplot as plt

# 지진 발생 위치 시각화
plt.figure(figsize=(10, 6))
plt.scatter(earthquakes_df['longitude'], earthquakes_df['latitude'], alpha=0.1, s=10)
plt.title('Earthquake Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# UFO 목격 위치 시각화
plt.figure(figsize=(10, 6))
plt.scatter(ufo_df['longitude'], ufo_df['latitude'], alpha=0.1, s=10)
plt.title('UFO Sightings Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# 두 데이터셋의 공통 날짜 범위 찾기
start_date = max(min(earthquakes_df['date']), min(ufo_df['datetime']))
end_date = min(max(earthquakes_df['date']), max(ufo_df['datetime']))

# 날짜 범위로 데이터 필터링
filtered_earthquakes = earthquakes_df[(earthquakes_df['date'] >= start_date) & (earthquakes_df['date'] <= end_date)]
filtered_ufo = ufo_df[(ufo_df['datetime'] >= start_date) & (ufo_df['datetime'] <= end_date)]

import numpy as np
import matplotlib.pyplot as plt

# bin의 크기 정의
bin_size = 1

# lat, lon bins 생성
lat_bins = np.arange(int(min(filtered_earthquakes['latitude'].min(), filtered_ufo['latitude'].min())),
                     int(max(filtered_earthquakes['latitude'].max(), filtered_ufo['latitude'].max())) + bin_size, bin_size)

lon_bins = np.arange(int(min(filtered_earthquakes['longitude'].min(), filtered_ufo['longitude'].min())),
                     int(max(filtered_earthquakes['longitude'].max(), filtered_ufo['longitude'].max())) + bin_size, bin_size)

# 각각의 데이터셋에 대해 위도 및 경도를 사용하여 히스토그램 계산
earthquake_hist, _, _ = np.histogram2d(filtered_earthquakes['latitude'], filtered_earthquakes['longitude'], [lat_bins, lon_bins])
ufo_hist, _, _ = np.histogram2d(filtered_ufo['latitude'], filtered_ufo['longitude'], [lat_bins, lon_bins])

# 상관관계 분석
correlation = np.corrcoef(earthquake_hist.ravel(), ufo_hist.ravel())[0, 1]
print(f"Correlation between UFO sightings and earthquakes: {correlation:.2f}")

# 결과 시각화
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(earthquake_hist, origin='lower', cmap='hot')
axs[0].set_title("Earthquakes")
axs[1].imshow(ufo_hist, origin='lower', cmap='hot')
axs[1].set_title("UFO sightings")
plt.show()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 필요한 열만 선택
earthquakes_data = earthquakes_df[['date', 'latitude', 'longitude']]
ufo_data = ufo_df[['datetime', 'latitude', 'longitude']]

# 두 데이터셋의 날짜 컬럼 이름을 통일
earthquakes_data = earthquakes_data.rename(columns={'date': 'datetime'})
ufo_data = ufo_data.rename(columns={'datetime': 'datetime'})

# 두 데이터셋을 datetime 열을 기준으로 병합
merged_data = pd.merge(earthquakes_data, ufo_data, on='datetime', how='inner')

# 위도와 경도 사이의 상관관계 계산
correlation = np.corrcoef(merged_data['latitude_x'], merged_data['latitude_y'])[0, 1]

# 상관관계 출력
print(f"Latitude Correlation: {correlation}")

# 산점도 그리기
plt.scatter(merged_data['latitude_x'], merged_data['latitude_y'], alpha=0.1)
plt.xlabel('Earthquake Latitude')
plt.ylabel('UFO Sightings Latitude')
plt.title('Correlation between Earthquake and UFO Sightings Latitude')
plt.show()

# 경도 사이의 상관관계 계산
correlation = np.corrcoef(merged_data['longitude_x'], merged_data['longitude_y'])[0, 1]

# 상관관계 출력
print(f"Longitude Correlation: {correlation}")

# 산점도 그리기
plt.scatter(merged_data['longitude_x'], merged_data['longitude_y'], alpha=0.1)
plt.xlabel('Earthquake Longitude')
plt.ylabel('UFO Sightings Longitude')
plt.title('Correlation between Earthquake and UFO Sightings Longitude')
plt.show()

# 날짜와 시간 데이터 형식 변경
merged_data['datetime'] = pd.to_datetime(merged_data['datetime'])

# 날짜를 인덱스로 설정
merged_data.set_index('datetime', inplace=True)

# 일별 UFO 목격 및 지진 발생 수 계산
daily_ufo_counts = merged_data['latitude_y'].resample('D').count()
daily_earthquake_counts = merged_data['latitude_x'].resample('D').count()

# 일별 UFO 목격 및 지진 발생 수 시계열 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(daily_ufo_counts.index, daily_ufo_counts, label='UFO Sightings')
plt.plot(daily_earthquake_counts.index, daily_earthquake_counts, label='Earthquakes')
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Daily Counts of UFO Sightings and Earthquakes')
plt.legend()
plt.show()

print(len(merged_data['latitude_x']))
print(len(merged_data['latitude_y']))
print(merged_data['latitude_x'].dtype)
print(merged_data['latitude_y'].dtype)