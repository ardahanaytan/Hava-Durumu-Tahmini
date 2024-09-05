import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from model import arima_model

df_t = pd.DataFrame({'Sicaklik': df['Sicaklik']})

error, combined = arima_model(df_t)
print(combined)