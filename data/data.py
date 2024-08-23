import pandas as pd

df_basinc = pd.read_csv('data/weather_datas/basinc.csv')
df_bulut = pd.read_csv('data/weather_datas/bulut.csv')
df_nem = pd.read_csv('data/weather_datas/nem.csv')
df_ruzgar = pd.read_csv('data/weather_datas/ruzgar_hizi_yonu.csv')
df_sicaklik = pd.read_csv('data/weather_datas/sicaklik.csv')
df_yagis = pd.read_csv('data/weather_datas/yagis_miktari.csv')

tables = [df_nem, df_ruzgar, df_sicaklik, df_yagis]
real_df = pd.merge(df_basinc, df_bulut, on = ['Yil', 'Ay', 'Gun', 'Saat'])

for i in tables:
    real_df = pd.merge(real_df, i, on = ['Yil', 'Ay', 'Gun', 'Saat'])

real_df.Yil = pd.Categorical(real_df.Yil)
real_df.Ay = pd.Categorical(real_df.Ay)
real_df.Gun = pd.Categorical(real_df.Gun)
real_df.Saat = pd.Categorical(real_df.Saat)

df = real_df.copy()
df = df.dropna()

print(df.tail())
