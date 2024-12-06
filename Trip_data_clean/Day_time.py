import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_time_category(time):
    # Get category in CST. Random_time is in EST
    if (time >= pd.to_datetime('06:00:00', format='%H:%M:%S').time()) & (time < pd.to_datetime('12:00:00', format='%H:%M:%S').time()):
        return '6AM-12PM'
    if (time >= pd.to_datetime('12:00:00', format='%H:%M:%S').time()) & (time < pd.to_datetime('18:00:00', format='%H:%M:%S').time()):
        return '12PM-6PM'
    if (time >= pd.to_datetime('00:00:00', format='%H:%M:%S').time()) & (time <= pd.to_datetime('06:00:00', format='%H:%M:%S').time()):
        return '12AM-6AM'
    else:
        return '6PM-12AM'

def get_day_category(day_of_week):
    if day_of_week < 5:
        return 'Weekday'
    else:
        return 'Weekend'