import pandas as pd
import numpy as np

def clean(tripdata_df):

    tripdata_df.dropna(subset=['Trip Start Timestamp', 'Pickup Community Area', 'Dropoff Community Area', 'Pickup Centroid Location', 'Dropoff Centroid Location', 'Fare'],
                       inplace=True)

    tripdata_df['Trip Start Timestamp'] = pd.to_datetime(tripdata_df['Trip Start Timestamp'])
    tripdata_df['Date'] = tripdata_df['Trip Start Timestamp'].dt.date

    tripdata_df['Trip Miles'] = tripdata_df['Trip Miles'].astype(float)
    tripdata_df['Trip Seconds'] = pd.to_numeric(tripdata_df['Trip Seconds'], errors='coerce').fillna(0).astype(int)
    tripdata_df['Fare'] = tripdata_df['Fare'].astype(float)
    tripdata_df['Trip Total'] = tripdata_df['Trip Total'].astype(float)
    tripdata_df['Trip_Minutes'] = tripdata_df['Trip Seconds'] / 60.0

    tripdata_df['Origin'] = tripdata_df['Pickup Centroid Latitude'].astype(str) + ', ' + tripdata_df['Pickup Centroid Longitude'].astype(str)
    tripdata_df['Destination'] = tripdata_df['Dropoff Centroid Latitude'].astype(str) + ', ' + tripdata_df['Dropoff Centroid Longitude'].astype(str)

    return tripdata_df

def filter(tripdata_df):

    tripdata_df['Trip Start Timestamp'] = pd.to_datetime(tripdata_df['Trip Start Timestamp'])
    tripdata_df['Trip End Timestamp'] = pd.to_datetime(tripdata_df['Trip End Timestamp'])

    filtered_df = tripdata_df.assign(
        Date=tripdata_df['Date'],
        Start=tripdata_df['Trip Start Timestamp'],
        Starttime=tripdata_df['Trip Start Timestamp'].dt.time,
        End=tripdata_df['Trip End Timestamp'],
        Endtime=tripdata_df['Trip End Timestamp'].dt.time,
        Pickup_CA=tripdata_df['Pickup Community Area'],
        Dropoff_CA=tripdata_df['Dropoff Community Area'],
        Origin=tripdata_df['Origin'],
        OriginLat=tripdata_df['Pickup Centroid Latitude'],
        OriginLong=tripdata_df['Pickup Centroid Longitude'],
        Destination=tripdata_df['Destination'],
        DestinationLat=tripdata_df['Dropoff Centroid Latitude'],
        DestinationLong=tripdata_df['Dropoff Centroid Longitude'],
        TNC_miles=tripdata_df['Trip Miles'],
        TNC_duration=tripdata_df['Trip_Minutes'],
        TNC_fare=tripdata_df['Fare'],
        TNC_total_fare=tripdata_df['Trip Total']
    )

    final_columns = [
        'Date', 'Start', 'Starttime', 'End', 'Endtime', 'Pickup_CA', 'Dropoff_CA',
        'Origin', 'OriginLat', 'OriginLong', 'Destination', 'DestinationLat', 'DestinationLong',
        'TNC_miles', 'TNC_duration', 'TNC_fare', 'TNC_total_fare'
    ]

    final_df = filtered_df[final_columns]

    return final_df
