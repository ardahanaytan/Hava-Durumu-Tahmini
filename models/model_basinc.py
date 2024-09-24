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

future['yhat'] = ((future['yhat'] - future['yhat'].min()) / (future['yhat'].max() - future['yhat'].min())) * (df['Basinc'].max() - df['Basinc'].min()) + df['Basinc'].min()
basinc_forecast = future[['ds','yhat']].tail(7)
basinc_forecast.yhat = basinc_forecast.yhat.round(1)

gun_kisaltmalari = {
    0: 'Pzt',  
    1: 'Sal', 
    2: 'Çar',  
    3: 'Per', 
    4: 'Cum', 
    5: 'Cmt',  
    6: 'Paz'   
}

basinc_forecast['ds'] = basinc_forecast['ds'].dt.dayofweek.map(gun_kisaltmalari)
print(basinc_forecast)