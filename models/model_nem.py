import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf, pacf

df_t = pd.DataFrame({'Sicaklik': df['Sicaklik']})
train_df = df_t[:'2020'].resample('M').mean()
test_df = df_t['2021':].resample('M').mean()

acf_lag = acf(train_df.values, nlags=20)
pacf_lag = pacf(train_df.values, nlags=20, method='ols')

model = ARIMA(train_df.values, order=(2,0,2))
model_fit = model.fit()

forecast_obj = model_fit.get_forecast(steps=44)

fc = forecast_obj.predicted_mean
se = forecast_obj.se_mean
conf = forecast_obj.conf_int(alpha=0.05)

fc_series = pd.Series(fc, index=test_df.index)
lower_series = pd.Series(conf[:, 0], index=test_df.index)
upper_series = pd.Series(conf[:, 1], index=test_df.index)

#Test Mean Squared Error:  38.86163339550428  DAHA DA IYILESTIRILMELI, EN IYISI BU ARIMA ILE