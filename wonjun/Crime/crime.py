import pandas as pd

crime_df = pd.read_csv('/content/drive/MyDrive/summer_project/Crime_Data_2010_2017.csv')
ufo_df = pd.read_csv('/content/drive/MyDrive/summer_project/complete.csv', error_bad_lines=False)

print(crime_df.head())
print(ufo_df.head())

# pandas 라이브러리를 사용하여 'Date Occurred' 칼럼을 datetime 형식으로 변환합니다.
crime_df['Date Occurred'] = pd.to_datetime(crime_df['Date Occurred'])

# 'Time Occurred' 칼럼을 시간 형식으로 변환합니다.
# 'Time Occurred' 칼럼은 24시간 형식의 정수이므로, 이를 문자열로 변환하고 시간 형식으로 파싱합니다.
crime_df['Time Occurred'] = pd.to_datetime(crime_df['Time Occurred'].astype(str).str.zfill(4), format='%H%M').dt.time

# 이제 'Date Occurred'와 'Time Occurred'를 결합하여 새로운 'datetime' 칼럼을 생성합니다.
crime_df['datetime'] = pd.to_datetime(crime_df['Date Occurred'].astype(str) + ' ' + crime_df['Time Occurred'].astype(str))

crime_df.columns = [column.strip() for column in crime_df.columns]
# Location 필드에서 NaN이나 Null값을 가진 행을 제거합니다.
crime_df = crime_df.dropna(subset=['Location'])

# Location 칼럼을 ','를 기준으로 분리하여 'latitude'와 'longitude' 칼럼을 생성합니다.
crime_df['latitude'], crime_df['longitude'] = zip(*crime_df['Location'].str.strip('()').str.split(', '))

# 위도와 경도를 문자열에서 실수(float)로 변환합니다.
crime_df['latitude'] = crime_df['latitude'].astype(float)
crime_df['longitude'] = crime_df['longitude'].astype(float)

def fix_midnight(time_str):
    try:
        date_part, time_part = time_str.split()
        if time_part == '24:00':
            date = pd.to_datetime(date_part, format='%m/%d/%Y') + pd.Timedelta(days=1)
            return date.strftime('%m/%d/%Y') + ' 00:00'
        else:
            return time_str
    except AttributeError:  # 'Timestamp' 객체가 'split' 메소드를 가지고 있지 않을 때 발생하는 오류를 처리
        return time_str

ufo_df['datetime'] = ufo_df['datetime'].apply(fix_midnight)
ufo_df['datetime'] = pd.to_datetime(ufo_df['datetime'], format='%m/%d/%Y %H:%M', errors='coerce')

crime_df['Time Occurred'] = crime_df['Time Occurred'].apply(lambda x: x.strftime('%H:%M'))

# 'Date Occurred'열의 데이터타입을 문자열로 변환합니다.
crime_df['Date Occurred'] = crime_df['Date Occurred'].dt.strftime('%Y-%m-%d')

# 이제 'Date Occurred'와 'Time Occurred' 열을 합칠 수 있습니다.
crime_df['datetime'] = pd.to_datetime(crime_df['Date Occurred'] + ' ' + crime_df['Time Occurred'])

# 'latitude', 'longitude', 'datetime' 이외의 열을 제거합니다.
crime_df = crime_df[['latitude', 'longitude', 'datetime']]
ufo_df = ufo_df[['latitude', 'longitude', 'datetime']]

# 두 데이터프레임을 통합합니다.
merged_df = pd.concat([crime_df, ufo_df])

# 'latitude' 열의 값들을 숫자로 변환하고, 그렇지 않은 값을 NaN으로 설정합니다.
merged_df['latitude'] = pd.to_numeric(merged_df['latitude'], errors='coerce')

print(merged_df.dtypes)
print(merged_df.isnull().sum())

# 결측값이 있는 행을 삭제하는 경우:
merged_df = merged_df.dropna()

# 또는

# 결측값을 열의 평균으로 채우는 경우:
merged_df['latitude'].fillna(merged_df['latitude'].mean(), inplace=True)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
merged_df['latitude'].hist(bins=30, edgecolor='black')
plt.title('Latitude Distribution')

plt.subplot(1, 2, 2)
merged_df['longitude'].hist(bins=30, edgecolor='black')
plt.title('Longitude Distribution')

plt.tight_layout()
plt.show()

merged_df.set_index('datetime').resample('M').count().plot(figsize=(10,5))
plt.title('Number of records by month')
plt.show()

import seaborn as sns

plt.figure(figsize=(10,6))
sns.jointplot(data=merged_df, x='longitude', y='latitude', kind='hex')
plt.title('Event distribution by latitude and longitude')
plt.show()

# datetime에서 hour, day, month, year를 추출합니다.
merged_df['hour'] = merged_df['datetime'].dt.hour
merged_df['day'] = merged_df['datetime'].dt.day
merged_df['month'] = merged_df['datetime'].dt.month
merged_df['year'] = merged_df['datetime'].dt.year

from sklearn.model_selection import train_test_split

# 피처와 타겟을 정의합니다.
features = merged_df[['latitude', 'longitude']]
target = merged_df[['hour', 'day', 'month', 'year']]

# 데이터를 훈련 세트와 테스트 세트로 분할합니다.
features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# 선형 회귀 모델 객체를 생성합니다.
model = LinearRegression()

# 훈련 데이터를 사용하여 모델을 학습시킵니다.
model.fit(features_train, target_train['hour'])

# 테스트 데이터에 대한 예측을 수행합니다.
predictions = model.predict(features_test)

# 모델의 성능을 평가합니다.
# 이 경우, Mean Absolute Error (MAE)를 사용하였습니다.
mae = mean_absolute_error(target_test['hour'], predictions)

print(f'Test MAE: {mae:.2f}')

from scipy.stats import spearmanr
import matplotlib.pyplot as plt

# 'hour' 피처 생성
merged_df['hour'] = merged_df['datetime'].dt.hour

# 각 시간별로 UFO 관측 수 계산
ufo_hourly_counts = merged_df[merged_df['source'] == 'ufo'].groupby('hour').size()

# 각 시간별로 범죄 발생 수 계산
crime_hourly_counts = merged_df[merged_df['source'] == 'crime'].groupby('hour').size()

# 스피어만 순위 상관 계수 계산
correlation, p_value = spearmanr(ufo_hourly_counts, crime_hourly_counts)

print(f'Spearman Rank Correlation: {correlation:.2f}')

# 데이터 시각화
plt.figure(figsize=(10,5))

plt.plot(ufo_hourly_counts.index, ufo_hourly_counts.values, label='UFO Sightings')
plt.plot(crime_hourly_counts.index, crime_hourly_counts.values, label='Crimes')
plt.legend()

plt.xlabel('Hour of Day')
plt.ylabel('Count')
plt.title('Hourly Count of Events (UFO Sightings and Crimes)')
plt.show()

# 각 시간별로 UFO 관측 수 계산
ufo_hourly_counts = merged_df[merged_df['source'] == 'ufo'].groupby('hour').size()

# 각 시간별로 범죄 발생 수 계산
crime_hourly_counts = merged_df[merged_df['source'] == 'crime'].groupby('hour').size()

# datetime에서 날짜만 추출
merged_df['date'] = merged_df['datetime'].dt.date

# UFO가 관측된 날짜 구하기
ufo_dates = merged_df[merged_df['source'] == 'ufo']['date'].unique()

# 각 날짜별 범죄 건수 계산
daily_crime_counts = merged_df[merged_df['source'] == 'crime'].groupby('date').size()

# UFO가 관측된 날의 범죄 건수
crime_counts_on_ufo_days = daily_crime_counts.loc[daily_crime_counts.index.isin(ufo_dates)]

# UFO가 관측되지 않은 날의 범죄 건수
crime_counts_on_non_ufo_days = daily_crime_counts.loc[~daily_crime_counts.index.isin(ufo_dates)]

# 두 그룹의 평균 범죄 건수 비교
mean_crime_on_ufo_days = crime_counts_on_ufo_days.mean()
mean_crime_on_non_ufo_days = crime_counts_on_non_ufo_days.mean()

print(f"Average number of crimes on days with UFO sightings: {mean_crime_on_ufo_days}")
print(f"Average number of crimes on days without UFO sightings: {mean_crime_on_non_ufo_days}")

