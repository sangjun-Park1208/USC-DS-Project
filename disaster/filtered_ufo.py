import pandas as pd

# UFO 데이터 로드
ufo_data = pd.read_csv('complete_after.csv')

# 필요한 열 선택
ufo_data = ufo_data[['datetime', 'state', 'country']]

# 'country' 열에서 'us' 값만 필터링
ufo_data = ufo_data[ufo_data['country'] == 'us']

# 'state' 열의 값을 대문자로 변환
ufo_data['state'] = ufo_data['state'].str.upper()

# 결과 출력
print(ufo_data)

# CSV 파일로 저장
ufo_data.to_csv('filtered_ufo_data.csv', index=False)
