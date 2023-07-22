import pandas as pd

# 데이터 로드
df = pd.read_csv('disaster/scv/us_disaster_declarations.csv')

# 'declaration_date' 열을 datetime 형식으로 변환하여 년도만 추출하여 'year' 열 생성
df['declaration_date'] = pd.to_datetime(df['declaration_date'])
df['year'] = df['declaration_date'].dt.year

# 년도별 가장 많이 일어난 incident_type 찾기
most_common_incident_by_year = df.groupby('year')['incident_type'].apply(lambda x: x.value_counts().idxmax())

# 결과 출력
print(most_common_incident_by_year)

# 년도별 자연재해 빈도를 CSV 파일로 저장
most_common_incident_by_year.to_csv('disaster_counts_by_year.csv', index=True)
