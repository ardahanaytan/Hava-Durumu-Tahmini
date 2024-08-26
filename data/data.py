import pandas as pd
from sklearn import preprocessing

df_basinc = pd.read_csv('data/weather_datas/basinc.csv')
df_bulut = pd.read_csv('data/weather_datas/bulut.csv')
df_nem = pd.read_csv('data/weather_datas/nem.csv')
df_ruzgar = pd.read_csv('data/weather_datas/ruzgar_hizi_yonu.csv')
df_sicaklik = pd.read_csv('data/weather_datas/sicaklik.csv')
df_yagis = pd.read_csv('data/weather_datas/yagis_miktari.csv')

ctable = ['Basinc','Bulut','Nem','Ruzgar Hizi','Ruzgar Yonu','Sicaklik','Yagis']
tables = [df_nem, df_ruzgar, df_sicaklik, df_yagis]
real_df = pd.merge(df_basinc, df_bulut, on = ['Yil', 'Ay', 'Gun', 'Saat'])

for i in tables:
    real_df = pd.merge(real_df, i, on = ['Yil', 'Ay', 'Gun', 'Saat'])

df = real_df.copy()
df = df.dropna()

df_mean = df['Basinc'].mean()
df_std = df['Basinc'].std()

df_st = pd.DataFrame(preprocessing.scale(df.select_dtypes('float64')), columns=ctable)
for i in ctable:
    df[i] = df_st[i]

df['Yil'] = df['Yil'].str[1:].astype(int)
df['Ay'] = df['Ay'].map({
    'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6,
    'Temmuz': 7, 'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
})
df['Gun'] = df['Gun'].str[1:].astype(int)
df['Saat'] = df['Saat'].str[1:].str[:2].astype(int)

df['datetime'] = pd.to_datetime(df[['Yil', 'Ay', 'Gun']].astype(str).agg('-'.join, axis=1) + ' ' + df['Saat'].astype(str), format='%Y-%m-%d %H')
df.set_index('datetime', inplace=True)
df.drop(columns=['Yil', 'Ay', 'Gun', 'Saat'], inplace=True)