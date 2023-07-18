# # import pandas as pd

# # # 데이터 로드
# # df = pd.read_csv('filtered_ufo_data.csv')

# # # 중복 제거 및 'state' 열만 선택
# # df = df.drop_duplicates(subset=['state']).loc[:, ['state']]

# # # CSV 파일로 저장
# # df.to_csv('state_list_data.csv', index=False)

# # # 결과 출력
# # print(df)

# # 주(state) 목록
# states = ['ME', 'TX', 'IN', 'IL', 'OR', 'CO', 'KS', 'ND', 'MI', 'AK', 'CA', 'AL', 'SC', 'IA', 'GA', 'TN', 'KY', 'NM', 'FL', 'NC', 'VA', 'NY', 'WA', 'AZ', 'OH', 'PA', 'MN', 'WI', 'MD', 'NV', 'ID', 'MO', 'OK', 'WV', 'MS', 'NJ', 'CT', 'WY', 'UT', 'RI', 'AR', 'MA', 'NE', 'LA', 'DE', 'NH', 'SD', 'VT', 'MT', 'HI', 'PR', 'DC']

# # 동부와 서부를 구분하는 기준 인덱스
# eastern_states = ['ME', 'IN', 'IL', 'OR', 'KS', 'MI', 'AK', 'CA', 'SC', 'GA', 'TN', 'KY', 'FL', 'NC', 'VA', 'NY', 'AZ', 'OH', 'PA', 'MN', 'WI', 'MD', 'NV', 'ID', 'MO', 'WV', 'MS', 'NJ', 'CT', 'DE', 'NH', 'VT', 'HI', 'PR', 'DC']
# western_states = ['TX', 'CO', 'ND', 'IA', 'NM', 'AL', 'WA', 'OK', 'LA', 'SD', 'MT']

# # 동부와 서부로 나누기
# eastern_states_list = [state for state in states if state in eastern_states]
# western_states_list = [state for state in states if state in western_states]

# # 결과 출력
# print("Eastern States:")
# print(eastern_states_list)
# print("\nWestern States:")
# print(western_states_list)

import pandas as pd

# UFO 데이터 로드
df = pd.read_csv('/Users/seongbyeongjun/Documents/GitHub/USC-DS-Project/filtered_ufo_data.csv')

# 동부와 서부로 분류
eastern_states = ['ME', 'IN', 'IL', 'OR', 'KS', 'MI', 'AK', 'CA', 'SC', 'GA', 'TN', 'KY', 'FL', 'NC', 'VA', 'NY', 'AZ', 'OH', 'PA', 'MN', 'WI', 'MD', 'NV', 'ID', 'MO', 'WV', 'MS', 'NJ', 'CT', 'DE', 'NH', 'VT', 'HI', 'PR', 'DC']
western_states = ['TX', 'CO', 'ND', 'IA', 'NM', 'AL', 'WA', 'OK', 'LA', 'SD', 'MT']

eastern_data = df[df['state'].isin(eastern_states)]
western_data = df[df['state'].isin(western_states)]

# 동부와 서부 지역의 UFO 관측 횟수 계산
eastern_count = eastern_data.shape[0]
western_count = western_data.shape[0]

# 전체 지역의 UFO 관측 횟수 계산
total_count = df.shape[0]

# 동부와 서부 지역의 UFO 관측률 계산
eastern_rate = (eastern_count / total_count) * 100
western_rate = (western_count / total_count) * 100

# 결과 출력
print("Eastern UFO Observation Rate: {:.2f}%".format(eastern_rate))
print("Western UFO Observation Rate: {:.2f}%".format(western_rate))




