import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 데이터 읽기
ufo = pd.read_csv('../../data/ufo_after/complete_after.csv')
crime = pd.read_csv('../../data/crime/Crime_Data_2010_2017.csv')

# datetime 컬럼을 datetime 형식으로 변환
ufo['datetime'] = pd.to_datetime(ufo['datetime'])
crime['Date Occurred'] = pd.to_datetime(crime['Date Occurred'])

# LA의 위도, 경도 범위 설정
la_lat_range = (33.7, 34.3)
la_long_range = (-118.7, -118.1)

# LA 지역으로 UFO 데이터 필터링
ufo = ufo[(ufo['latitude'] >= la_lat_range[0]) & (ufo['latitude'] <= la_lat_range[1])
          & (ufo['longitude'] >= la_long_range[0]) & (ufo['longitude'] <= la_long_range[1])]

# 각 데이터셋에서의 최소 및 최대 날짜 확인
ufo_min_date, ufo_max_date = ufo['datetime'].min(), ufo['datetime'].max()
crime_min_date, crime_max_date = crime['Date Occurred'].min(), crime['Date Occurred'].max()

# 공통 날짜 범위 설정
start_date = max(ufo_min_date, crime_min_date)
end_date = min(ufo_max_date, crime_max_date)

# 범위에 맞는 데이터만 선택
ufo = ufo[(ufo['datetime'] >= start_date) & (ufo['datetime'] <= end_date)]
crime = crime[(crime['Date Occurred'] >= start_date) & (crime['Date Occurred'] <= end_date)]

# 같은 날에 발생한 UFO 관측과 범죄 사건의 수를 계산
ufo['Date'] = ufo['datetime'].dt.date
crime['Date'] = crime['Date Occurred'].dt.date

ufo_count_per_day = ufo.groupby('Date').size()
crime_count_per_day = crime.groupby('Date').size()

# 두 시계열 데이터의 상관관계를 계산
combined_data = pd.DataFrame({
    'UFO_count': ufo_count_per_day,
    'Crime_count': crime_count_per_day
})

correlation = combined_data.corr().loc['UFO_count', 'Crime_count']
print("Correlation between UFO sightings and crime rates in LA:", correlation)

# 연도별 데이터 빈도수 계산
ufo['Year'] = ufo['datetime'].dt.year
crime['Year'] = crime['Date Occurred'].dt.year

ufo_count_per_year = ufo.groupby('Year').size()
crime_count_per_year = crime.groupby('Year').size()

# 그래프 그리기
plt.figure(figsize=(10, 6))

plt.plot(ufo_count_per_year.index, ufo_count_per_year, label='UFO sightings')
plt.plot(crime_count_per_year.index, crime_count_per_year, label='Crime rates')

plt.xlabel('Year')
plt.ylabel('Frequency (Log Scale)')
plt.title('UFO Sightings and Crime Rates over Years')
plt.legend()

# 두 데이터의 스케일 차이가 크므로 로그 스케일로 변경
plt.yscale('log')
plt.savefig('1_crime.png', dpi=600)
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(y=ufo_count_per_year.values)
plt.ylim(0, 100) # Set y-axis range based on the min and max value from the UFO sightings statistics
plt.title('UFO sightings per year')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(y=crime_count_per_year.values)
plt.ylim(0, 210000) # Set y-axis range based on the min and max value from the crime rates statistics
plt.title('Crime rates per year')
plt.ylabel('Frequency')
plt.show()
