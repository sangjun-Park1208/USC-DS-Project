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

# 비선형 회귀 모델 만들기 (Polynomial Regression)
X = merged_data['u_num']
X_poly = np.column_stack((X, X**2))  # 독립 변수에 X와 X^2 추가
X_poly = sm.add_constant(X_poly)  # 상수항 추가
y = merged_data['number']

model = sm.OLS(y, X_poly)

# 회귀 모델 피팅
results = model.fit()

# 결과 출력
print(results.summary())

# 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
plt.scatter(X, y, color='blue', label='Actual Cases')
plt.plot(X, results.predict(X_poly), color='red', label='Predicted Cases')
plt.title('Number of Cases Over Years (Polynomial Regression)')
plt.xlabel('Year (u_num)')
plt.ylabel('Number of Cases (number)')
plt.legend()
plt.show()

plt.savefig('polynomial_regression.png')