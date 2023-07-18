# import pandas as pd

# # disaster.csv 파일 로드
# df = pd.read_csv('num_disaster.csv')

# # 'declaration_date' 열을 년도로 변환
# df['declaration_date'] = pd.to_datetime(df['declaration_date']).dt.year

# # 년도별 자연재해 횟수 계산
# df = df.groupby('declaration_date').size().reset_index(name='number')

# # 1953년부터 2014년까지의 년도 범위 생성
# years_range = pd.DataFrame({'declaration_date': range(1953, 2015)})

# # 년도 범위와 기존 데이터 병합
# df = pd.merge(years_range, df, on='declaration_date', how='left').fillna(0)

# # 결과 출력
# for _, row in df.iterrows():
#     print(f"{row['declaration_date']}, {row['number']}")


import pandas as pd

# filtered_ufo_data.csv 파일 로드
df = pd.read_csv('filtered_ufo_data.csv')

# datetime 열을 datetime 형식으로 변환
df['datetime'] = pd.to_datetime(df['datetime'])

# 1953년부터 2014년까지의 데이터만 남기기
df = df[(df['datetime'].dt.year >= 1953) & (df['datetime'].dt.year <= 2014)]

# 연도별 UFO 출현 횟수 계산
ufo_counts = df['datetime'].dt.year.value_counts().reset_index()

# 칼럼 이름 변경
ufo_counts.columns = ['year', 'u_num']

ufo_counts.sort_values(by='year', ascending=True, inplace=True)


# 결과 출력
print(ufo_counts)


# CSV로 저장
ufo_counts.to_csv('ufo_num.csv', index=False)
