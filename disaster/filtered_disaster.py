import pandas as pd

# 자연재해 데이터 로드
disaster_data = pd.read_csv('disaster/scv/filtered_disaster_data.csv')

# 'declaration_date' 열에서 시간 부분 제거하여 날짜로 변환
disaster_data['declaration_date'] = pd.to_datetime(disaster_data['declaration_date']).dt.strftime('%Y-%m-%d')

# 필요한 열 선택
disaster_data = disaster_data[['state', 'declaration_date', 'incident_type']]

# 결과 출력
print(disaster_data)

# CSV 파일로 저장
disaster_data.to_csv('filtered_disaster_data.csv', index=False)
