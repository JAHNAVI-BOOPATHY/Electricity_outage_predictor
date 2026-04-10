# Load model
model = pickle.load(open("rf_model.pkl", "rb"))

# Example input
prediction = model.predict([[36, 0, 12]])

print("Outage Prediction:", prediction)