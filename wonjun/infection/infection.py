import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from statsmodels.tsa.stattools import grangercausalitytests
from sklearn.model_selection import cross_val_score


# 0.데이터 전처리 과정
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


# 1. 연도별 UFO 발견 횟수와 감염병 사례 수의 상관관계 및 p값 계산
correlation, p_value = pearsonr(merged_data['UFO_counts'], merged_data['Cases'])
print('Correlation between yearly UFO counts and disease cases:', correlation)
print('P-value:', p_value)
# 상관관계 시각화
fig, ax1 = plt.subplots(figsize=(15, 10))
color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('UFO Counts (log scale)', color=color)
line1, = ax1.plot(merged_data['Year'], merged_data['UFO_counts'], color=color, label='UFO Counts')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_yscale('log') # y-axis in log scale
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Disease Cases (log scale)', color=color)
line2, = ax2.plot(merged_data['Year'], merged_data['Cases'], color=color, label='Disease Cases')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_yscale('log') # y-axis in log scale
lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines])
fig.tight_layout()
plt.title('UFO Counts and Disease Cases Over Years')
plt.savefig('1_infection_log_scale.png', dpi=600)


# # 2. 이상치 판별
# ufo_counts_zscore = np.abs((merged_data['UFO_counts'] - merged_data['UFO_counts'].mean()) / merged_data['UFO_counts'].std())
# disease_cases_zscore = np.abs((merged_data['Cases'] - merged_data['Cases'].mean()) / merged_data['Cases'].std())
# outlier_threshold = 3
# # UFO Counts 이상치
# ufo_outliers = merged_data[ufo_counts_zscore > outlier_threshold]
# # Disease Cases 이상치
# disease_outliers = merged_data[disease_cases_zscore > outlier_threshold]
# # 이상치 출력
# if not ufo_outliers.empty:
#     print('Outliers in UFO counts:')
#     print(ufo_outliers)
# else:
#     print('No outliers found in UFO counts.')
#
# if not disease_outliers.empty:
#     print('Outliers in Disease cases:')
#     print(disease_outliers)
# else:
#     print('No outliers found in Disease cases.')
# # 이상치 그래프 시각화(Box Plots)
# plt.figure(figsize=(15, 10))
# # Box plot for UFO
# plt.subplot(2, 1, 1)
# plt.boxplot(merged_data['UFO_counts'], vert=False)
# plt.xlabel('UFO Counts')
# plt.title('Box Plot for UFO Counts')
# # Box plot for Disease
# plt.subplot(2, 1, 2)
# plt.boxplot(merged_data['Cases'], vert=False)
# plt.xlabel('Disease Cases')
# plt.title('Box Plot for Disease Cases')
# plt.tight_layout()
# plt.savefig('2_box_plots.png', dpi=600)

# 2. 이상치 판별
ufo_counts_zscore = np.abs((merged_data['UFO_counts'] - merged_data['UFO_counts'].mean()) / merged_data['UFO_counts'].std())
disease_cases_zscore = np.abs((merged_data['Cases'] - merged_data['Cases'].mean()) / merged_data['Cases'].std())
outlier_threshold = 3
# UFO Counts 이상치
ufo_outliers = merged_data[ufo_counts_zscore > outlier_threshold]
# Disease Cases 이상치
disease_outliers = merged_data[disease_cases_zscore > outlier_threshold]
# 이상치 출력
if not ufo_outliers.empty:
    print('Outliers in UFO counts:')
    print(ufo_outliers)
else:
    print('No outliers found in UFO counts.')

if not disease_outliers.empty:
    print('Outliers in Disease cases:')
    print(disease_outliers)
else:
    print('No outliers found in Disease cases.')

# 이상치 그래프 시각화(Box Plots)
plt.figure(figsize=(15, 10))
# Box plot for UFO
plt.subplot(2, 1, 1)
plt.boxplot(merged_data['UFO_counts'], vert=False)
plt.xlabel('UFO Counts')
plt.title('Box Plot for UFO Counts')
# Adding arrows to UFO outliers
if not ufo_outliers.empty:
    for outlier, year in zip(ufo_outliers['UFO_counts'], ufo_outliers['Year']):
        plt.annotate(f'Outlier in {year}', xy=(outlier, 1), xytext=(outlier, 1.5),
                     arrowprops=dict(arrowstyle='->', lw=1), ha='center')

# Box plot for Disease
plt.subplot(2, 1, 2)
plt.boxplot(merged_data['Cases'], vert=False)
plt.xlabel('Disease Cases')
plt.title('Box Plot for Disease Cases')
plt.tight_layout()
plt.savefig('2_1_box_plots.png', dpi=600)




# 3. 특정계절에 따른 관측 횟수 시각화
# 'Month' 열을 생성합니다. 'datetime'에서 월만 추출해서 추가합니다.
ufo_data['Month'] = ufo_data['datetime'].dt.month
# 월별로 그룹화하고 각 그룹의 크기(즉, 발견 횟수)를 계산
ufo_counts_by_month = ufo_data.groupby('Month').size().reset_index(name='UFO_counts')
# 그래프 그리기
plt.figure(figsize=(15, 10))
plt.plot(ufo_counts_by_month['Month'], ufo_counts_by_month['UFO_counts'], label='UFO Counts by Month')
plt.xlabel('Month')
plt.ylabel('Counts')
plt.title('UFO Counts by Month')
plt.legend()
plt.savefig('3_UFO Counts by Month.png', dpi=600)


# 4. 비선형회귀
# PolynomialFeatures 객체 생성
poly_features = PolynomialFeatures(degree=2)
# 연도를 특징으로 사용하고, 감염병 사례 수를 목표 변수로 설정
X = merged_data['Year'].values.reshape(-1, 1)
y = merged_data['Cases']
# 다항식 특징 생성
X_poly = poly_features.fit_transform(X)
# 모델 생성
model = LinearRegression()
# Cross validation
cv_scores = cross_val_score(model, X_poly, y, cv=5)
print("Cross-validation scores: ", cv_scores)
print("Average cross-validation score: ", cv_scores.mean())
# 모델 훈련
model.fit(X_poly, y)
# 예측 수행
y_poly_pred = model.predict(X_poly)
# R^2 Score 계산
r2_score = r2_score(y, y_poly_pred)
print('R^2 Score:', r2_score)
# 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Actual Cases')
plt.plot(X, y_poly_pred, color='red', label='Predicted Cases')
plt.title('Disease Cases Over Years')
plt.xlabel('Year')
plt.ylabel('Cases')
plt.legend()
plt.show()


# 5. 다변량 회귀분석
# Multivariate Regression_shape.py
# Multivariate Regression_state.py


# 6. Granger 인과성 테스트 수행
max_lag = 3  # 최대 시차 (lag) 설정
test_result = grangercausalitytests(merged_data[['UFO_counts', 'Cases']], max_lag, verbose=True)
print(test_result)
