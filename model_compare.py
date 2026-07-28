import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from prophet import Prophet

monthly_ts = pd.read_pickle('monthly_ts.pkl')
ts = monthly_ts.set_index('date')['total_revenue'].asfreq('ME')
print('ts length:', len(ts), ts.index.min(), '->', ts.index.max())

# 2024-07 is a partial month in the raw daily sales export (data cutoff mid-period);
# excluding it avoids penalizing both models for an artificially low last point.
ts_full = ts.iloc[:-1]
print('using ts_full length:', len(ts_full), 'up to', ts_full.index.max())

TEST_H = 6
train = ts_full.iloc[:-TEST_H]
test  = ts_full.iloc[-TEST_H:]
print('train:', len(train), 'test:', len(test))
print(test)

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))

def mae(y_true, y_pred):
    return np.mean(np.abs(np.array(y_true) - np.array(y_pred)))

# ---------- SARIMA ----------
sarima_model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12),
                        enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
sarima_fc = sarima_model.get_forecast(steps=TEST_H)
sarima_pred = sarima_fc.predicted_mean
sarima_ci = sarima_fc.conf_int(alpha=0.05)

sarima_mae  = mae(test.values, sarima_pred.values)
sarima_rmse = rmse(test.values, sarima_pred.values)
sarima_mape = mape(test.values, sarima_pred.values)
print('\nSARIMA  MAE={:.0f}  RMSE={:.0f}  MAPE={:.2f}%'.format(sarima_mae, sarima_rmse, sarima_mape))

# ---------- Prophet ----------
prophet_df = train.reset_index().rename(columns={'date':'ds', 'total_revenue':'y'})
m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m.fit(prophet_df)
future = m.make_future_dataframe(periods=TEST_H, freq='ME')
prophet_fc = m.predict(future)
prophet_pred = prophet_fc.set_index('ds')['yhat'].reindex(test.index)

prophet_mae  = mae(test.values, prophet_pred.values)
prophet_rmse = rmse(test.values, prophet_pred.values)
prophet_mape = mape(test.values, prophet_pred.values)
print('Prophet MAE={:.0f}  RMSE={:.0f}  MAPE={:.2f}%'.format(prophet_mae, prophet_rmse, prophet_mape))

results = pd.DataFrame({
    'Model': ['SARIMA(1,1,1)(1,1,1,12)', 'Prophet'],
    'MAE': [sarima_mae, prophet_mae],
    'RMSE': [sarima_rmse, prophet_rmse],
    'MAPE_%': [sarima_mape, prophet_mape],
})
print('\n', results)

# ---------- Refit both on full history for the actual forward-looking forecast ----------
FORECAST_STEPS = 12
sarima_full = SARIMAX(ts_full, order=(1,1,1), seasonal_order=(1,1,1,12),
                       enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
sarima_full_fc = sarima_full.get_forecast(steps=FORECAST_STEPS)
sarima_full_mean = sarima_full_fc.predicted_mean
sarima_full_ci = sarima_full_fc.conf_int(alpha=0.05)

prophet_full_df = ts_full.reset_index().rename(columns={'date':'ds', 'total_revenue':'y'})
m_full = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
m_full.fit(prophet_full_df)
future_full = m_full.make_future_dataframe(periods=FORECAST_STEPS, freq='ME')
prophet_full_fc = m_full.predict(future_full)

# Save everything needed for charts / report
import pickle
with open('model_compare.pkl', 'wb') as f:
    pickle.dump({
        'ts_full': ts_full, 'train': train, 'test': test,
        'sarima_pred': sarima_pred, 'sarima_ci': sarima_ci,
        'prophet_pred': prophet_pred,
        'results': results,
        'sarima_full_mean': sarima_full_mean, 'sarima_full_ci': sarima_full_ci,
        'prophet_full_fc': prophet_full_fc,
    }, f)
print('\nSaved model_compare.pkl')
