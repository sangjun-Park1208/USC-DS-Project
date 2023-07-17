import pandas as pd
import matplotlib.pyplot as plt

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

# 연도별 UFO 발견 횟수와 감염병 사례 수의 상관관계 계산
correlation = merged_data['UFO_counts'].corr(merged_data['Cases'])

print('Correlation between yearly UFO counts and disease cases:', correlation)

# 그래프 그리기
plt.figure(figsize=(15, 10))
plt.plot(merged_data['Year'], merged_data['UFO_counts'], label='UFO Counts')
plt.plot(merged_data['Year'], merged_data['Cases'], label='Disease Cases')
plt.xlabel('Year')
plt.ylabel('Counts')
plt.title('UFO Counts and Disease Cases Over Years')
plt.legend()
plt.savefig('infection.png', dpi=300)
plt.show()
