import pandas as pd
import numpy as np
import statsmodels.api as sm

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 비선형 회귀 모델 만들기
X = merged_data['u_num']
X = sm.add_constant(X)  # 상수항 추가
y = merged_data['number']

model = sm.OLS(y, X)

# 회귀 모델 피팅
results = model.fit()

# 결과 출력
print(results.summary())
