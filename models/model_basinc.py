import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_withoutsum

df_y = pd.DataFrame(df['Basinc'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Basinc': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Basinc': 'min'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Basinc': 'mean'}, inplace=True)
df_ = pd.concat([df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_withoutsum(df_)
