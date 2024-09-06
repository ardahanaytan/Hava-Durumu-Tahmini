import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions

df_y = pd.DataFrame(df['Yagmur'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Yagmur': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Yagmur': 'min'}, inplace=True)
df_top = df_y.resample('D').sum()
df_top.rename(columns = {'Yagmur': 'sum'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Yagmur': 'mean'}, inplace=True)
df_ = pd.concat([df_top, df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions(df_)
