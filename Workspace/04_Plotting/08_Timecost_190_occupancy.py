import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from Tools.Cumulative_distribution import plot_cumulative_distribution, plot_cumulative_distribution_comparison, plot_cumulative_distribution_weather


transit_cost = pd.read_csv('dataframe_transit_cost.csv')
transit_cost_full = pd.read_csv('dataframe_transit_cost_full.csv')
transit_cost_empty = pd.read_csv('dataframe_transit_cost_empty.csv')

print("average:", transit_cost['Time_Value_Matching'].median(), transit_cost['Time_Value_Matching_Social_ice_190'].median(), transit_cost['Time_Value_Matching_Social_ev40_190'].median())
print("full:", transit_cost_full['Time_Value_Matching'].median(), transit_cost_full['Time_Value_Matching_Social_ice_190'].median(), transit_cost_full['Time_Value_Matching_Social_ev40_190'].median())
print("empty:", transit_cost_empty['Time_Value_Matching'].median(), transit_cost_empty['Time_Value_Matching_Social_ice_190'].median(), transit_cost_empty['Time_Value_Matching_Social_ev40_190'].median())


#####################################################################
transit_cost_full['MODE'] = 'Transit \n(Full seating \ncapacity)'
transit_cost['MODE'] = 'Transit \n(Average \ncapacity)'
transit_cost_empty['MODE'] = 'Transit \n(Half average \ncapacity)'
df = pd.concat([transit_cost_empty, transit_cost, transit_cost_full])
print(df.columns)

columns_to_convert = ['TNC_miles', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare', 'WT_min', 'Transit_miles',
                      'Transit_duration', 'Transit_fare', 'Count',
                      'Bus_duration', 'Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap',
                      'Time_Value_Matching', 'Time_Value_Matching_Social_ice_190', 'Time_Value_Matching_Social_ev40_190',
                      'Time_Value_Matching_Social_ev60_190']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
print(df.dtypes)

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

#####################################################################
# Weight for box plot
def repeat_values(cost_series, count_series):
    return np.repeat(cost_series.values, count_series.values)

weighted_cost_no_social = repeat_values(df['Cost_no_social'], df['Count'])
weighted_cost_social = repeat_values(df['Cost_social'], df['Count'])
weighted_cost_social_ev = repeat_values(df['Cost_social_ev'], df['Count'])
weighted_mode = repeat_values(df['MODE'], df['Count'])

#####################################################################
# Box plot
df_plot = pd.DataFrame({
    'MODE': np.concatenate([weighted_mode] * 3),
    'Cost_Type': (['Without social cost'] * len(weighted_cost_no_social) +
                  ['With social cost (vs gasoline TNC vehicles)'] * len(weighted_cost_social) +
                  ['With social cost (vs electric TNC vehicles)'] * len(weighted_cost_social_ev)),
    'Cost ($/hr)': np.concatenate([weighted_cost_no_social, weighted_cost_social, weighted_cost_social_ev])
})

cost_type_labels = {
    'Without social cost': 'Without social cost',
    'With social cost (vs gasoline TNC vehicles)': 'With social cost (vs gasoline TNC vehicles)',
    'With social cost (vs electric TNC vehicles)': 'With social cost (vs electric TNC vehicles)'
}
df_plot['Cost_Type'] = df_plot['Cost_Type'].map(cost_type_labels)

sns.set(style="ticks", palette=colors)
sns.set_context("paper", font_scale=1.1, rc={"lines.linewidth": 1.1})

flierprops = dict(marker='x', color='grey', linewidth=0.5, markersize=3)

g = sns.catplot(x="MODE", y="Cost ($/hr)", hue='MODE',
                col="Cost_Type", data=df_plot, kind="box", height=4, aspect=1.2,
                width=0.8, linewidth=1.1, notch=False, orient="v",
                palette=['white'], medianprops=dict(color='orange'), showfliers=False)

for ax in g.axes.flat:
    ax.axhline(y=20, color='DeepSkyBlue', linestyle=':', linewidth=1.2, label='DoT Standard, All purpose ($20/hr)')
    ax.axhline(y=32, color='DeepSkyBlue', linestyle='--', linewidth=1.2, label='DoT Standard, Business ($32/hr)')

plt.ylim(-30, 120)
g.set_axis_labels("", "Implied value of time ($/hr)")
for ax in g.axes.flat:
    ax.set_xlabel(ax.get_xlabel(), fontsize=16)
    ax.set_ylabel(ax.get_ylabel(), fontsize=16)
    ax.set_yticks(range(-20, 121, 20))
    ax.set_yticklabels(range(-20, 121, 20), fontsize=16)
    ax.tick_params(axis='x', labelsize=16)

g.set_titles(col_template="{col_name}", size=16)
sns.despine(trim=True)

plt.tight_layout()
plt.show()

