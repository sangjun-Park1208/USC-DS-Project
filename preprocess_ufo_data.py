import pandas as pd
import io

complete_df = pd.read_csv('./data/ufo/complete.csv', 
                              on_bad_lines='skip', 
                              dtype={
                                  'datetime': str,
                                  'city': str,
                                  'state': str,
                                  'country': str,
                                  'shape': str,
                                  'duration (seconds)': str,
                                  'duration (hours/min)': str,
                                  'comments': str,
                                  'date posted': str,
                                  'latitude': str,
                                  'longitude': str,
                                  }
                              )

scrubbed_df = pd.read_csv('./data/ufo/scrubbed.csv', 
                              on_bad_lines='skip',
                              dtype={
                                  'datetime': str,
                                  'city': str,
                                  'state': str,
                                  'country': str,
                                  'shape': str,
                                  'duration (seconds)': str,
                                  'duration (hours/min)': str,
                                  'comments': str,
                                  'date posted': str,
                                  'latitude': str,
                                  'longitude': str,
                                  }
                              )

# 결측치가 포함된 행 통째로 삭제
complete_df = complete_df.dropna()
scrubbed_df = scrubbed_df.dropna()

# 기존 'datetime'에 포함되어 있던 시간대 정보를 'time' Column 으로 별도 분리
complete_df['datetime'] = pd.to_datetime(complete_df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')
complete_df['time'] = complete_df['datetime'].dt.strftime('%H:%M').replace('24:00', '00:00')

scrubbed_df['datetime'] = pd.to_datetime(scrubbed_df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')
scrubbed_df['time'] = scrubbed_df['datetime'].dt.strftime('%H:%M').replace('24:00', '00:00')

# 'datetime' Column 형태를 'yyyy-mm-dd' 로 바꿈 
complete_df['datetime'] = complete_df['datetime'].dt.floor('D')
scrubbed_df['datetime'] = scrubbed_df['datetime'].dt.floor('D')

# 열 위치 재조정 (datetime, time, ...)
column_order_complete = ['datetime', 'time'] + [col for col in complete_df.columns if col not in ['datetime', 'time']]
complete_df = complete_df[column_order_complete]

column_order_scrubbed = ['datetime', 'time'] + [col for col in scrubbed_df.columns if col not in ['datetime', 'time']]
scrubbed_df = scrubbed_df[column_order_scrubbed]

# datetime 기준 오름차순 정렬 & 같은 날짜인 경우 time 순으로 오름차순 재정렬
complete_df = complete_df.sort_values(by=['datetime', 'time'], ascending=[True, True])
scrubbed_df = scrubbed_df.sort_values(by=['datetime', 'time'], ascending=[True, True])

# 전처리 중 발생한 NaT, NaN 결측치 행 제거
complete_df = complete_df.dropna()
scrubbed_df = scrubbed_df.dropna()

# 'comment', 'duration (hours/min)', 'date posted' Column 제거
columns_to_drop = ['comments', 'duration (hours/min)', 'date posted']
complete_df = complete_df.drop(columns=columns_to_drop)
scrubbed_df = scrubbed_df.drop(columns=columns_to_drop)

# 'duration (seconds)' Column 이름을 'duration' 으로 변경
complete_df = complete_df.rename(columns={'duration (seconds)': 'duration'})
scrubbed_df = scrubbed_df.rename(columns={'duration (seconds)': 'duration'})

print(complete_df)
print(scrubbed_df)

# csv파일로 각각 (complete_after.csv, scrubbed_after.csv) 저장
complete_df.to_csv('complete_after.csv', index=False)
scrubbed_df.to_csv('scrubbed_after.csv', index=False)