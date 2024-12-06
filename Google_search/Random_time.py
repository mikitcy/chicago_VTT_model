
import random
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta, MO
import pandas as pd
import pytz


def random_time(row):
    if pd.isnull(row['Start']):
        return pd.NaT
    if isinstance(row['Start'], str):
        # Convert the string [Starttime] to naive datetime object
        starttime_chicago_naive = datetime.strptime(row['Start'], '%m/%d/%Y %I:%M:%S %p')
        chicago_tz = pytz.timezone('America/Chicago')
        starttime_chicago = chicago_tz.localize(starttime_chicago_naive)
    else:
        starttime_chicago = row['Start']

    # Convert to Eastern Standard Time (EST)
    est_tz = pytz.timezone('America/New_York')
    starttime_est = starttime_chicago.astimezone(est_tz)

    # Randomly assign time in a 15-min block
    random_additional_minutes = random.randint(0, 14)
    random_time = starttime_est + timedelta(minutes=random_additional_minutes)

    day_of_week = random_time.weekday()
    current_time = datetime.now(est_tz)

    days_until_next = (day_of_week - current_time.weekday()) % 7 + 7
    future_date = current_time + timedelta(days=days_until_next)

    future_date_est = est_tz.localize(datetime.combine(future_date.date(), datetime.min.time()))
    future_date_est = future_date_est + timedelta(hours=random_time.hour, minutes=random_time.minute)

    return future_date_est