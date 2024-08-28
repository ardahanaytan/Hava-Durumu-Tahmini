import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from sklearn.linear_model import Ridge
rr = Ridge(alpha=0.1)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf

scaler = MinMaxScaler()
scaled_df = scaler.fit_transform(df)
sequence_length = 72
num_features = len(df.columns)

sequences = []
labels = []
for i in range(len(scaled_df) - sequence_length):
    seq = scaled_df[i:i+sequence_length]
    label = scaled_df[i+sequence_length][0]
    sequences.append(seq)
    labels.append(label)

sequences = np.array(sequences)
labels = np.array(labels)

train_size = int(0.8 * len(sequences))
train_x, test_x = sequences[:train_size], sequences[train_size:]
train_y, test_y = labels[:train_size], labels[train_size:]

model = Sequential()

model.add(LSTM(units=64, input_shape = (train_x.shape[1], train_x.shape[2]), return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=32, return_sequences=False))
model.add(Dropout(0.2))

#model.add(LSTM(units=32, return_sequences=False))
#model.add(Dropout(0.2))

model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model_checkpoint = ModelCheckpoint('models/best_model_weights.keras', monitor='val_loss', save_best_only=True)

history = model.fit(
    train_x, train_y, 
    epochs=100, 
    batch_size=720, 
    validation_split=0.2,
    callbacks=[early_stopping, model_checkpoint]
)

best_model = tf.keras.models.load_model('models/best_model_weights.keras')
#test_loss = best_model.evaluate(test_x, test_y)
#print('Test Loss: ', test_loss)

'''
predictions = best_model.predict(test_x)

mae = mean_absolute_error(test_y, predictions)
mse = mean_squared_error(test_y, predictions)
rmse = np.sqrt(mse)

print('MAE: ', mae)
print('MSE: ', mse)
print('RMSE: ', rmse)
'''

test_y_copies = np.repeat(test_y.reshape(-1, 1), test_x.shape[-1], axis=-1)
true_temp = scaler.inverse_transform(test_y_copies)[:, 0]

prediction = best_model.predict(test_x)
prediction_copies = np.repeat(prediction, 8, axis=-1)
preedicted_temp = scaler.inverse_transform(prediction_copies)[:, 0]

plt.figure(figsize=(10,6))
plt.plot(df.index[-100:], true_temp[-100:], label='Actual')
plt.plot(df.index[-100:], preedicted_temp[-100:], label='Predicted')
plt.title('Basinc Prediction vs Actual')
plt.xlabel('Time')
plt.ylabel('Basinc')
plt.legend()
plt.show()



'''
df['hedef'] = df.shift(-24)['Sicaklik']
df.iloc[-24:] = df.iloc[-48:-24]

predictors = df.columns[~df.columns.isin(['hedef'])]

def backtest(weather, model, predictors, start = 40000, step = 24):
    all_predictions = []
    
    for i in range(start, weather.shape[0], step):
        train = weather.iloc[:i,:]
        test = weather.iloc[i:(i+step),:]
        
        model.fit(train[predictors], train['hedef'])
        
        preds = model.predict(test[predictors])
        
        preds = pd.Series(preds, index=test.index)
        combined = pd.concat([test['hedef'], preds], axis=1)
        
        combined.columns = ['actual','prediction']
        combined['diff'] = (combined['prediction'] - combined['actual']).abs()
        
        all_predictions.append(combined)
    return pd.concat(all_predictions)

predictions = backtest(df, rr, predictors)

def pct_diff(old, new):
    return (new - old) / old

def compute_rolling(weather, horizon, col):
    label = f"rolling_{horizon}_{col}"
    weather[label] = weather[col].rolling(horizon).mean()
    weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
    return weather

rolling_horizons = [3,24]

for horizon in rolling_horizons:
    for col in ['Basinc','Bulut','Nem','Ruzgar Hizi','Ruzgar Yonu','Sicaklik','Yagis','Kar']:
        df = compute_rolling(df, horizon, col)

df = df.iloc[24:, :]
df = df.fillna(0)

def expand_mean(df):
    return df.expanding(1).mean()

for col in ['Basinc','Bulut','Nem','Ruzgar Hizi','Ruzgar Yonu','Sicaklik','Yagis','Kar']:
    df[f'month_avg_{col}'] = df[col].groupby(df.index.month, group_keys=False).apply(expand_mean)
    df[f'day_avg_{col}'] = df[col].groupby(df.index.day_of_year, group_keys=False).apply(expand_mean)
    df[f'hour_avg_{col}'] = df[col].groupby(df.index.hour, group_keys=False).apply(expand_mean)

predictors = df.columns[~df.columns.isin(['hedef'])]
predictions = backtest(df, rr, predictors)
print(predictions['diff'].mean())

# SICAKLIK ICIN EN DUSUK -> 2.0638077871120877
'''