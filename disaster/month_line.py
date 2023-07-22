import pandas as pd
import matplotlib.pyplot as plt

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 그래프 생성
plt.figure(figsize=(10, 6))

# UFO 데이터 그래프
plt.plot(merged_data['year'], merged_data['u_num'], color='red', label='UFO')

# 자연재해 데이터 그래프
plt.plot(merged_data['year'], merged_data['number'], color='blue', label='Disaster')

# 축과 제목 설정
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.title('UFO and Disaster Frequency')


# 범례 추가
plt.legend()
plt.savefig('month_1.png', dpi=600)

# 그래프 표시
plt.show()


