import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

transit_cost = pd.read_csv('dataframe_transit_cost.csv')
df = transit_cost[['Transit_type_all', 'TNC_duration_total', 'TNC_duration', 'TNC_wait_time', 'Transit_duration',
                    'Bus_duration', 'Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration','Count',
                   'Weather_type', 'DayOfWeek', 'Pickup_Area']]

######################################
df.loc[df['Transit_type_all'] == 'Bus & Subway & Train', 'Transit_type_all'] = 'Bus & Subway\n  & Train'


def weighted_median(df, value_column, weight_column):
    df_sorted = df.sort_values(value_column)
    cumsum = df_sorted[weight_column].cumsum()
    cutoff = df_sorted[weight_column].sum() / 2.0
    return df_sorted[cumsum >= cutoff][value_column].iloc[0]

result_transit = df.groupby('Transit_type_all').apply(lambda x: weighted_median(x, 'Bus_duration', 'Count'))
result_transit = result_transit.rename('Bus_duration')

for col in ['Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration']:
    result_transit = pd.concat([result_transit, df.groupby('Transit_type_all').apply(lambda x: weighted_median(x, col, 'Count')).rename(col)], axis=1)

####################
def weighted_median_tnc(data, weights):
    sorted_data = data.sort_values()
    cum_weights = weights.loc[sorted_data.index].cumsum()
    cutoff = weights.sum() / 2
    return sorted_data[cum_weights >= cutoff].iloc[0]

medians = {col: weighted_median_tnc(df[col], df['Count']) for col in ['TNC_duration', 'TNC_wait_time']}
plot_data = pd.DataFrame(medians, index=['TNC'])

combined_data = pd.concat([result_transit, plot_data])

combined_data['Vehicle time'] = combined_data[['Bus_duration', 'Subway_duration', 'Train_duration', 'TNC_duration']].sum(axis=1)
combined_data['Wait time'] = combined_data[['Other_duration', 'TNC_wait_time']].sum(axis=1)
combined_data['Walk time'] = combined_data['Walk_duration']

plot_data_combined = combined_data[['Vehicle time', 'Wait time', 'Walk time']]
plot_data_combined['Total time'] = plot_data_combined.sum(axis=1)
plot_data_combined = plot_data_combined.sort_values('Total time', ascending=False)
plot_data_combined = plot_data_combined.drop(columns='Total time')

colors = ['#6489FA', '#FA7864', '#FFDE5C']
plot_data_combined.plot(kind='barh', stacked=True, color=colors)

plt.yticks(rotation=0, ha='right')
plt.xlabel('Median Time (minutes)')
plt.tight_layout()
plt.subplots_adjust(right=0.7, bottom=0.3)
plt.show()

#####################################################################
# Filter weekend/weekdays here:
#df = df[df['DayOfWeek'] <3]
#####################################################################

# Weight for box plot
def repeat_values(cost_series, count_series):
    return np.repeat(cost_series.values, count_series.values)

weighted_waittime = repeat_values(df['TNC_wait_time'], df['Count'])

df["AREA"] = 'Suburban \narea'
df.loc[df['Pickup_Area'].isin(['West Side', 'North Side']), "AREA"] = 'West & \nNorth \nChicago'
df.loc[df['Pickup_Area'].isin(['Central']), "AREA"] = 'Central \nChicago \n(downtown)'
weighted_area = repeat_values(df['AREA'], df['Count'])

#####################################################################
# Box plot
df_plot = pd.DataFrame({
    'AREA': np.concatenate([weighted_area]),
    'Wait time': (['TNC_wait_time'] * len(weighted_waittime)),
    'TNC wait time (minutes)': np.concatenate([weighted_waittime])
})

cost_type_labels = {
    'TNC_wait_time': 'TNC wait time'
}

df_plot['Wait time'] = df_plot['Wait time'].map(cost_type_labels)

sns.set(style="whitegrid")

g = sns.catplot(x='AREA', y='TNC wait time (minutes)', hue='AREA',
                data=df_plot, kind="box", height=4, aspect=0.8,
                width=0.6, linewidth=1.1, notch=False, orient="v",
                boxprops=dict(facecolor='white'),
                medianprops=dict(color='orange'), whiskerprops=dict(color='black'),
                capprops=dict(color='black',linewidth = 0), showfliers=False,
                showmeans = True, meanline = True)
plt.ylim(0, 18)
plt.tight_layout()
plt.show()
