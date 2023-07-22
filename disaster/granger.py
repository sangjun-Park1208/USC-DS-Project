import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 상관관계 계산 u_num는 ufor관측빈도, number는 자연재해 빈도
correlation = merged_data['u_num'].corr(merged_data['number'])

# 결과 출력
print(f"Correlation: {correlation}")

# Granger 인과성 테스트를 위한 데이터 준비
# 두 개의 시계열 데이터 생성
np.random.seed(0)
n_obs = 100
data = np.zeros((n_obs, 2))
data[:, 0] = np.random.randn(n_obs)  # 첫 번째 시계열 데이터
data[:, 1] = 0.5 * data[:, 0] + np.random.randn(n_obs)  # 두 번째 시계열 데이터 (첫 번째 시계열 데이터에 영향을 받음)
df = pd.DataFrame(data, columns=['Y1', 'Y2'])

# Granger 인과성 테스트 수행
max_lag = 3  # 최대 시차 (lag) 설정
test_result = grangercausalitytests(df, max_lag, verbose=True)
print(test_result)
