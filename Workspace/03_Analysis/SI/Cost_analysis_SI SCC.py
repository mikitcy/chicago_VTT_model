import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from Input.TNC import TNC
from Input.Transit import Transit
from Input.Cost import Cost
from Input.Fuel import Fuel
from Cost.Cost_calc_congestion import calc_cost_tnc, calc_cost_transit
from Tools.json_read import object_from_json
# Read csv
df = pd.read_csv('Direction_data_clean.csv')

# Convert data type
columns_to_convert = ['TNC_miles', 'TNC_duration', 'TNC_wait_time', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare',
                      'Transit_miles', 'Transit_duration', 'Transit_fare', 'Bus_duration', 'Subway_duration',
                      'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap', 'Bus_miles',
                      'Subway_miles', 'Train_miles', 'Walk_miles']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
print(df.dtypes)

df['Transit_duration'] = df['Transit_duration'] + df['Time_gap']
df['Other_duration'] = df['Other_duration'] + df['Time_gap']

# Read JSON files
Gasoline = object_from_json('Input/JSON/Gasoline.json', Fuel)
Electricity = object_from_json('Input/JSON/Electricity.json', Fuel)
Electricity_Average = object_from_json('Input/JSON/Electricity_Average.json', Fuel)
Diesel = object_from_json('Input/JSON/Diesel.json', Fuel)
ICE = object_from_json('Input/JSON/ICE.json', TNC)
EV40 = object_from_json('Input/JSON/EV.json', TNC, level='base')
EV60 = object_from_json('Input/JSON/EV.json', TNC, level='large')
Cost = object_from_json('Input/JSON/Cost.json', Cost, level='base')
Bus = object_from_json('Input/JSON/Bus.json', Transit)
Subway = object_from_json('Input/JSON/Subway.json', Transit)
Train_diesel = object_from_json('Input/JSON/Train.json', Transit, level='diesel')
Train_electric = object_from_json('Input/JSON/Train.json', Transit, level='electric')

# Calculate cost and save to new csv file
ice_cost = calc_cost_tnc(df, ICE, Gasoline, Cost)
EV40_cost = calc_cost_tnc(df, EV40, Electricity, Cost)
EV60_cost = calc_cost_tnc(df, EV60, Electricity, Cost)
transit_cost = calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost)

#####################################################################
## Consolidate column names between modes
# Set Fare column
for df in [ice_cost, EV40_cost, EV60_cost]:
    df['Fare'] = df['TNC_total_fare'].fillna(0)
transit_cost['Fare'] = transit_cost['Transit_fare'].fillna(0)

# Set time
for df in [ice_cost, EV40_cost, EV60_cost]:
    df['Time'] = df['TNC_duration_total']
transit_cost['Time'] = transit_cost['Transit_duration']

# Set total private cost with internalized social cost
for df in [ice_cost, EV40_cost, EV60_cost, transit_cost]:
    df['Trip_fare_with_time_cost'] = df['Trip_fare_with_time_cost'].fillna(0)
    df['Total_private_cost_internalized_externality'] = df['Trip_fare_with_time_cost'] + df['Externality']

#####################################################################
# Comparison between Uber / transit
attributes = ['GHG_cost', 'Air_pollutant_cost', 'Other_externality', 'Externality', 'Fare', 'Time', 'Time_cost',
              'Trip_fare_with_time_cost', 'Total_private_cost_internalized_externality']
for attribute in attributes:
    comparison_column_name = f'Comparison_{attribute}'
    transit_cost[comparison_column_name] = transit_cost[attribute] / ice_cost[attribute]

#####################################################################
# Time value cost to match trade-offs ($ per hour)
transit_cost['Time_Value_Matching'] = (
        ((transit_cost['TNC_total_fare'] - transit_cost['Transit_fare'])
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

transit_cost['Time_Value_Matching_Social_ice_58'] = (
        ((transit_cost['TNC_total_fare'] + ice_cost['Externality'] - transit_cost['Transit_fare'] - transit_cost['Externality'])
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

transit_cost['Time_Value_Matching_Social_ev40_58'] = (
        ((transit_cost['TNC_total_fare'] + EV40_cost['Externality'] - transit_cost['Transit_fare'] - transit_cost['Externality'])
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

transit_cost['Time_Value_Matching_Social_ev60_58'] = (
        ((transit_cost['TNC_total_fare'] + EV60_cost['Externality'] - transit_cost['Transit_fare'] - transit_cost['Externality'])
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

#=======================
transit_cost['Time_Value_Matching_Social_ice_190'] = (
        ((transit_cost['TNC_total_fare'] + ice_cost['Externality'] + ice_cost['GHG_cost'] * (190/58 - 1)
          - transit_cost['Transit_fare'] - transit_cost['Externality'] - transit_cost['GHG_cost'] * (190/58 - 1))
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

transit_cost['Time_Value_Matching_Social_ev40_190'] = (
        ((transit_cost['TNC_total_fare'] + ice_cost['Externality'] + EV40_cost['GHG_cost'] * (190/58 - 1)
          - transit_cost['Transit_fare'] - transit_cost['Externality'] - transit_cost['GHG_cost'] * (190/58 - 1))
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

transit_cost['Time_Value_Matching_Social_ev60_190'] = (
        ((transit_cost['TNC_total_fare'] + ice_cost['Externality'] + EV60_cost['GHG_cost'] * (190/58 - 1)
          - transit_cost['Transit_fare'] - transit_cost['Externality'] - transit_cost['GHG_cost'] * (190/58 - 1))
         / (transit_cost['Transit_duration'] - transit_cost['TNC_duration_total'])) * 60)

#####################################################################
#####################################################################
dfs = {
    'ICE Cost': ice_cost,
    'EV40 Cost': EV40_cost,
    'EV60 Cost': EV60_cost,
    'Transit Cost': transit_cost
}

def weighted_results(df, attr, weight, percentile):
    attr = np.array(df[attr])
    wt = np.array(df[weight])

    sorted_df = np.argsort(attr)
    attr_sorted = attr[sorted_df]
    wt_sorted = wt[sorted_df]

    cumulative_weight = np.cumsum(wt_sorted)
    cutoff = percentile * cumulative_weight[-1]

    weighted_value = attr_sorted[np.searchsorted(cumulative_weight, cutoff)]

    return weighted_value

############
## Social cost results table
for name, df in dfs.items():
    df['GHG_cost_190'] = df['GHG_cost'] #* 190 / 58
    df['Total'] = df['GHG_cost_190'] + df['Air_pollutant_cost'] + df['Other_externality']

attributes = ['GHG_cost_190', 'Air_pollutant_cost', 'Other_externality', 'Total']

results = {attr: [] for attr in attributes}

for df_name, df in dfs.items():
    for attr in attributes:
        # Calculate the 10th percentile, 90th percentile, and median
        p25 = weighted_results(df, attr, ["Count"], 0.25)
        p75 = weighted_results(df, attr, ["Count"], 0.75)
        median = weighted_results(df, attr, ["Count"], 0.50)

        # Convert values to strings
        p25_str = f'{p25:.2f}'
        p75_str = f'{p75:.2f}'
        median_str = f'{median:.4f}'

        # Format in '10th - 90th (Median)'
        formatted_value = f'{p25_str} - {p75_str} ({median_str})'
        results[attr].append(formatted_value)

result_df = pd.DataFrame(results, index=dfs.keys()).T
print(result_df)

fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=result_df.values,
                 colLabels=result_df.columns,
                 rowLabels=result_df.index,
                 cellLoc='center',
                 loc='center')
plt.tight_layout()
plt.show()

#####################################################################
############
## Breakeven time cost results table
dfs = {
    'Transit Cost': transit_cost
}

attributes = ['Time_Value_Matching', 'Time_Value_Matching_Social_ice_58', 'Time_Value_Matching_Social_ev40_58', 'Time_Value_Matching_Social_ev60_58']

results = {attr: [] for attr in attributes}

for df_name, df in dfs.items():
    for attr in attributes:
        # Calculate the 10th percentile, 90th percentile, and median
        p25 = weighted_results(df, attr, ["Count"], 0.25)
        p75 = weighted_results(df, attr, ["Count"], 0.75)
        median = weighted_results(df, attr, ["Count"], 0.50)

        # Convert values to strings
        p25_str = f'{p25:.2f}'
        p75_str = f'{p75:.2f}'
        median_str = f'{median:.4f}'

        # Format in '10th - 90th (Median)'
        formatted_value = f'{p25_str} - {p75_str} ({median_str})'
        results[attr].append(formatted_value)

result_df = pd.DataFrame(results, index=dfs.keys()).T
print(result_df)

fig, ax = plt.subplots(figsize=(6, 4))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=result_df.values,
                 colLabels=result_df.columns,
                 rowLabels=result_df.index,
                 cellLoc='center',
                 loc='center')
plt.tight_layout()
plt.show()
