import pandas as pd
import matplotlib.pyplot as plt

# UFO 관측 데이터 로드
ufo_df = pd.read_csv('./data/ufo/complete.csv', on_bad_lines='skip')

# 자연재해 데이터 로드
disaster_df = pd.read_csv('/Users/seongbyeongjun/Documents/GitHub/USC-DS-Project/data/disaster/us_disaster_declarations.csv')

# 날짜 열을 datetime 형식으로 변환
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')
disaster_df['declaration_date'] = pd.to_datetime(disaster_df['declaration_date'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')

# 연도별 UFO 관측 횟수 계산
ufo_counts = ufo_df['datetime'].dt.year.value_counts().sort_index()

# 연도별 자연재해 횟수 계산
disaster_counts = disaster_df['declaration_date'].dt.year.value_counts().sort_index()

# 시계열 그래프 그리기
plt.plot(ufo_counts.index, ufo_counts.values, label='UFO Sightings')
plt.plot(disaster_counts.index, disaster_counts.values, label='Disasters')

# 그래프 제목, 축 레이블 설정
plt.title('UFO Sightings and Disasters over Time')
plt.xlabel('Year')
plt.ylabel('Count')

# 범례 표시
plt.legend()

# 그래프 출력
plt.show()
