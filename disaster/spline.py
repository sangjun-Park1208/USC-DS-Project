# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import make_interp_spline

# # num_ufo_data.csv 파일 로드
# ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# # num_disaster_data.csv 파일 로드
# disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# # 데이터 병합
# merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# # 스플라인 회귀 모델 만들기
# X = merged_data['u_num']
# y = merged_data['number']

# # 중복된 x 값 제거
# unique_x, index = np.unique(X, return_index=True)
# unique_y = y.iloc[index]

# # 스플라인 보간법 적용
# x_new = np.linspace(unique_x.min(), unique_x.max(), 300)
# spl = make_interp_spline(unique_x, unique_y, k=3)
# y_spline = spl(x_new)

# # 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
# plt.scatter(X, y, color='blue', label='Actual Cases')
# plt.plot(x_new, y_spline, color='red', label='Predicted Cases (Spline Regression)')
# plt.title('Disaster Cases Over Years (Spline Regression)')
# plt.xlabel('UFO Observations')
# plt.ylabel('Number of Disasters')
# plt.legend()
# plt.savefig('spline_regression.png', dpi=300)
# plt.show()


#spline의 교차검증으로 성능평가

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression

# num_ufo_data.csv 파일 로드
ufo_data = pd.read_csv('disaster/scv/num_ufo_data.csv')

# num_disaster_data.csv 파일 로드
disaster_data = pd.read_csv('disaster/scv/num_disaster_data.csv')

# 데이터 병합
merged_data = pd.merge(ufo_data, disaster_data, left_on='year', right_on='declaration_date', how='inner')

# 스플라인 회귀 모델 만들기
X = merged_data['u_num']
y = merged_data['number']

# 중복된 x 값 제거
unique_x, index = np.unique(X, return_index=True)
unique_y = y.iloc[index]

# 스플라인 보간법 적용
x_new = np.linspace(unique_x.min(), unique_x.max(), 300)
spl = make_interp_spline(unique_x, unique_y, k=3)
y_spline = spl(x_new)

# 원래의 데이터와 비선형 회귀 결과를 그래프로 그림
plt.scatter(X, y, color='blue', label='Actual Cases')
plt.plot(x_new, y_spline, color='red', label='Predicted Cases (Spline Regression)')
plt.title('Disaster Cases Over Years (Spline Regression)')
plt.xlabel('UFO Observations')
plt.ylabel('Number of Disasters')
plt.legend()
plt.savefig('spline_regression.png', dpi=300)
plt.show()

# 데이터 분할을 위한 KFold 객체 생성
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 스플라인 회귀 모델로 교차 검증 수행
spline_model = LinearRegression()
cv_scores = cross_val_score(spline_model, X.values.reshape(-1, 1), y, cv=kf)

# 교차 검증 결과 출력
print("Cross-Validation Scores:", cv_scores)
print("Average Cross-Validation Score:", np.mean(cv_scores))
