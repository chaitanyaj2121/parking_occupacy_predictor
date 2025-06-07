import pandas as pd
import statsmodels.api as sm
import joblib

# Load and preprocess data
def prepare_data():
    df = pd.read_csv('dataset.csv')
    df['LastUpdated'] = pd.to_datetime(df['LastUpdated'])
    df['Date'] = df['LastUpdated'].dt.date
    df['Time'] = df['LastUpdated'].dt.time
    df.drop(['SystemCodeNumber', 'Capacity', 'LastUpdated'], axis=1, inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    y = df['Occupancy'].resample('D').mean()
    y.fillna(method='bfill', inplace=True)
    return y

# Train and save model
def train_and_save_model():
    y = prepare_data()
    model = sm.tsa.statespace.SARIMAX(
        y,
        order=(1, 1, 1),
        seasonal_order=(0, 1, 1, 4),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    results = model.fit()
    joblib.dump(results, 'parking_model.pkl')
    print("Model trained and saved successfully!")

if __name__ == '__main__':
    train_and_save_model()