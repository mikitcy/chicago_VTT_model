import pandas as pd

from Trip_data_clean.Season import assign_season
from Trip_data_clean.Day_time import get_day_category
from Trip_data_clean.Transit_type import get_transit_types
from Trip_data_clean.Fare import calculate_fare

# Read csv
df = pd.read_csv('Direction_data.csv')
print(df.dtypes)

##############################################
# Convert data type
df['TNC_miles'] = pd.to_numeric(df['TNC_miles'], errors='coerce')
df['TNC_duration'] = pd.to_numeric(df['TNC_duration'], errors='coerce')
df['TNC_fare'] = pd.to_numeric(df['TNC_fare'], errors='coerce')
df['TNC_total_fare'] = pd.to_numeric(df['TNC_total_fare'], errors='coerce')
df['Time_gap'] = pd.to_numeric(df['Time_gap'], errors='coerce')
print(df.dtypes)

##############################################
# Season assignment
df['Start'] = pd.to_datetime(df['Start'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['Month'] = df['Start'].dt.month
df['Season'] = df['Month'].apply(assign_season)

##############################################
# Day of week category assignment
#['Day_of_week'] = df['Date'].dt.day_name()
df['Weekday_weekend'] = df['DayOfWeek'].apply(get_day_category)

##############################################
# Add wait time
df['TNC_wait_time'] = df['WT_min']
df['TNC_duration_total'] = df['TNC_duration'] + df['TNC_wait_time']

##############################################
# Count the transit type and define detailed transit type
df['Transit_type_all'] = df.apply(get_transit_types, axis=1)

##############################################
# Fare calculation
df = calculate_fare(df)
df = df[df['TNC_total_fare'] != 0]

##############################################
# Drop direction
df = df.drop('Direction', axis=1)

df['Time_gap'].fillna(0, inplace=True)
df = df[df['Time_gap'] <= 1000]

##############################################
# Community Area
df_ca = pd.read_csv('chicago_community_areas.csv')

df = pd.merge(df, df_ca, left_on='Pickup_CA', right_on='Number', how='left')
df = df.rename(columns={'Area': 'Pickup_Area'})
df = df.rename(columns={'Community': 'Pickup_Community'})
df.drop(columns='Number', inplace=True)

df = pd.merge(df, df_ca, left_on='Dropoff_CA', right_on='Number', how='left')
df = df.rename(columns={'Area': 'Dropoff_Area'})
df = df.rename(columns={'Community': 'Dropoff_Community'})
df.drop(columns='Number', inplace=True)

##############################################
# NOAA weather data (hourly temperature, precipitation)
df_noaa = pd.read_csv('Chicago_temperature_precipitation.csv')
df_noaa = df_noaa[['Year', 'Month', 'Day', 'Hour', 'temperature', 'precipitation', 'snow_depth']]

df_noaa['temperature'] = pd.to_numeric(df_noaa['temperature'], errors='coerce')
df_noaa['precipitation'] = pd.to_numeric(df_noaa['precipitation'], errors='coerce')
df_noaa['snow_depth'] = pd.to_numeric(df_noaa['snow_depth'], errors='coerce')

df_noaa_grouped = df_noaa.groupby(['Year', 'Month', 'Day', 'Hour']).agg({
    'temperature': 'mean',
    'precipitation': 'max',
    'snow_depth': 'max'
}).reset_index()

df['Year'] = df['Start'].dt.year
df['Day'] = df['Start'].dt.day
df = pd.merge(df, df_noaa_grouped, how='left', on=['Year', 'Month', 'Day', 'Hour'])
df['temperature'] = (df['temperature'] * 9/5) + 32

##############################################
# Save to csv
df.to_csv('Direction_data_clean.csv', index=False)

print(df.dtypes)
print("Completed")