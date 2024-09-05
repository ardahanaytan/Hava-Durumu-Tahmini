import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
reg = Ridge(alpha=.1)
from statsmodels.tsa.arima.model import ARIMA




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
    return error, combined






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
    return error, combined








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
    return error, combined








def arima_model(df_t):
    train_df = df_t[:'2020'].resample('M').mean()
    test_df = df_t['2021':].resample('M').mean()
    model = ARIMA(train_df.values, order=(2,0,2))
    model_fit = model.fit()
    forecast_obj = model_fit.get_forecast(steps=44)
    fc = forecast_obj.predicted_mean
    fc_series = pd.Series(fc, index=test_df.index)
    error = mean_absolute_error(test_df, fc_series)
    return error, fc_series