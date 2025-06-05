import datetime

# Placeholder prediction logic
def predict_occupancy(system_code, capacity, timestamp):
    # Convert timestamp to time-based feature
    time_obj = datetime.datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
    hour = time_obj.hour
    minute = time_obj.minute

    # Dummy logic: just simulate some increasing occupancy
    predicted = int((hour + minute / 60) / 12 * capacity)
    return min(predicted, capacity)
