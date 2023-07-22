import pandas as pd

# 데이터 로딩
ufo_data = pd.read_csv('../../data/ufo_after/complete_after.csv')

# datetime 필드를 datetime 형태로 변환
ufo_data['datetime'] = pd.to_datetime(ufo_data['datetime'], errors='coerce')

# 필요한 칼럼만 추출
ufo_data = ufo_data[['datetime', 'city', 'state', 'country', 'shape', 'latitude', 'longitude']]

# 관측이 많이 발견되는 주 확인
top_states = ufo_data['state'].value_counts().head(5)
print(top_states)
