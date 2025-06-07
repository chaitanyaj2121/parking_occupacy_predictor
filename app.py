from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('parking_model.pkl')

# Last date in training data
LAST_TRAINING_DATE = pd.Timestamp('2016-12-19')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        date_str = request.form['date']
        try:
            # Convert input to pandas Timestamp
            input_date = pd.Timestamp(date_str)
            
            # Calculate days from last training date
            steps = (input_date - LAST_TRAINING_DATE).days
            
            if steps < 1:
                return render_template('index.html', 
                                      error="Date must be after 2016-12-19",
                                      prediction=prediction)
            
            # Get forecast
            forecast = model.get_forecast(steps=steps)
            prediction = round(forecast.predicted_mean.iloc[-1])
            
        except Exception as e:
            return render_template('index.html', 
                                  error=f"Error: {str(e)}",
                                  prediction=prediction)
    
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)