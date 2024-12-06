import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('filtered_tripdata.csv')
print(df.dtypes)

df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Date'] = pd.to_datetime(df['Date'])
df['Hour'] = df['Start'].dt.hour

datetime.strptime('2022-01-01 01:00:00', '%Y-%m-%d %H:%M:%S')
df['Start'] = pd.to_datetime(df['Start'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['End'] = pd.to_datetime(df['End'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

df = df.sample(frac=1).reset_index(drop=True)

grouped_df = df.groupby(['Date', 'Hour', 'Pickup_CA', 'Dropoff_CA']).apply(
    lambda x: x.sample(1).assign(Count=len(x))
).reset_index(drop=True)

desired_columns = [
    'Date', 'Hour', 'Pickup_CA', 'Dropoff_CA',
    'Start', 'Starttime', 'End', 'Endtime',
    'TNC_miles', 'TNC_duration', 'TNC_fare', 'TNC_total_fare',
    'Origin', 'OriginLat', 'OriginLong',
    'Destination', 'DestinationLat', 'DestinationLong', 'Count']

##############################################
#  Filter out trips between 12am - 6am and error for direction search
print("24H: ", len(grouped_df))
grouped_df = grouped_df[grouped_df['Hour'] > 5]
print("18H: ", len(grouped_df))
##############################################
#  Filter out O'Hare airport (CA 76)
grouped_df = grouped_df[grouped_df['Pickup_CA'] != 76]
grouped_df = grouped_df[grouped_df['Dropoff_CA'] != 76]
print("Without airport: ", len(grouped_df))
##############################################

grouped_df.to_csv('grouped_tripdata.csv', index=False)
print(grouped_df)

print("Completed")