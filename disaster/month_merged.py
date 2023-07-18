import pandas as pd

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 상관관계 계산
correlation = merged_data['u_num'].corr(merged_data['number'])

# 결과 출력
print(f"Correlation: {correlation}")