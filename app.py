from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('parking_model.pkl')

# Last date in training data
LAST_TRAINING_DATE = pd.Timestamp('2016-12-19')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    if request.method == 'POST':
        date_str = request.form['date']
        try:
            # Convert input to pandas Timestamp
            input_date = pd.Timestamp(date_str)
            
            # Calculate days from last training date
            steps = (input_date - LAST_TRAINING_DATE).days
            
            if steps < 1:
                error = "Date must be after 2016-12-19"
            else:
                # Get forecast
                forecast = model.get_forecast(steps=steps)
                prediction = round(forecast.predicted_mean.iloc[-1])
                
        except Exception as e:
            error = f"Error: {str(e)}"
    
    return render_template('index.html', prediction=prediction, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)