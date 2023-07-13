import pandas as pd
import matplotlib.pylab as plt

# CSV 파일 로드
df = pd.read_csv('./data/ufo/complete.csv', on_bad_lines='skip')

# 날짜 열을 datetime 형식으로 변환
df['datetime'] = pd.to_datetime(df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')

# 시간이 "24:00"인 경우 "00:00"으로 수정
df['datetime'] = df['datetime'].apply(lambda x: x.replace(hour=0) if x.hour == 24 else x)

# 연도 열 추출
df['year'] = df['datetime'].dt.year

# 년도별 UFO 관측 횟수 계산
year_counts = df['year'].value_counts().sort_index()

# 바 그래프로 시각화
plt.bar(year_counts.index, year_counts.values)
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('UFO Sightings by Year')
plt.show()




