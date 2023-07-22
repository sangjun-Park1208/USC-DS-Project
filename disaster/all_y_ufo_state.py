import pandas as pd

# 데이터 로드
df = pd.read_csv('disaster/scv/complete_after.csv')

# 'datetime' 열을 datetime 형식으로 변환하여 년도만 추출하여 'year' 열 생성
df['datetime'] = pd.to_datetime(df['datetime'])
df['year'] = df['datetime'].dt.year

# state 값을 대문자로 변경
df['state'] = df['state'].str.upper()

# 각 년도별로 가장 많이 관측된 주 파악
most_observed_state_by_year = df.groupby(['year', 'state'])['state'].count().reset_index(name='count')
most_observed_state_by_year = most_observed_state_by_year.loc[most_observed_state_by_year.groupby('year')['count'].idxmax()]

# 결과 출력
print(most_observed_state_by_year)

# 결과를 CSV 파일로 저장
most_observed_state_by_year.to_csv('most_observed_state_by_year.csv', index=False)
