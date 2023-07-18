import pandas as pd

# 필터링된 자연재해 데이터 로드
disaster_data = pd.read_csv('filtered_disaster_data.csv')

# 'incident_type' 열의 고유한 값 확인
incident_types = disaster_data['incident_type'].unique()

# 고유한 값 출력
for incident_type in incident_types:
    print(incident_type)
ㅣ