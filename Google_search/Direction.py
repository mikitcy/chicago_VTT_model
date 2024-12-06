import pandas as pd
import json
from datetime import datetime

def hours_to_minutes(duration_str):
    total_minutes = 0
    time_components = duration_str.split(' ')

    for index, component in enumerate(time_components):
        if 'day' in component:
            total_minutes += int(time_components[index - 1]) * 60 * 24
        elif 'hour' in component:
            total_minutes += int(time_components[index - 1]) * 60
        elif 'min' in component:
            total_minutes += int(time_components[index - 1])

    return total_minutes

def str_to_miles(distance_str):

    total_miles = 0
    distance_components = distance_str.split(' ')

    for index, component in enumerate(distance_components):
        if 'km' in component:
            total_miles += float(distance_components[index - 1]) * 0.621371
        elif 'ft' in component:
            total_miles += float(distance_components[index - 1]) * 0.000189394
        elif 'mi' in component:
            total_miles += float(distance_components[index - 1])

    return total_miles
