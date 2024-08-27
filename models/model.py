import sys
import pandas as pd
sys.path.append('/Users/ardahanaytan/Desktop/STAJ/Hava Durumu Tahmin Projesi/data')
from data import df
from sklearn.linear_model import Ridge
rr = Ridge(alpha=0.1)

df['hedef'] = df.shift(-24)['Sicaklik']
df.iloc[-24:] = df.iloc[-48:-24]

predictors = df.columns[~df.columns.isin(['hedef'])]

def backtest(weather, model, predictors, start = 40000, step = 24):
    all_predictions = []
    
    for i in range(start, weather.shape[0], step):
        train = weather.iloc[:i,:]
        test = weather.iloc[i:(i+step),:]
        
        model.fit(train[predictors], train['hedef'])
        
        preds = model.predict(test[predictors])
        
        preds = pd.Series(preds, index=test.index)
        combined = pd.concat([test['hedef'], preds], axis=1)
        
        combined.columns = ['actual','prediction']
        combined['diff'] = (combined['prediction'] - combined['actual']).abs()
        
        all_predictions.append(combined)
    return pd.concat(all_predictions)

predictions = backtest(df, rr, predictors)

def pct_diff(old, new):
    return (new - old) / old

def compute_rolling(weather, horizon, col):
    label = f"rolling_{horizon}_{col}"
    weather[label] = weather[col].rolling(horizon).mean()
    weather[f"{label}_pct"] = pct_diff(weather[label], weather[col])
    return weather

rolling_horizons = [3,24]

for horizon in rolling_horizons:
    for col in ['Basinc','Bulut','Nem','Ruzgar Hizi','Ruzgar Yonu','Sicaklik','Yagis','Kar']:
        df = compute_rolling(df, horizon, col)

df = df.iloc[24:, :]
df = df.fillna(0)

def expand_mean(df):
    return df.expanding(1).mean()

for col in ['Basinc','Bulut','Nem','Ruzgar Hizi','Ruzgar Yonu','Sicaklik','Yagis','Kar']:
    df[f'month_avg_{col}'] = df[col].groupby(df.index.month, group_keys=False).apply(expand_mean)
    df[f'day_avg_{col}'] = df[col].groupby(df.index.day_of_year, group_keys=False).apply(expand_mean)
    df[f'hour_avg_{col}'] = df[col].groupby(df.index.hour, group_keys=False).apply(expand_mean)

predictors = df.columns[~df.columns.isin(['hedef'])]
predictions = backtest(df, rr, predictors)
print(predictions['diff'].mean())

# SICAKLIK ICIN EN DUSUK -> 2.0638077871120877