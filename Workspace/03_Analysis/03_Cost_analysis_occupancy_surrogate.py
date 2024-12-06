import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.optimize import root_scalar
from matplotlib.ticker import MaxNLocator

from Input.TNC import TNC
from Input.Transit import Transit
from Input.Cost import Cost
from Input.Fuel import Fuel
from Cost.Cost_calc_congestion import calc_cost_tnc, calc_cost_transit
from Tools.json_read import object_from_json
# Read csv
df = pd.read_csv('C:/Users/miki/Documents/CSV data/Tripdata/Direction_data/Direction_data_clean_allca.csv')

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

dfs = {
    'ICE Cost': ice_cost,
    'EV40 Cost': EV40_cost,
    'EV60 Cost': EV60_cost,
    'Transit Cost': transit_cost
}

for name, df in dfs.items():
    df['GHG_cost_190'] = df['GHG_cost'] * 190 / 58

################
## Numerically finding seat rate for specific cost
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

# --- Surrogate ------------------------------------------
seat_rates = []
GHG_median = []
GHG_10 = []
GHG_90 = []
AP_median = []
AP_10 = []
AP_90 = []
other_median = []
other_10 = []
other_90 = []
total_median = []
total_10 = []
total_90 = []

for i in range(1000):
    seat_rate = np.random.uniform(low=1, high=100, size=None)
    seat_rates.append(seat_rate)

    Bus.occupancy = 44 * seat_rate / 100
    Subway.occupancy = 42 * 7 * seat_rate / 100
    Train_electric.occupancy = 148 * 6 * seat_rate / 100
    Train_diesel.occupancy = 148 * 6 * seat_rate / 100

    transit_cost = calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost)
    transit_cost['GHG_cost_190'] = transit_cost['GHG_cost'] * 190 / 58

    GHG_median_i = weighted_results(transit_cost, 'GHG_cost_190', "Count", 0.5)
    GHG_10_i = weighted_results(transit_cost, 'GHG_cost_190', "Count", 0.1)
    GHG_90_i = weighted_results(transit_cost, 'GHG_cost_190', "Count", 0.9)
    GHG_median.append(GHG_median_i)
    GHG_10.append(GHG_10_i)
    GHG_90.append(GHG_90_i)

    AP_median_i = weighted_results(transit_cost, 'Air_pollutant_cost', "Count", 0.5)
    AP_10_i = weighted_results(transit_cost, 'Air_pollutant_cost', "Count", 0.1)
    AP_90_i = weighted_results(transit_cost, 'Air_pollutant_cost', "Count", 0.9)
    AP_median.append(AP_median_i)
    AP_10.append(AP_10_i)
    AP_90.append(AP_90_i)

### Sort
sorted_indices = np.argsort(seat_rates)
sorted_seat_rates = np.array(seat_rates)[sorted_indices]

sorted_GHG_median = np.array(GHG_median)[sorted_indices]
sorted_GHG_10 = np.array(GHG_10)[sorted_indices]
sorted_GHG_90 = np.array(GHG_90)[sorted_indices]

sorted_AP_median = np.array(AP_median)[sorted_indices]
sorted_AP_10 = np.array(AP_10)[sorted_indices]
sorted_AP_90 = np.array(AP_90)[sorted_indices]

### Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 10), sharex=True, sharey=True)

ax.plot(sorted_seat_rates, sorted_GHG_median, label='GHG cost', color='grey')
ax.fill_between(sorted_seat_rates, sorted_GHG_10, sorted_GHG_90, color='grey', alpha=0.1, edgecolor=None)
ax.set_title('GHG Cost ($190/t-CO2), \n$/trip', fontsize=30)
# ax.set_xlabel('Seat Rates (%)')
ax.set_ylabel('Externality, $/trip', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

plt.ylim(0, 0.8)
plt.xlim(0, 100)
plt.tight_layout()
plt.show()


### Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 10), sharex=True, sharey=True)

ax.plot(sorted_seat_rates, sorted_AP_median, label='Air pollutant cost', color='grey')
ax.fill_between(sorted_seat_rates, sorted_AP_10, sorted_AP_90, color='grey', alpha=0.1, edgecolor=None)
ax.set_title('Air Pollutant \nCost, $/trip', fontsize=30)
# ax.set_xlabel('Seat Rates (%)')
ax.set_ylabel('Externality, $/trip', fontsize=30)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=30)

plt.ylim(0, 0.8)
plt.xlim(0, 100)
plt.tight_layout()
plt.show()



##### GHG
def ghg_cost_from_seat_rate(seat_rate):
    Bus.occupancy = 44 * seat_rate / 100
    Subway.occupancy = 42 * 7 * seat_rate / 100
    Train_electric.occupancy = 148 * 6 * seat_rate / 100
    Train_diesel.occupancy = 148 * 6 * seat_rate / 100

    transit_cost = calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost)
    transit_cost['GHG_cost_190'] = transit_cost['GHG_cost'] * 190 / 58
    GHG_median = weighted_results(transit_cost, 'GHG_cost_190', "Count", 0.5)

    return GHG_median

# EV vs Transit seat
target = 0.2225

def cost_minus_target(seat_rate):
    return ghg_cost_from_seat_rate(seat_rate) - target
bracket = [1, 100]
sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a GHG_cost of TNC - EV median is approximately: {sol.root}")

# ICE vs Transit seat
target = 0.3909

sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a GHG_cost of TNC - ICE median is approximately: {sol.root}")

##### AP
def ap_cost_from_seat_rate(seat_rate):
    Bus.occupancy = 44 * seat_rate / 100
    Subway.occupancy = 42 * 7 * seat_rate / 100
    Train_electric.occupancy = 148 * 6 * seat_rate / 100
    Train_diesel.occupancy = 148 * 6 * seat_rate / 100

    transit_cost = calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost)
    AP_median = weighted_results(transit_cost, 'Air_pollutant_cost', "Count", 0.5)

    return AP_median

# EV vs Transit seat
target = 0.1070

def cost_minus_target(seat_rate):
    return ap_cost_from_seat_rate(seat_rate) - target
bracket = [1, 100]
sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a AP Externality of TNC - EV median is approximately: {sol.root}")

# ICE vs Transit seat
target = 0.1592

def cost_minus_target(seat_rate):
    return ap_cost_from_seat_rate(seat_rate) - target
sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a AP Externality of TNC - ICE median is approximately: {sol.root}")

##### Total
def total_cost_from_seat_rate(seat_rate):
    Bus.occupancy = 44 * seat_rate / 100
    Subway.occupancy = 42 * 7 * seat_rate / 100
    Train_electric.occupancy = 148 * 6 * seat_rate / 100
    Train_diesel.occupancy = 148 * 6 * seat_rate / 100

    transit_cost = calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost)
    AP_median = weighted_results(transit_cost, 'Externality', "Count", 0.5)

    return AP_median

# EV vs Transit seat
target = 0.9065

def cost_minus_target(seat_rate):
    return ap_cost_from_seat_rate(seat_rate) - target
bracket = [1, 100]
sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a Externality of TNC - EV median is approximately: {sol.root}")

# ICE vs Transit seat
target = 1.1145

def cost_minus_target(seat_rate):
    return ap_cost_from_seat_rate(seat_rate) - target
sol = root_scalar(cost_minus_target, bracket=bracket, method='bisect')
if sol.converged:
    print(f"The seat_rate that results in a Externality of TNC - ICE median is approximately: {sol.root}")
