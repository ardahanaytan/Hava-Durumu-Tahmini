import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_mean

df_y = pd.DataFrame(df['Ruzgar_Yonu'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Ruzgar_Yonu': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Ruzgar_Yonu': 'min'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Ruzgar_Yonu': 'mean'}, inplace=True)
df_sum = df_y.resample('D').sum()
df_sum.rename(columns = {'Ruzgar_Yonu': 'sum'}, inplace=True)
df_ = pd.concat([df_sum, df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_mean(df_)
future['yhat'] = ((future['yhat'] - future['yhat'].min()) / (future['yhat'].max() - future['yhat'].min())) * (df['Ruzgar_Yonu'].max() - df['Ruzgar_Yonu'].min()) + df['Ruzgar_Yonu'].min()
ruzgaryonu_forecast = future[['ds','yhat']].tail(7)
ruzgaryonu_forecast.yhat = ruzgaryonu_forecast.yhat.round(2)