import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge # Ridge를 import 합니다.
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

# 데이터 로딩
ufo_data = pd.read_csv('../../data/ufo_after/complete_after.csv')
# datetime 필드를 datetime 형태로 변환
ufo_data['datetime'] = pd.to_datetime(ufo_data['datetime'], errors='coerce')
# 필요한 칼럼만 추출
ufo_data = ufo_data[['datetime', 'city', 'state', 'country', 'shape', 'latitude', 'longitude']]
# 결측값 제거
ufo_data = ufo_data.dropna()
# 'Year' 열을 생성합니다. 'datetime'에서 연도만 추출해서 추가합니다.
ufo_data['Year'] = ufo_data['datetime'].dt.year
# 2001년 이후의 데이터만 선택
ufo_data = ufo_data[ufo_data['Year'] >= 2001]
# 연도별로 그룹화하고 각 그룹의 크기(즉, 발견 횟수)를 계산
ufo_counts_by_year = ufo_data.groupby('Year').size().reset_index(name='UFO_counts')

# 이 부분이 추가된 부분입니다. 2012년과 2013년의 값을 평균 값으로 대체합니다.
average_counts = ufo_counts_by_year['UFO_counts'].mean()
ufo_counts_by_year.loc[ufo_counts_by_year['Year'] == 2012, 'UFO_counts'] = average_counts
ufo_counts_by_year.loc[ufo_counts_by_year['Year'] == 2013, 'UFO_counts'] = average_counts

# 데이터 로딩
disease_data = pd.read_csv('../../data/infection/infectious-diseases-by-county-year-and-sex.csv')
# 'Year' 필드를 datetime 형태로 변환
disease_data['Year'] = disease_data['Year'].astype(int)
# 필요한 칼럼만 추출
disease_data = disease_data[['Disease', 'County', 'Year', 'Sex', 'Cases', 'Population', 'Rate']]
# 결측값 제거
disease_data = disease_data.dropna()
# 감염병 데이터를 연도별로 그룹화하고, 각 그룹의 사례 수를 합산
disease_cases_by_year = disease_data.groupby('Year')['Cases'].sum().reset_index()
# 병합된 데이터 생성
merged_data = pd.merge(ufo_counts_by_year, disease_cases_by_year, on='Year', how='left')

# PolynomialFeatures 객체 생성
poly_features = PolynomialFeatures(degree=1)
# 연도를 특징으로 사용하고, 감염병 사례 수를 목표 변수로 설정
X = merged_data['Year'].values.reshape(-1, 1)
y = merged_data['Cases']
# 다항식 특징 생성
X_poly = poly_features.fit_transform(X)
# 모델 생성
model = Ridge(alpha=1.0)  # Ridge 모델을 사용합니다.
# Cross validation
cv_scores = cross_val_score(model, X_poly, y, cv=3)
print("Cross-validation scores: ", cv_scores)
print("Average cross-validation score: ", cv_scores.mean())
# 모델 훈련
model.fit(X_poly, y)
# 예측 수행
y_poly_pred = model.predict(X_poly)
# R^2 Score 계산
r2_score_value = r2_score(y, y_poly_pred)
print('R^2 Score:', r2_score_value)
# 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Actual Cases')
plt.plot(X, y_poly_pred, color='red', label='Predicted Cases')
plt.title('Disease Cases Over Years')
plt.xlabel('Year')
plt.ylabel('Cases')
plt.legend()
plt.savefig('1_infection_log_scale.png', dpi=600)
plt.show()
