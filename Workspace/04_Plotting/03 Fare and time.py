import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

ice_cost = pd.read_csv('dataframe_ice_cost.csv')
transit_cost = pd.read_csv('dataframe_transit_cost.csv')

colors = [
    "#f58231", # orange
    "#bcf60c", # lime
    "#46f0f0", # cyan
    "#f032e6", # magenta
    "#e6194B",  # bright red
    "#3cb44b",  # bright green
    "#ffe119",  # yellow
    "#4363d8",  # bright blue
    "#fabebe",  # pink
    "#911eb4"  # purple
]
#####################################################################
ice_cost['MODE'] = 'TNC'
transit_cost['MODE'] = 'Transit'
df = pd.concat([ice_cost, transit_cost])
print(df.columns)

#####################################################################
# Weight for box plot
def repeat_values(cost_series, count_series):
    return np.repeat(cost_series.values, count_series.values)

weighted_fare = repeat_values(df['Fare'], df['Count'])
weighted_mode = repeat_values(df['MODE'], df['Count'])

#####################################################################
df_weighted = pd.DataFrame({
    'MODE': weighted_mode,
    'Fare': weighted_fare
})

df_plot = pd.melt(df_weighted, id_vars=['MODE'], value_vars=['Fare'],
                  var_name='Cost_Type', value_name='Cost')

cost_type_labels = {'Fare': ''}
df_plot['Cost_Type'] = df_plot['Cost_Type'].map(cost_type_labels)

sns.set_context("notebook", rc={"font.size":30,"axes.titlesize":30})
sns.set(style="whitegrid")

plt.figure(figsize=(5,10))
ax = sns.boxplot(y='Cost', x='Cost_Type', hue='MODE', data=df_plot,
            palette=colors, dodge=True, showfliers=False, width=0.6, linewidth=1.1,
            boxprops=dict(facecolor='white'),
            medianprops=dict(color='orange'), whiskerprops=dict(color='black'),
            capprops=dict(color='black',linewidth = 0),
            showmeans = True, meanline = True)
plt.ylim(0, 50)

plt.ylabel('Fare, $/trip', fontsize=30)
plt.xlabel('', fontsize=30)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=30)
ax.tick_params(axis='both', labelsize=30)
ax.legend_.remove()
plt.tight_layout()
plt.show()

#####################################################################
weighted_time = repeat_values(df['Time'], df['Count'])
weighted_mode = repeat_values(df['MODE'], df['Count'])

df_weighted = pd.DataFrame({
    'MODE': weighted_mode,
    'Time': weighted_time
})

df_plot = pd.melt(df_weighted, id_vars=['MODE'], value_vars=['Time'],
                  var_name='Cost_Type', value_name='Cost')

df_plot = pd.melt(df,
                  id_vars=['MODE'],
                  value_vars=['Time'],
                  var_name='Cost_Type',
                  value_name='Cost')

cost_type_labels = {'Time': ''}
df_plot['Cost_Type'] = df_plot['Cost_Type'].map(cost_type_labels)

sns.set_context("notebook", rc={"font.size":30,"axes.titlesize":30})
sns.set(style="whitegrid")

plt.figure(figsize=(5,10))
ax = sns.boxplot(y='Cost', x='Cost_Type', hue='MODE', data=df_plot,
            palette=colors, dodge=True, showfliers=False, width=0.6, linewidth=1.1,
            boxprops=dict(facecolor='white'),
            medianprops=dict(color='orange'), whiskerprops=dict(color='black'),
            capprops=dict(color='black',linewidth = 0),
            showmeans = True, meanline = True)
plt.ylim(0, 120)

plt.ylabel('Time, minutes', fontsize=30)
plt.xlabel('', fontsize=30)
ax.set_xticklabels(ax.get_xticklabels(), fontsize=30)
ax.tick_params(axis='both', labelsize=30)
ax.legend_.remove()
plt.tight_layout()
plt.show()