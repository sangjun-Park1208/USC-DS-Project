import pandas as pd
from sklearn.linear_model import LinearRegression


# 5. 다변량 회귀분석
# 5-2 'Shape'
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

# shape 변수를 One-Hot Encoding
shape_dummies = pd.get_dummies(ufo_data['shape'])

# 원래 데이터프레임에 새로 만든 shape 더미 변수를 추가
ufo_data = pd.concat([ufo_data, shape_dummies], axis=1)

# 'State' 더미 변수 생성
state_dummies = pd.get_dummies(ufo_data['state'], drop_first=True)
ufo_data = pd.concat([ufo_data, state_dummies], axis=1)

# 각 년도별 각 주에서의 UFO 발견 횟수 계산
ufo_counts_by_year_state_shape = ufo_data.groupby(['Year', 'state', 'shape']).size().reset_index(name='UFO_counts')

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
merged_data = pd.merge(ufo_counts_by_year_state_shape, disease_cases_by_year, on='Year', how='left')

# 독립변수와 종속변수 설정
X = merged_data.drop(columns=['Cases', 'Year', 'state', 'shape'])
y = merged_data['Cases']

# 모델 생성 및 훈련
model = LinearRegression()
model.fit(X, y)

# 모델 평가: R^2 Score 계산
r2_score = model.score(X, y)

print('R^2 Score:', r2_score)
