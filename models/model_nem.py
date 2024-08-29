import sys
import numpy as np
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from sklearn.metrics import mean_squared_error
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

df_t = pd.DataFrame({'Nem': df['Nem']})

train_df = df_t[:int(0.8 * len(df.index))].resample('M').mean()
test_df = df_t[int(0.8 * len(df.index)):].resample('M').mean()

acf_lag = acf(train_df.values, nlags=20)
pacf_lag = pacf(train_df.values, nlags=20, method='ols')

model = ARIMA(train_df.values, order=(2,0,1))
model_fit = model.fit()

