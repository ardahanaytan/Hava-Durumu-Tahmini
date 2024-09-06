import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_mean

df_y = pd.DataFrame(df['Bulut'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Bulut': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Bulut': 'min'}, inplace=True)
df_top = df_y.resample('D').sum()
df_top.rename(columns = {'Bulut': 'sum'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Bulut': 'mean'}, inplace=True)
df_ = pd.concat([df_top, df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_mean(df_)
future[['yhat_lower', 'yhat_upper', 'yhat']] -= future['yhat_lower'].min()
