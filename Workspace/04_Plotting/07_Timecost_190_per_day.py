import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.nonparametric.kde import KDEUnivariate

from Tools.Cumulative_distribution import plot_cumulative_distribution, plot_cumulative_distribution_comparison, plot_cumulative_distribution_weather

transit_cost = pd.read_csv('dataframe_transit_cost.csv')

#####################################################################
df = transit_cost
print(df.columns)

columns_to_convert = ['TNC_miles', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare', 'WT_min', 'Transit_miles',
                      'Transit_duration', 'Transit_fare', 'Count',
                      'Bus_duration', 'Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap',
                      'Time_Value_Matching', 'Time_Value_Matching_Social_ice_190', 'Time_Value_Matching_Social_ev40_190',
                      'Time_Value_Matching_Social_ev60_190']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
print(df.dtypes)

df["WEATHER"] = 'None'
df.loc[df['Weather_type'].isin(['Winter Weather', 'Winter Storm', 'Extreme Cold/Wind Chill']), "WEATHER"] = 'Winter\nWeather'
df.loc[df['Weather_type'] == 'Excessive Heat', "WEATHER"] = 'Heat'

colors = [
    "#bcf60c",  # lime
    "#fabebe",  # pink
    "#ffe119",  # yellow
    "#46f0f0", # cyan
    "#3cb44b",  # bright green
    "#4363d8",  # bright blue
    "#e6194B",  # bright red
    "#f032e6", # magenta
    "#f58231", # orange
    "#ffe119",  # yellow
    "#911eb4"  # purple
]

#####################################################################
# Set data
df['Cost_no_social'] = df['Time_Value_Matching']
df['Cost_social'] = df['Time_Value_Matching_Social_ice_190']
df['Cost_social_ev'] = df['Time_Value_Matching_Social_ev40_190']

# Cumulative density
df['Weight'] = df['Count'] / df['Count'].sum()

#####################################################################
# Weight for box plot
def repeat_values(cost_series, count_series):
    return np.repeat(cost_series.values, count_series.values)

weighted_dates = repeat_values(df['Date'], df['Count'])
weighted_cost_no_social = repeat_values(df['Cost_no_social'], df['Count'])

#####################################################################
# Box plot
### All days together

df_weighted = pd.DataFrame({
    'Date': weighted_dates,
    'Cost_no_social': weighted_cost_no_social
})

unique_dates = df['Date'].unique()
print(unique_dates)

desired_order = [
    '2022-02-01', '2022-03-16', '2022-06-13', '2022-09-12',
    '5/30/2023', '2022-01-08', '2022-12-24', '2023-02-17'
]
df_weighted['Date'] = pd.Categorical(df_weighted['Date'], categories=desired_order, ordered=True)

plt.figure(figsize=(20, 15))
ax = df_weighted.boxplot(
    column='Cost_no_social', by='Date', grid=False, showfliers=False,
    boxprops=dict(color='black'), medianprops=dict(color='orange'),
    whiskerprops=dict(color='black'), capprops=dict(color='black', linewidth=0),
    showmeans=False, meanline=False)

ax.axhline(y=20, color='DeepSkyBlue', linestyle=':', linewidth=1.2) #label='DoT Standard, All purpose ($20/hr)')
ax.axhline(y=32, color='DeepSkyBlue', linestyle='--', linewidth=1.2) #label='DoT Standard, Business ($32/hr)')

plt.ylim(-30, 120)

plt.xlabel('Date', fontsize=14)
plt.ylabel('Implied value of time ($/hr)', fontsize=14)
plt.title('')
plt.suptitle('')
plt.xticks(rotation=45, fontsize=12)
plt.yticks(range(-20, 121, 20), fontsize=12)
plt.tight_layout()

labels = [item.get_text() for item in ax.get_xticklabels()]
ax.set_xticklabels(labels, rotation=45, fontsize=12)

plt.show()