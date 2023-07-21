
#이상치판단 코드

# import pandas as pd
# import matplotlib.pyplot as plt

# # CSV 파일 로드
# df = pd.read_csv('disaster/scv/num_disaster_data.csv')

# # 이상치를 찾기 위해 박스플롯 그리기
# plt.figure(figsize=(10, 6))
# box = plt.boxplot(df['number'], vert=False, patch_artist=True)

# # 이상치를 판단하여 그래프에 표시
# outliers = [flier.get_xdata()[0] for flier in box['fliers']]
# for outlier in outliers:
#     index = df[df['number'] == outlier].index[0]
#     plt.annotate(df['declaration_date'][index], xy=(outlier, 1), xytext=(outlier, 1.1),
#                  arrowprops=dict(arrowstyle="->", lw=1), ha='center')

# plt.title('Box Plot of Number')
# plt.xlabel('Number')
# plt.show()



#2005년,2011년,2008년 데이터 구분

# import pandas as pd

# # CSV 파일 로드
# data = pd.read_csv('disaster/scv/filtered_disaster_data.csv')

# # declaration_date 열을 datetime 형식으로 변환
# data['declaration_date'] = pd.to_datetime(data['declaration_date'])

# # 년도만 남기고 월, 일, 시간단위는 제거하여 새로운 열 생성
# data['year_only'] = data['declaration_date'].dt.year

# # 불필요한 열(declaration_date) 제거
# data.drop(columns=['declaration_date'], inplace=True)

# # 2005년 데이터만 필터링
# filtered_data = data[data['year_only'] == 2008]

# # 결과를 새로운 CSV 파일로 저장
# filtered_data.to_csv('2008_disaster_data.csv', index=False)



# 2005년,2011년,2008년 재난 종류 확인

# import pandas as pd

# # CSV 파일 로드
# data = pd.read_csv('disaster/scv/2011_disaster_data.csv')

# # incident_type의 데이터 종류 확인
# incident_types = data['incident_type'].unique()

# # 결과 출력
# print(incident_types)


#2005년, 2011년, 2008년 재난 종류 바 그래프

# import pandas as pd
# import matplotlib.pyplot as plt

# # CSV 파일 로드
# df = pd.read_csv('disaster/scv/2008_disaster_data.csv')

# # incident_type의 데이터 카운트
# incident_counts = df['incident_type'].value_counts()

# # 바 그래프 그리기
# plt.bar(incident_counts.index, incident_counts.values)
# plt.xticks(rotation=45, ha='right')
# plt.xlabel('Incident Type')
# plt.ylabel('Count')
# plt.title('2008 Incident Type Counts')
# plt.tight_layout()

# # PNG 이미지로 저장
# plt.savefig('2008_incident_type_counts.png')

# # 그래프 표시
# plt.show()




# 2005년 허리케인이 가장 많이 주 바그래프

# import pandas as pd
# import matplotlib.pyplot as plt

# # CSV 파일 로드
# df = pd.read_csv('disaster/scv/2005_disaster_data.csv')

# # 허리케인(incident_type이 Hurricane) 데이터 필터링
# hurricane_data = df[df['incident_type'] == 'Hurricane']

# # 각 주별 허리케인 발생 횟수 계산
# hurricane_counts_by_state = hurricane_data['state'].value_counts()

# # 가장 많이 발생한 주 확인
# most_frequent_state = hurricane_counts_by_state.idxmax()

# print(f"가장 많이 허리케인이 발생한 주: {most_frequent_state}")

# # 바 그래프로 시각화
# plt.bar(hurricane_counts_by_state.index, hurricane_counts_by_state.values)
# plt.xticks(rotation=45, ha='right')
# plt.xlabel('State')
# plt.ylabel('Count')
# plt.title('Hurricane Occurrences by State')
# plt.tight_layout()


# # # PNG 이미지로 저장
# plt.savefig('2005_state_hurricane.png')


# # 그래프 표시
# plt.show()


# 2011년, 2008년 Severe Storm이 가장 많이 주 바그래프

# import pandas as pd
# import matplotlib.pyplot as plt

# # CSV 파일 로드
# df = pd.read_csv('disaster/scv/2008_disaster_data.csv')

# # 허리케인(incident_type이 Hurricane) 데이터 필터링
# severe_storm_data = df[df['incident_type'] == 'Severe Storm']

# # 각 주별 허리케인 발생 횟수 계산
# severe_storm_counts_by_state = severe_storm_data['state'].value_counts()

# # 가장 많이 발생한 주 확인
# most_frequent_state = severe_storm_counts_by_state.idxmax()

# print(f"가장 많이 허리케인이 발생한 주: {most_frequent_state}")

# # 바 그래프로 시각화
# plt.bar(severe_storm_counts_by_state.index, severe_storm_counts_by_state.values)
# plt.xticks(rotation=45, ha='right')
# plt.xlabel('State')
# plt.ylabel('Count')
# plt.title('2008 Severe Storm Occurrences by State')
# plt.tight_layout()


# # PNG 이미지로 저장
# plt.savefig('2008_state_severe_storm.png')


# # 그래프 표시
# plt.show()