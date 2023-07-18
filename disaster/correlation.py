import pandas as pd

# 데이터 로드
data = pd.read_csv('merged_data.csv')

# 날짜를 연도, 월, 일로 분해
data['declaration_year'] = pd.to_datetime(data['declaration_date']).dt.year
data['declaration_month'] = pd.to_datetime(data['declaration_date']).dt.month
data['declaration_day'] = pd.to_datetime(data['declaration_date']).dt.day

data['datetime_year'] = pd.to_datetime(data['datetime']).dt.year
data['datetime_month'] = pd.to_datetime(data['datetime']).dt.month
data['datetime_day'] = pd.to_datetime(data['datetime']).dt.day

# 'declaration_date'와 'datetime' 간의 상관관계 계산
correlation = data['declaration_year'].corr(data['datetime_year'])

# 결과 출력
print(f"Correlation: {correlation}")
