import os
import numpy as np
import flask
import pickle
from flask import Flask, redirect, url_for, request, render_template


# creating instance of the class
app = Flask(__name__, template_folder='template')

# to tell flask what url should trigger the function index()
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')
    
    
# prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,2)
    loaded_model = pickle.load(open("model.pkl","rb")) # load the model
    result = loaded_model.predict(to_predict) # predict the values using loded model
    return result[0]


@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.values()
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
            
        if float(result) == 0:
            prediction='Customers with medium annual income and medium annual spend'
        elif float(result) == 1:
            prediction='Customers with medium to high annual income and low annual spend'
        elif float(result) == 2:
            prediction='Customers with low annual income and low annual spend'
        elif float(result) == 3:
            prediction='Customers with low annual income and high annual spend'
        elif float(result) == 4:
            prediction='Customers with medium to high annual income and high annual spend'
            
        return render_template("result.html",prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True) # use debug = False for jupyter notebook