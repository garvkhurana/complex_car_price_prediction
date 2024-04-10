import pandas as pd
from flask import Flask, render_template, request
import numpy as np
from sklearn.preprocessing import StandardScaler

model = pd.read_pickle("C:\\Users\\Garv Khurana\\Videos\\Car Prize Prediction\\car_prize.pkl")
app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return predict()
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    def convert_input(value):
        return 1 if value and value.lower() == 'yes' else 0

    km_driven = int(request.form.get("km-driven"))
    transmission = convert_input(request.form.get("transmission"))
    seats = int(request.form.get("seats"))
    mileage = float(request.form.get("mileage"))
    engine = int(request.form.get("engine"))
    max_power = float(request.form.get("max_power"))
    torque = float(request.form.get("torque"))
    seller_type = request.form.get("seller_type")
    number_of_years_driven = int(request.form.get("number_of_years_driven") or 0)
    if seller_type and seller_type.lower() == "individual":
        seller_type = 0
    elif seller_type and seller_type.lower() == "dealer":
        seller_type = 1
    else:
        seller_type = 2

    owner = request.form.get("owner")
    if owner and owner.lower() == "first owner":
        owner = 0
    elif owner and owner.lower() == "second owner":
        owner = 1
    elif owner and owner.lower() == "third owner":
        owner = 2
    elif owner and owner.lower() == "fourth & above owner":
        owner = 3
    else:
        owner = 4
        
    fuel=request.form.get('fuel')
    if fuel and fuel.lower()=="Diesel":
        fuel=0
    elif fuel and fuel.lower()=="Petrol":
        fuel=1
    elif fuel and fuel.lower()=="LPG":
        fuel=2
    else : fuel and fuel.lower()=="CNG"
    fuel=3        
     

    features = np.array([km_driven, transmission, seats, mileage, engine, max_power, torque, seller_type, owner,number_of_years_driven,fuel])
    features = features.reshape(1, -1)
    ss=StandardScaler()
    features1=ss.fit_transform(features)
    prediction = model.predict(features1)
    output = f"The predicted price of the car is {prediction[0]}"
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)