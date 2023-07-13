import pandas as pd

print("hello")

# 데이터셋 로드
dataset_path = "./data/ufo/scrubbed.csv"  # 데이터셋 파일 경로
df = pd.read_csv(dataset_path, sep=",")

print(df.head())
# 'datetime' 열을 datetime 형식으로 변환 (errors='coerce'를 사용하여 잘못된 값은 NaT로 처리)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# 날짜 형식을 변경하여 년/월/일로 정렬
df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')
df = df.sort_values(by='datetime')


print("asdasd")