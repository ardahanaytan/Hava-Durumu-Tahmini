import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions

df_y = pd.DataFrame(df['Kar'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Kar': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Kar': 'min'}, inplace=True)
df_top = df_y.resample('D').sum()
df_top.rename(columns = {'Kar': 'sum'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Kar': 'mean'}, inplace=True)
df_ = pd.concat([df_top, df_ort, df_max, df_min], axis=1)

error, combined = create_predictions(df_)

combined['predictions'] -= combined['predictions'].min()