from flask import Flask, render_template
from flask.globals import request
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
app = Flask(__name__, template_folder='template')

model = joblib.load('model_j')


@app.route("/", methods=['GET'])

@app.route("/")
def home():
    return render_template("/index.html")

standard_to = StandardScaler()

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        year = int(request.form['year'])
        no_year = int(2021 - year)
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = float(request.form['Kms_Driven'])

        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Indivisual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual == 'Mannual Car':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        

        predict = model.predict([[year, Present_Price, Kms_Driven, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                Seller_Type_Individual, Transmission_Manual, no_year]])

        if predict<0:
            return render_template('/index.html',predict="Sorry you cannot sell this car")
            
        #condition for prediction when values are valid
        else:
            return render_template('/index.html',predict="You Can Sell the Car at {} lakhs".format(round(predict[0],2)))
            
    #html form to be displayed on screen when no values are inserted; without any output or prediction
    else:
        return render_template('/index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
