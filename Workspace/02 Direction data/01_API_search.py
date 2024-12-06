import pandas as pd
import os
from datetime import datetime
import ast

from Google_search.Google_transit import get_transit_google
from Google_search.Random_location import get_random_location_airportfix
from Google_search.Direction import hours_to_minutes, str_to_miles
from Trip_data_clean.Weather_event import find_event_type
from Google_search.Random_location import get_random_coordinate_sameCA
from Google_search.Random_time import random_time

### Read csv
folder_path = 'tripdata.csv'

Tripdata = {}

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)

        df_name = os.path.splitext(filename)[0]
        Tripdata[df_name] = df

df = Tripdata['df_20220316']

### Randomization
df['Start'] = pd.to_datetime(df['Start'])
df['Start'] = df['Start'].dt.strftime('%m/%d/%Y %I:%M:%S %p')

if df['Origin'] == df['Destination']:
    df['Random_origin'] = df.apply(get_random_coordinate_sameCA, axis=1)
    df['Random_destination'] = df.apply(get_random_coordinate_sameCA, axis=1)
else:
    get_random_location_airportfix(df)

df['Random_time'] = df.apply(random_time, axis=1)
df['Random_time'] = pd.to_datetime(df['Random_time'], format="%Y-%m-%d-%H:%M")

def split_dataframe(df, chunk_size):
    chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
    return chunks

chunks = split_dataframe(df, 1500)

results_df = pd.DataFrame()
results = []

### Google search
for index, chunk in enumerate(chunks):
    chunk['Direction'] = chunk.apply(get_transit_google, axis=1)
    results.append(chunk)
    print(datetime.now())

results_df = pd.concat(results)

df = results_df
df = df[df['Direction'].notna() & (df['Direction'] != '[]')]

direction_list = []
error_count = 0
fontSize_found =0
toDelete_row = []

for i, data_raw in enumerate(df['Direction']):
    html_idx = data_raw.find('"html_instructions"')
    while html_idx > 0:
        end_idx = data_raw.find('", ', html_idx)
        data_raw = data_raw[:html_idx] + data_raw[end_idx + 3:]
        html_idx = data_raw.find('"html_instructions"')
    try:
        direction_list.append(ast.literal_eval(data_raw))
    except:
        direction_list.append([])
        toDelete_row.append(i)
        if data_raw.find('"font-size') > 0:
            fontSize_found += 1
        error_count += 1
    #print(data_raw)
    #break

print(error_count)
print(fontSize_found)

df['Direction'] = direction_list
df = df[~df.index.isin(toDelete_row)]

for index, row in df.iterrows():
    data = row['Direction']
    random_time = row['Random_time']

    for item in data:

        for leg in item['legs']:
            duration_str = leg['duration']['text']
            distance_str = leg['distance']['text']
            duration_mins = hours_to_minutes(duration_str)
            distance_miles = str_to_miles(distance_str)

            if 'departure_time' in leg:
                departure_time_result_unix = leg['departure_time']['value']
                # Assuming Random_time is in Unix timestamp format
                random_time_unix = pd.to_datetime(random_time).timestamp()
                # Calculate the time gap in minutes
                time_gap = (departure_time_result_unix - random_time_unix) / 60
            else:
                time_gap = None

            #Transit details
            time_bus = 0
            time_subway = 0
            time_train = 0
            time_other = 0
            time_walk = 0
            mile_bus = 0
            mile_subway = 0
            mile_train = 0
            mile_walk = 0

            for step in leg['steps']:

                if 'transit_details' in step:

                    transit_name = step['transit_details']['line']['vehicle']['name']

                    step_duration = hours_to_minutes(step['duration']['text'])
                    step_miles = str_to_miles(step['distance']['text'])

                    if transit_name == "Bus":
                        time_bus += step_duration
                        mile_bus += step_miles
                    elif transit_name == "Train":
                        time_train += step_duration
                        mile_train += step_miles
                    elif transit_name == "Subway":
                        time_subway += step_duration
                        mile_subway += step_miles

                else:
                    step_duration = hours_to_minutes(step['duration']['text'])
                    step_miles = str_to_miles(step['distance']['text'])

                    time_walk += step_duration
                    mile_walk += step_miles

                time_other = hours_to_minutes(leg['duration']['text']) - (time_bus + time_train + time_subway + time_walk)

                if time_other < 0:
                    time_other = 0


    df.at[index, 'Transit_miles'] = distance_miles
    df.at[index, 'Transit_duration'] = duration_mins
    df.at[index, 'Bus_duration'] = time_bus
    df.at[index, 'Subway_duration'] = time_subway
    df.at[index, 'Train_duration'] = time_train
    df.at[index, 'Other_duration'] = time_other
    df.at[index, 'Walk_duration'] = time_walk
    df.at[index, 'Time_gap'] = time_gap
    df.at[index, 'Bus_miles'] = mile_bus
    df.at[index, 'Subway_miles'] = mile_subway
    df.at[index, 'Train_miles'] = mile_train
    df.at[index, 'Walk_miles'] = mile_walk

df_event = pd.read_csv('weather_events_cleaned.csv')
df_event['BEGIN_DATE_TIME'] = pd.to_datetime(df_event['BEGIN_DATE_TIME'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df_event['END_DATE_TIME'] = pd.to_datetime(df_event['END_DATE_TIME'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

df['Start'] = pd.to_datetime(df['Start'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce') #5/30: '%m/%d/%Y %H:%M'
df['Start'] = df['Start'].dt.strftime('%m/%d/%Y %I:%M:%S %p')
df['Weather_type'] = find_event_type(df['Start'], df_event)

df = df.drop('Direction', axis=1)

df.to_csv('Direction_data.csv', index=False)
