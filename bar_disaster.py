import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/seongbyeongjun/Documents/GitHub/USC-DS-Project/data/disaster/us_disaster_declarations.csv')

# 날짜 열을 datetime 형식으로 변환
df['declaration_date'] = pd.to_datetime(df['declaration_date'])

# 연도 열 추출
df['year'] = df['declaration_date'].dt.year

# 년도별 자연재해 횟수 계산
year_counts = df['year'].value_counts().sort_index()

# 바 그래프로 시각화
plt.bar(year_counts.index, year_counts.values)
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Disasters by Year')
plt.show()