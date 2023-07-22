import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
disaster_data = pd.read_csv('disaster/scv/filtered_disaster_data.csv')

# 'declaration_date' 열에서 연도 추출
disaster_data['year'] = pd.to_datetime(disaster_data['declaration_date']).dt.year

# 필요한 연도 범위 선택 (1953년부터 2014년까지)
disaster_data = disaster_data[(disaster_data['year'] >= 1953) & (disaster_data['year'] <= 2014)]

# 연도별 재해 발생 빈도 계산
disaster_frequency = disaster_data['year'].value_counts().sort_index()

# 선 그래프 생성
plt.plot(disaster_frequency.index, disaster_frequency.values)
plt.xlabel('Year')
plt.ylabel('Disaster Frequency')
plt.title('Natural Disasters Frequency (1953-2014)')
plt.savefig('DISASTER_1.png', dpi=600)
plt.show()
