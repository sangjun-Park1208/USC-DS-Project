# 판다스 라이브러리를 임포트
import pandas as pd

# 데이터 로딩
disease_data = pd.read_csv('../../data/infection/infectious-diseases-by-county-year-and-sex.csv')

# 'Year' 필드를 datetime 형태로 변환
disease_data['Year'] = pd.to_datetime(disease_data['Year'], format='%Y')

# 필요한 칼럼만 추출
disease_data = disease_data[['Disease', 'County', 'Year', 'Sex', 'Cases', 'Population', 'Rate']]

# 결측값 제거
disease_data = disease_data.dropna()

# 감염병 데이터를 연도별로 그룹화하고, 각 그룹의 사례 수를 합산
disease_cases_by_year = disease_data.groupby(disease_data['Year'].dt.year)['Cases'].sum().reset_index()

# 감염병의 종류 수를 파악
disease_types_count = disease_data['Disease'].nunique()

# 감염병의 종류 확인
disease_types = disease_data['Disease'].unique()

# 감염병 종류별 발생수 계산
disease_cases_by_type = disease_data.groupby('Disease')['Cases'].sum().reset_index()

# 결과 출력
print("Yearly Disease Cases:")
print(disease_cases_by_year)
print("\nNumber of Disease Types:")
print(disease_types_count)
print("\nTypes of Diseases:")
for disease in disease_types:
    print(disease)
print("\nDisease Cases by Type:")
print(disease_cases_by_type)
