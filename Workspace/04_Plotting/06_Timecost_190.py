import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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

#####################################################################
# Box plot
df_plot = pd.DataFrame({
    'Cost_Type': ['Without \nsocial cost'] * len(weighted_cost_no_social) +
                 ['With social \ncost (vs ICE)'] * len(weighted_cost_social) +
                 ['With social \ncost (vs EV)'] * len(weighted_cost_social_ev),
    'Cost ($/hr)': np.concatenate([weighted_cost_no_social, weighted_cost_social, weighted_cost_social_ev])
})

sns.set(style="ticks")
sns.set_context("paper", font_scale=1.1, rc={"lines.linewidth": 1.1, "axes.labelsize": 30, "axes.titlesize": 30, "xtick.labelsize": 30, "ytick.labelsize": 30, "legend.fontsize": 30})

plt.figure(figsize=(10, 12))
ax = sns.boxplot(x="Cost_Type", y="Cost ($/hr)", data=df_plot, showfliers=False,
                 boxprops=dict(facecolor='white'), medianprops=dict(color='orange'),
                 whiskerprops=dict(color='black'), capprops=dict(color='black',linewidth = 0),
                 showmeans = True, meanline = True)

ax.axhline(y=20, color='DeepSkyBlue', linestyle=':', linewidth=1.2) #label='DoT Standard, All purpose ($20/hr)')
ax.axhline(y=32, color='DeepSkyBlue', linestyle='--', linewidth=1.2) #label='DoT Standard, Business ($32/hr)')

plt.ylim(-50, 120)
plt.legend()
sns.despine(trim=True)
plt.tight_layout()
plt.show()

#####################################################################
#####################################################################

df['Time_group'] = (df['Transit_duration'] // 30) * 30
df['Time_group'] = df['Time_group'].astype(int)
df = df[df['Time_group'] < 180]
#df['Cost_group'] = (df['Cost_no_social'] // 5) * 5

weighted_cost_no_social = repeat_values(df['Cost_no_social'], df['Count'])
weighted_cost_social = repeat_values(df['Cost_social'], df['Count'])
weighted_cost_social_ev = repeat_values(df['Cost_social_ev'], df['Count'])
weighted_time_group = repeat_values(df['Time_group'], df['Count'])

all_costs = np.concatenate([weighted_cost_no_social, weighted_cost_social, weighted_cost_social_ev])
all_time_groups = np.concatenate([weighted_time_group] * 3)
all_cost_types = (['Without social cost'] * len(weighted_cost_no_social) +
                  ['With social cost (vs gasoline TNC vehicles)'] * len(weighted_cost_social) +
                  ['With social cost (vs electric TNC vehicles)'] * len(weighted_cost_social_ev))

df_plot = pd.DataFrame({
    'Time_group': all_time_groups,
    'Cost_Type': all_cost_types,
    'Cost ($/hr)': all_costs
})

sns.set(style="ticks", palette=colors)
sns.set_context("paper", font_scale=1.1, rc={"lines.linewidth": 1.1})

flierprops = dict(marker='x', color='grey', linewidth=0.5, markersize=3)

g = sns.catplot(x="Time_group", y="Cost ($/hr)", hue='Cost_Type',
                col="Cost_Type", data=df_plot, kind="box", height=5, aspect=0.8,
                width=0.8, linewidth=1.1, notch=False, orient="v",
                palette=['white'], medianprops=dict(color='orange'), showfliers=False)

for ax in g.axes.flat:
    ax.axhline(y=20, color='DeepSkyBlue', linestyle=':', linewidth=1.2, label='DoT Standard, All purpose ($20/hr)')
    ax.axhline(y=32, color='DeepSkyBlue', linestyle='--', linewidth=1.2, label='DoT Standard, Business ($32/hr)')

g.set_axis_labels("Travel duration (minutes)", "Implied value of time ($/hr)")
for ax in g.axes.flat:
    ax.set_xlabel(ax.get_xlabel(), fontsize=18)
    ax.set_ylabel(ax.get_ylabel(), fontsize=18)
    ax.set_yticks(range(-50, 201, 50))
    ax.set_yticklabels(range(-50, 201, 50), fontsize=18)
    ax.tick_params(axis='x', labelsize=18)

g.set_titles(col_template="{col_name}", fontsize=18)
g._legend.set_bbox_to_anchor((1.25, 0.5))

sns.despine(trim=True)
plt.tight_layout()

plt.show()

