import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
reg = Ridge(alpha=.1)
from prophet import Prophet

def create_predictions(df):
    df['target'] = df.shift(-1)['sum']
    df = df.iloc[:-1,:].copy()
    predictors = ['sum', 'mean', 'max', 'min']
    train = df.loc[:'2021-12-31']
    test = df.loc['2022-01-01':]
    reg.fit(train[predictors], train['target'])
    predictions = reg.predict(test[predictors])
    error = mean_absolute_error(test['target'], predictions)
    combined = pd.concat([test['target'], pd.Series(predictions, index=test.index)], axis=1)
    combined.columns = ['actual', 'predictions']
    combined['predictions'] -= combined['predictions'].min()
    forecast = future_predict(combined)
    return error, combined, forecast

def create_predictions_mean(df):
    df['target'] = df.shift(-1)['mean']
    df = df.iloc[:-1,:].copy()
    predictors = ['sum', 'mean', 'max', 'min']
    train = df.loc[:'2021-12-31']
    test = df.loc['2022-01-01':]
    reg.fit(train[predictors], train['target'])
    predictions = reg.predict(test[predictors])
    error = mean_absolute_error(test['target'], predictions)
    combined = pd.concat([test['target'], pd.Series(predictions, index=test.index)], axis=1)
    combined.columns = ['actual', 'predictions']
    forecast = future_predict(combined)
    return error, combined, forecast

def create_predictions_withoutsum(df):
    df['target'] = df.shift(-1)['max']
    df = df.iloc[:-1,:].copy()
    df['month_max'] = df['max'].rolling(30).mean()
    df['month_day_max'] = df['month_max'] / df['max']
    df['max_min'] = df['max'] / df['min']
    df = df.iloc[30:,:].copy()
    predictors = ['mean', 'max', 'min', 'month_max', 'month_day_max', 'max_min']
    train = df.loc[:'2021-12-31']
    test = df.loc['2022-01-01':]
    reg.fit(train[predictors], train['target'])
    predictions = reg.predict(test[predictors])
    error = mean_absolute_error(test['target'], predictions)
    combined = pd.concat([test['target'], pd.Series(predictions, index=test.index)], axis=1)
    combined.columns = ['actual', 'predictions']
    forecast = future_predict(combined)
    return error, combined, forecast

def future_predict(combined):
    m = Prophet()
    prophet_df = combined.reset_index().rename(columns={'datetime': 'ds', 'predictions':'y'})
    m.fit(prophet_df[['ds', 'y']])
    future = m.make_future_dataframe(periods=15, freq='D')
    forecast = m.predict(future)
    return forecast