import pandas as pd
import re
import json

def calculate_fare(df):
    fare_list = []

    for index, row in df.iterrows():

        transit_counts = {
            'BUS': 0,
            'SUBWAY': 0,
            'TRAIN': 0
        }

        directions_result = row['Direction']

        transit_counts['BUS'] = directions_result.count("'type': 'BUS'")
        transit_counts['SUBWAY'] = directions_result.count("'type': 'SUBWAY'")
        transit_counts['TRAIN'] = directions_result.count("'type': 'TRAIN'")

        total_fare = 0

        if transit_counts['BUS'] in [1, 2, 3]:
            total_fare += 2.25
        if transit_counts['BUS'] in [4, 5, 6]:
            total_fare += 4.5

        if transit_counts['SUBWAY'] in [1, 2, 3]:
            total_fare += 2.5
        if transit_counts['SUBWAY'] in [4, 5, 6]:
            total_fare += 5

        # Add cost for airport shuttle
        #if re.search(r"\bO'Hare\b", row['Note']):
            #total_fare += 2.5

        if transit_counts['TRAIN'] != 0:
            total_fare += 3.75

        fare_list.append(total_fare)

    df['Transit_fare'] = fare_list
    return df
