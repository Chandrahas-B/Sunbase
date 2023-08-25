from flask import Flask, render_template, request
from src import ChurnPredictor


app = Flask(__name__)


@app.route('/', methods= ['POST', 'GET'])
def index():
    pred = None
    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        location = request.form.get('location')
        subscription = request.form.get('subscription')
        monthlyBill = request.form.get('monthlyBill')
        totalGB = request.form.get('totalGB')
        predictor = ChurnPredictor()
        predictor.create_df(age, gender, location, subscription,
                            monthlyBill, totalGB)
        predictor.transformation()
        pred = predictor.ensemble()
        print(f"pred: {pred}")
        
    return render_template('index.html', pred = pred)

if __name__ == '__main__':
    app.run(debug= True, host= '0.0.0.0', port = 5000)