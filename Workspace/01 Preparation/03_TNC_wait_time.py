import pandas as pd

df_wd = pd.read_csv('TNC_wait_time_WD.csv')
df_we = pd.read_csv('TNC_wait_time_WE.csv')

df_wd['Date'] = pd.to_datetime(df_wd['pickup_date'], format='%m/%d/%Y', errors='coerce')
df_wd['pickup_datetime'] = pd.to_datetime(df_wd['pickup_datetime'], errors='coerce', infer_datetime_format=True)
df_wd['Hour'] = df_wd['pickup_datetime'].dt.hour
average_wait_by_hour_wd = df_wd.groupby(['Pickup_CA', 'Date', 'Hour'])['WT_min'].mean().reset_index()

df_we['Date'] = pd.to_datetime(df_we['pickup_date'], format='%m/%d/%Y', errors='coerce')
df_we['pickup_datetime'] = pd.to_datetime(df_we['pickup_datetime'], errors='coerce', infer_datetime_format=True)
df_we['Hour'] = df_we['pickup_datetime'].dt.hour
average_wait_by_hour_we = df_we.groupby(['Pickup_CA', 'Date', 'Hour'])['WT_min'].mean().reset_index()

df = pd.read_csv('grouped_tripdata.csv')

df['Date'] = pd.to_datetime(df['Date'])
df['DayOfWeek'] = df['Date'].dt.dayofweek # Monday=0, Sunday=6

weekdays_df = df[df['DayOfWeek'] < 4]
weekends_df = df[df['DayOfWeek'] >= 4]

df['Pickup_CA'] = df['Pickup_CA'].astype(float)
df['Hour'] = df['Hour'].astype(float)
print(df.dtypes)

### Waittime
average_wait_by_hour_wd['Date'] = pd.to_datetime(average_wait_by_hour_wd['Date'])
average_wait_by_hour_we['Date'] = pd.to_datetime(average_wait_by_hour_we['Date'])
print(average_wait_by_hour_we.dtypes)

### Merge
# Merge the weekday and weekend DataFrames with their respective df2
merged_weekdays = pd.merge(weekdays_df, average_wait_by_hour_wd[['Date', 'Hour', 'Pickup_CA', 'WT_min']], on=['Date', 'Hour', 'Pickup_CA'], how='left')
merged_weekends = pd.merge(weekends_df, average_wait_by_hour_we[['Date', 'Hour', 'Pickup_CA', 'WT_min']], on=['Date', 'Hour', 'Pickup_CA'], how='left')

# Concatenate the two merged DataFrames back into one
final_df = pd.concat([merged_weekdays, merged_weekends], ignore_index=True)

final_df = final_df.sort_values(by=['Date', 'Hour']).reset_index(drop=True)

final_df.to_csv('tripdata.csv', index=False)


