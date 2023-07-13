from tensorflow import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 시계열 데이터 로드
data = pd.read_csv('시계열데이터.csv')

# 필요한 열 추출 및 전처리
# 예시: 시간열 'date'와 예측 대상 열 'target'
data = data[['date', 'target']]
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 데이터 정규화
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# 학습 데이터와 테스트 데이터 분할
train_size = int(len(data_scaled) * 0.8)
train_data = data_scaled[:train_size]
test_data = data_scaled[train_size:]

# 학습 데이터와 레이블 생성
def create_sequences(data, seq_length):
    X = []
    y = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 10  # 시퀀스 길이 설정
X_train, y_train = create_sequences(train_data, seq_length)
X_test, y_test = create_sequences(test_data, seq_length)

# LSTM 모델 구축
model = Sequential()
model.add(LSTM(units=64, input_shape=(seq_length, 1)))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
model.fit(X_train, y_train, epochs=10, batch_size=32)

# 테스트 데이터로 예측 수행
predictions = model.predict(X_test)

# 예측 결과 역정규화
predictions = scaler.inverse_transform(predictions)

# 예측 결과 시각화 등 추가 작업 가능
# ...
