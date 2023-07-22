# state_analysis_by_year.py

import pandas as pd

# 데이터 로드
df = pd.read_csv('disaster/scv/us_disaster_declarations.csv')

# 'declaration_date' 열을 datetime 형식으로 변환하여 년도만 추출하여 'year' 열 생성
df['declaration_date'] = pd.to_datetime(df['declaration_date'])
df['year'] = df['declaration_date'].dt.year

# 각 연도별로 가장 많은 재난이 발생한 주 파악
most_frequent_state_by_year = df.groupby(['year', 'state'])['state'].count().reset_index(name='count')
most_frequent_state_by_year = most_frequent_state_by_year.loc[most_frequent_state_by_year.groupby('year')['count'].idxmax()]

# 결과 출력
print(most_frequent_state_by_year)

most_frequent_state_by_year.to_csv('most_frequent_state_by_year.csv', index=False)