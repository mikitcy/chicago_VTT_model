import googlemaps
import random
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta, MO
import pytz

gmaps = googlemaps.Client(key='Enter your key')
now = datetime.now()

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

def get_transit_google(row):

    directions_result = gmaps.directions(row['Random_origin'], row['Random_destination'], mode="transit", departure_time=row['Random_time'])

    return directions_result
