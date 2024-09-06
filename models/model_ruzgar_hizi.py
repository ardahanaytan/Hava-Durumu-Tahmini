import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_mean

df_y = pd.DataFrame(df['Ruzgar_Hizi'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Ruzgar_Hizi': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Ruzgar_Hizi': 'min'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Ruzgar_Hizi': 'mean'}, inplace=True)
df_sum = df_y.resample('D').sum()
df_sum.rename(columns = {'Ruzgar_Hizi': 'sum'}, inplace=True)
df_ = pd.concat([df_sum, df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_mean(df_)
#VERILER GUNCELLENDIKTEN SONRA TEKRAR BAKILACAK
