import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle


app = Flask(__name__)
# model = pickle.load(open('car_mpg.pkl','rb'))
with open('car_mpg.pkl', 'rb') as file:
    model = pickle.load(file)
if not hasattr(model, 'predict'):
    raise ValueError("Loaded model does not have a predict method. Ensure 'car_mpg.pkl' is a trained model with a predict method.")


@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')
    #return render_template('index.html')

@app.route('/predict',methods = ['POST'])
def predict():
    model = pickle.load(open('car_mpg.pkl','rb'))
    int_features = [float(x) for x in request.form.values()]
    if len(int_features) != 13:
        raise ValueError(f"Expected 13 features, but got {int_features}.")
    f = np.array(int_features)
    # final_features = [f]
    prediction = model.predict([f])
    print(prediction[0])

    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="MPG for the car is: {}".format(prediction[0]))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)



if __name__ == '__main__':
    app.run(debug=True)