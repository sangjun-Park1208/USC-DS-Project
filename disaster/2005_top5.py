# import pandas as pd

# # 데이터 로드 (파일 경로에 맞게 수정)
# df = pd.read_csv('disaster/scv/2005_disaster_data.csv')

# # 주별로 발생한 재난 종류와 횟수 계산
# state_incident_counts = df.groupby(['state', 'incident_type'])['year_only'].count().reset_index(name='count')

# # 결과 출력
# print(state_incident_counts)

# # 결과를 CSV 파일로 저장 (파일 경로에 맞게 수정)
# state_incident_counts.to_csv('2005_result.csv', index=False)

# import pandas as pd

# # 데이터 로드 (파일 경로에 맞게 수정)
# df = pd.read_csv('disaster/scv/2005_result.csv')

# # incident_type을 카운트해서 top5 추출
# top5_incident_types = df.groupby('incident_type')['count'].sum().reset_index()
# top5_incident_types = top5_incident_types.nlargest(5, 'count')

# # 결과 출력
# print(top5_incident_types)

import pandas as pd

# 데이터 로드
# df = pd.read_csv('disaster/scv/2005_result.csv')

# # 필터링할 incident_type 목록
# desired_incident_types = ["Hurricane", "Severe Storm", "Coastal Storm", "Snowstorm", "Fire"]

# # incident_type이 desired_incident_types에 해당하는 행들만 남기기
# filtered_df = df[df['incident_type'].isin(desired_incident_types)]

# filtered_df.to_csv('2005_top5_data.csv', index=False)

# # 결과 출력
# print(filtered_df)

# import pandas as pd

# # 데이터 로드
# df = pd.read_csv('2005_top5_data.csv')

# # state를 기준으로 그룹화하여 재난 종류별 횟수 합산
# grouped_df = df.groupby(['state', 'incident_type'])['count'].sum().reset_index()

# # state를 기준으로 그룹화하여 재난 종류별 총 발생 횟수 합산
# state_total_df = grouped_df.groupby('state')['count'].sum().reset_index()

# # 중복되는 state를 하나로 합치고 재난 데이터들과 횟수들도 합침
# combined_df = state_total_df.merge(grouped_df, on='state')

# # 결과 출력
# print(combined_df)



import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
df = pd.read_csv('2005_top5_data.csv')

# 범주형 데이터로 변환
df['incident_type'] = pd.Categorical(df['incident_type'])

# 그래프 생성
plt.figure(figsize=(14, 8))
for incident_type, group in df.groupby('incident_type'):
    plt.scatter(group['state'], group['count'], label=incident_type)

plt.xlabel('State')
plt.ylabel('Count')
plt.title('Scatter Plot of Incidents by State')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()
