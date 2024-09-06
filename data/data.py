import pandas as pd

df_basinc = pd.read_csv('data/weather_datas/basinc.csv')
df_bulut = pd.read_csv('data/weather_datas/bulut.csv')
df_nem = pd.read_csv('data/weather_datas/nem.csv')
df_ruzgar = pd.read_csv('data/weather_datas/ruzgar.csv')
df_sicaklik = pd.read_csv('data/weather_datas/sicaklik.csv')
df_yagmur = pd.read_csv('data/weather_datas/yagmur.csv')
df_kar = pd.read_csv('data/weather_datas/kar.csv')

tables = [df_nem, df_ruzgar, df_sicaklik, df_yagmur, df_kar]
df = pd.merge(df_basinc, df_bulut, on=['location'])
for i in tables:
    df = pd.merge(df, i, on=['location'])

df = df.dropna()

df['Yil'] = df['location'].str[:4].astype(int)
df['Ay'] = df['location'].str[4:6].astype(int)
df['Gun'] = df['location'].str[6:8].astype(int)
df['Saat'] = df['location'].str[9:].str[:2].astype(int)
df['datetime'] = pd.to_datetime(df[['Yil', 'Ay', 'Gun']].astype(str).agg('-'.join, axis=1) + ' ' + 
                                df['Saat'].astype(str), format='%Y-%m-%d %H')
df.set_index('datetime', inplace=True)
df.drop(columns=['location', 'Yil', 'Ay', 'Gun', 'Saat'], inplace=True)
