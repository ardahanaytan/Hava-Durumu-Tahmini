import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from data import df_mean, df_std

X = df.drop('Basinc', axis = 1)
y = df['Basinc']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 270)

X_train = X_train.values.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.values.reshape((X_test.shape[0], 1, X_test.shape[1]))

model = Sequential()
model.add(LSTM(600, activation = 'relu', input_shape = (X_train.shape[1], X_train.shape[2])))
model.add(Dense(1))
model.compile(optimizer = 'adam', loss = 'mse')

model.fit(X_train, y_train, epochs=150, verbose=1)

y_pred = model.predict(X_test)
y_pred = pd.DataFrame(y_pred * df_std + df_mean)
print(y_pred.head())