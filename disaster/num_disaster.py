import pandas as pd

# disaster.csv 파일 로드
df = pd.read_csv('filtered_disaster_data.csv')

# declaration_date 열을 datetime 형식으로 변환
df['declaration_date'] = pd.to_datetime(df['declaration_date'])

# 2014년 이전의 데이터만 남기기
df = df[df['declaration_date'].dt.year < 2015]

# 필요한 열 선택 (declaration_date와 incident_type)
df = df[['declaration_date', 'incident_type']]

# declaration_date 열을 연도 형식으로 변경
df['declaration_date'] = df['declaration_date'].dt.year

# 연도별 자연재해 횟수 계산
df = df.groupby('declaration_date').count().reset_index()

# 열 이름 변경 (incident_type을 number로)
df.rename(columns={'incident_type': 'number'}, inplace=True)

# 결과 출력
print(df)

df.to_csv('num_disaster_data.csv', index=False)