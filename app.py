from flask import Flask, render_template, request
from main import predict_occupancy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    system_code = request.form['system_code']
    capacity = int(request.form['capacity'])
    timestamp = request.form['timestamp']

    predicted_occupancy = predict_occupancy(system_code, capacity, timestamp)

    return render_template('index.html', prediction=predicted_occupancy)

if __name__ == '__main__':
    app.run(debug=True)
