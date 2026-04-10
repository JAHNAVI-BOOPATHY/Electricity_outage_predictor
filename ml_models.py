import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from statsmodels.tsa.arima.model import ARIMA

# -------------------------------
# LOAD DATA
# -------------------------------
data = pd.read_csv("dataset.csv")

# -------------------------------
# FEATURES & TARGETS
# -------------------------------
X = data[['temp', 'rain', 'wind']]

y_class = data['outage']   # classification
y_reg = data['count']     # regression

# -------------------------------
# SPLIT DATA (for classification)
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_class, test_size=0.2
)

# -------------------------------
# RANDOM FOREST CLASSIFIER
# -------------------------------
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

pickle.dump(clf, open("rf_model.pkl", "wb"))
print("RF Model saved ✅")

# -------------------------------
# RANDOM FOREST REGRESSOR
# -------------------------------
reg = RandomForestRegressor()
reg.fit(X, y_reg)

pickle.dump(reg, open("reg_model.pkl", "wb"))
print("Regression Model saved ✅")

# -------------------------------
# ARIMA MODEL (TIME SERIES)
# -------------------------------
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

ts = data['count']

arima_model = ARIMA(ts, order=(1,1,1))
arima_fit = arima_model.fit()

# Forecast next 3 days
forecast = arima_fit.forecast(steps=3)

print("Next 3 days forecast:")
print(forecast)