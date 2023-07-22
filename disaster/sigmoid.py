import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 비선형 회귀 모델 만들기 (Logistic Regression with Sigmoid function)
X = merged_data['u_num']
X = sm.add_constant(X)  # 상수항 추가
y = merged_data['number']

# Sigmoid 함수 정의
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Logistic Regression 모델 피팅
model = sm.Logit(y, X)
results = model.fit()

# 결과 출력
print(results.summary())

# 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
plt.scatter(X['u_num'], y, color='blue', label='Actual Cases')
plt.plot(X['u_num'], sigmoid(results.fittedvalues), color='red', label='Predicted Cases (Logistic Regression)')
plt.title('Number of Cases Over Years (Logistic Regression)')
plt.xlabel('Year (u_num)')
plt.ylabel('Number of Cases (number)')
plt.legend()
plt.show()
