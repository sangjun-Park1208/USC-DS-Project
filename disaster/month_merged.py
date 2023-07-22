import pandas as pd
from scipy.stats import pearsonr

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 상관관계 계산 u_num는 ufor관측빈도, number는 자연재해 빈도
correlation = merged_data['u_num'].corr(merged_data['number'])

# p-value 계산
correlation, p_value = pearsonr(merged_data['u_num'], merged_data['number'])

# 결과 출력
print(f"Correlation: {correlation}")
print(f"P-value: {p_value}")
