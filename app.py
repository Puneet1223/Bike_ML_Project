from flask import Flask, request, render_template
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load trained model
model = pickle.load(open("pipe1.pkl", "rb"))

# Load dataset to extract dropdown values
df = pd.read_pickle("df1.pkl")   # change to read_csv if you saved as CSV

# Helper function
def safe_cast(value, cast_type, default=None):
    try:
        return cast_type(value)
    except (TypeError, ValueError):
        return default

@app.route('/')
def home():
    owners = df["owner"].unique().tolist()
    brands = df["Brand"].unique().tolist()
    locations = df["location"].unique().tolist()
    return render_template('index.html',
                           owners=owners,
                           brands=brands,
                           locations=locations)

@app.route('/predict', methods=['POST'])
def predict():
    model_year = safe_cast(request.form.get('model_year'), int, 0)
    kms_driven = safe_cast(request.form.get('kms_driven'), float, 0.0)
    owner = request.form.get('owner', "first owner")
    location = request.form.get('location', "Other")
    mileage = safe_cast(request.form.get('mileage'), float, 0.0)
    power = safe_cast(request.form.get('power'), float, 0.0)
    cc = safe_cast(request.form.get('cc'), float, 0.0)
    Brand = request.form.get('Brand', "Unknown")
    bike_age = safe_cast(request.form.get('bike__age'), int, 0)

    # Convert into dataframe
    input_df = pd.DataFrame([[model_year, kms_driven, owner, location,
                              mileage, power, cc, Brand, bike_age]],
                            columns=['model_year','kms_driven','owner',
                                     'location','mileage','power','cc',
                                     'Brand','bike__age'])

    prediction = np.exp(model.predict(input_df)[0])
    return render_template('index.html',
                           prediction_text=f"Predicted Price: ₹{round(prediction,2)}",
                           owners=df["owner"].unique().tolist(),
                           brands=df["Brand"].unique().tolist(),
                           locations=df["location"].unique().tolist())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

