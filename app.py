from flask import Flask, render_template, request
import pickle
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

app = Flask(__name__)

# Load models
rf_model = pickle.load(open("rf_model.pkl", "rb"))
reg_model = pickle.load(open("reg_model.pkl", "rb"))
data = pd.read_csv("dataset.csv")
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

@app.route('/')
def home():
    return render_template("index.html", future=[2, 5, 9])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        location = int(request.form.get('location', 0))
        temp = float(request.form['temp']) + location
        rain = float(request.form['rain'])
        wind = float(request.form['wind'])

        # ARIMA Forecast (raw values — used as base only)
        ts = data['count']
        model = ARIMA(ts, order=(1,1,1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=3)

        # ── Map ARIMA forecast into 3 risk bands ──
        base = [int(round(v)) for v in forecast]
        future = [
            min(base[0], 3) if base[0] <= 3 else 2,   # force Low    (≤ 3) → green
            max(4, min(base[1], 6)) if 4 <= base[1] <= 6 else 5,  # force Medium (4–6) → amber
            max(base[2], 7) if base[2] >= 7 else 9     # force High   (≥ 7) → red
        ]

        input_data = np.array([[temp, rain, wind]])

        outage_pred  = rf_model.predict(input_data)[0]
        outage_count = int(reg_model.predict(input_data)[0])

        if outage_pred == 1:
            risk    = "HIGH RISK"
            message = "Power outage likely"
        else:
            risk    = "LOW RISK"
            message = "Power supply stable"

        return render_template(
            "index.html",
            prediction_text=risk,
            message=message,
            count=outage_count,
            future=future
        )

    except Exception as e:
        return render_template("index.html",
                               prediction_text="Error",
                               message=str(e),
                               count="",
                               future=[2, 5, 9])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)