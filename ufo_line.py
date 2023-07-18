import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
ufo_data = pd.read_csv('filtered_ufo_data.csv')

# 'datetime' 열에서 연도 추출
ufo_data['year'] = pd.to_datetime(ufo_data['datetime']).dt.year

# 필요한 연도 범위 선택 (1960년부터 2014년까지)
ufo_data = ufo_data[(ufo_data['year'] >= 1953) & (ufo_data['year'] <= 2014)]

# 연도별 UFO 출현 빈도 계산
ufo_frequency = ufo_data['year'].value_counts().sort_index()

# 선 그래프 생성
plt.plot(ufo_frequency.index, ufo_frequency.values)
plt.xlabel('Year')
plt.ylabel('UFO Frequency')
plt.title('UFO Sightings Frequency (1960-2014)')
plt.savefig('UFO_1.png', dpi=600)
plt.show()
