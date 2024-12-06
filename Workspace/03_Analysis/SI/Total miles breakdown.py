import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Read csv
df = pd.read_csv('C:/Users/miki/Documents/CSV data/Tripdata/Cost/dataframe_transit_cost_allca.csv')

# Convert data type
columns_to_convert = ['TNC_miles', 'TNC_duration', 'TNC_wait_time', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare',
                      'Transit_miles', 'Transit_duration', 'Transit_fare', 'Bus_duration', 'Subway_duration',
                      'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap', 'Bus_miles',
                      'Subway_miles', 'Train_miles', 'Walk_miles', 'Count']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')

print(df.columns)

# Total mile plot per day (total:8days)
total_transit_miles = (df['Count'] * df['Transit_miles']).sum() / 8
total_bus_miles = (df['Count'] * df['Bus_miles']).sum() / 8
total_subway_miles = (df['Count'] * df['Subway_miles']).sum() / 8
total_train_miles = (df['Count'] * df['Train_miles']).sum() / 8 #"electric_ratio": 0.45
total_train_diesel_miles = total_train_miles * 0.55
total_train_electric_miles = total_train_miles * 0.45
total_walk_miles = (df['Count'] * df['Walk_miles']).sum() / 8

sums = [total_bus_miles, total_subway_miles, total_train_diesel_miles, total_train_electric_miles, total_walk_miles]
labels = ['Bus', 'Subway', 'Train - diesel', 'Train - electric', 'Walk']

def yaxis_formatter(x, pos):
    return f'{x / 1000:.0f}'

plt.figure(figsize=(7,4))
plt.bar(labels, sums)
plt.xlabel('')
plt.ylabel('Miles per transit mode \n(k-miles per day)')

plt.gca().yaxis.set_major_formatter(FuncFormatter(yaxis_formatter))

plt.tight_layout()
plt.show()

# per mile emissions plot
bus_emissions = df['Bus_GHG_emissions_per_mile'].mean()
subway_emissions = df['Subway_GHG_emissions_per_mile'].mean()
train_diesel_emissions = df['Train_diesel_GHG_emissions_per_mile'].mean()
train_electric_emissions = df['Train_electric_GHG_emissions_per_mile'].mean()

emissions = [bus_emissions, subway_emissions, train_diesel_emissions, train_electric_emissions, 0]
plt.figure(figsize=(7,4))
plt.bar(labels, emissions)
plt.xlabel('')
plt.ylabel('GHG emissions per mile per transit mode')

plt.tight_layout()
plt.show()

# Total emissions plot
total_bus_emissions = total_bus_miles * bus_emissions
total_subway_emissions = total_subway_miles * subway_emissions
total_train_diesel_emissions = total_train_diesel_miles * train_diesel_emissions
total_train_electric_emissions = total_train_electric_miles * train_electric_emissions

emissions = [total_bus_emissions, total_subway_emissions, total_train_diesel_emissions, total_train_electric_emissions, 0]
plt.figure(figsize=(7,4))
plt.bar(labels, emissions)
plt.xlabel('')
plt.ylabel('Total GHG emissions per transit mode \n(kt-CO2e per day)')

plt.gca().yaxis.set_major_formatter(FuncFormatter(yaxis_formatter))

plt.tight_layout()
plt.show()