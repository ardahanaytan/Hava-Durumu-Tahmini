import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import create_predictions_withoutsum

df_y = pd.DataFrame(df['Nem'])
df_max = df_y.resample('D').max()
df_max.rename(columns = {'Nem': 'max'}, inplace=True)
df_min = df_y.resample('D').min()
df_min.rename(columns = {'Nem': 'min'}, inplace=True)
df_ort = df_y.resample('D').mean()
df_ort.rename(columns = {'Nem': 'mean'}, inplace=True)
df_ = pd.concat([df_ort, df_max, df_min], axis=1)

error, combined, future = create_predictions_withoutsum(df_)
#future[['yhat_lower', 'yhat_upper', 'yhat']] -= 45
#TAM OLARAK OLMAMIS BI KONTROL EDILECEK
#YENI VERILER ILE DAHA IYI OLABILIR VERILERIN BITTIGI HAFTA NEM COK YUKSEKMIS, MODELDE DAHA DA YUKSELMEYE DEVAM EDIYOR