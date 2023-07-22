import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
df = pd.read_csv('../../data/death/leading_cause_death.csv')

# 'DEATHS' 열의 데이터 타입을 숫자로 변환
df['DEATHS'] = pd.to_numeric(df['DEATHS'], errors='coerce')

# 'All causes' 또는 'All Causes' 제외
df = df[~df['CAUSE_NAME'].isin(['All causes', 'All Causes'])]

# 'YEAR'와 'CAUSE_NAME' 별로 그룹화하고, 'DEATHS' 열을 합산
deaths_by_year_and_cause = df.groupby(['YEAR', 'CAUSE_NAME'])['DEATHS'].sum().reset_index()

# 각 연도별로 사망자 수를 기준으로 내림차순 정렬
deaths_by_year_and_cause_sorted = deaths_by_year_and_cause.sort_values(['YEAR', 'DEATHS'], ascending=[True, False])

# 각 연도별로 순위 매기기
deaths_by_year_and_cause_sorted['RANK'] = deaths_by_year_and_cause_sorted.groupby('YEAR')['DEATHS'].rank(method='min', ascending=False)

# 매년 Top 5 사망원인만 선택
top_5_causes_each_year = deaths_by_year_and_cause_sorted[deaths_by_year_and_cause_sorted['RANK'] <= 5]

# 결과 출력
print(top_5_causes_each_year)
# 시각화
plt.figure(figsize=(15, 10))
sns.barplot(data=top_5_causes_each_year, x='YEAR', y='DEATHS', hue='CAUSE_NAME')
plt.title('Top 5 Causes of Death Each Year (Excluding "All causes")')
plt.xlabel('Year')
plt.ylabel('Number of Deaths')
plt.legend(title='Cause of Death', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('Cause_of_Death.png', dpi=600)
plt.show()


