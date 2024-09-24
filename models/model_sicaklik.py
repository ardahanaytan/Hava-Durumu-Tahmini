import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_withoutsum

df_y = pd.DataFrame(df['Sicaklik'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Sicaklik': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Sicaklik': 'min'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Sicaklik': 'mean'}, inplace=True)
df_ = pd.concat([df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_withoutsum(df_)
future['yhat_lower'] = ((future['yhat_lower'] - future['yhat_lower'].min()) / (future['yhat_lower'].max() - future['yhat_lower'].min())) * (df_min['min'].max() - df_min['min'].min()) + df_min['min'].min()
future['yhat_upper'] = ((future['yhat_upper'] - future['yhat_upper'].min()) / (future['yhat_upper'].max() - future['yhat_upper'].min())) * (df_max['max'].max() - df_max['max'].min()) + df_max['max'].min()

sicaklikmin_forecast = future[['ds','yhat_lower']].tail(7)
sicaklikmin_forecast.yhat_lower = sicaklikmin_forecast.yhat_lower.round(1)

sicaklikmax_forecast = future[['ds','yhat_upper']].tail(7)
sicaklikmax_forecast.yhat_upper = sicaklikmax_forecast.yhat_upper.round(1)