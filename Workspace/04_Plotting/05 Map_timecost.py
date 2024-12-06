import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

shapefile_path = 'Boundaries - Community Areas (current).zip'
gdf = gpd.read_file(shapefile_path)
print(gdf.dtypes)
gdf['area_num_1'] = gdf['area_num_1'].astype(float)

transit_cost = pd.read_csv('dataframe_transit_cost.csv')

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

df = transit_cost[['Hour', 'Pickup_CA', 'Count', 'Time_Value_Matching']]
df = df.groupby(['Hour', 'Pickup_CA']).apply(
    lambda x: weighted_results(x, 'Time_Value_Matching','Count', 0.5)).reset_index(
    name='Weighted_Median_Time_Value_Matching')

hour_ranges = [(6, 12), (12, 14),(14, 16),(16, 18), (18, 24)]

overall_min = 10
overall_max = 60

fig, axes = plt.subplots(1, 5, figsize=(25, 5), sharex=True, sharey=True)

for idx, (start_hour, end_hour) in enumerate(hour_ranges):

    filtered_df = df[(df['Hour'] >= start_hour) & (df['Hour'] < end_hour)]
    merged_gdf = gdf.merge(filtered_df, left_on='area_num_1', right_on='Pickup_CA')

    merged_gdf.plot(column='Weighted_Median_Time_Value_Matching', ax=axes[idx], legend=False,
                    cmap='GnBu', edgecolor='black',
                    vmin=overall_min, vmax=overall_max)
    axes[idx].set_title(f"Hours {start_hour}-{end_hour}")
    axes[idx].axis('off')

cbar_ax = fig.add_axes([0.95, 0.3, 0.01, 0.5])  # [left, bottom, width, height] in figure coordinate
sm = plt.cm.ScalarMappable(cmap='GnBu', norm=plt.Normalize(vmin=overall_min, vmax=overall_max))
fig.colorbar(sm, cax=cbar_ax, orientation='vertical', label='Median breakeven time value, $/hr')

plt.tight_layout()
plt.show()


df2 = transit_cost[['Hour', 'Dropoff_CA', 'Count', 'Time_Value_Matching']]
df = df2.groupby(['Hour', 'Dropoff_CA']).apply(
    lambda x: weighted_results(x, 'Time_Value_Matching','Count', 0.5)).reset_index(
    name='Weighted_Median_Time_Value_Matching')

fig, axes = plt.subplots(1, 5, figsize=(25, 5), sharex=True, sharey=True)

for idx, (start_hour, end_hour) in enumerate(hour_ranges):

    filtered_df = df[(df['Hour'] >= start_hour) & (df['Hour'] < end_hour)]
    merged_gdf = gdf.merge(filtered_df, left_on='area_num_1', right_on='Dropoff_CA')

    merged_gdf.plot(column='Weighted_Median_Time_Value_Matching', ax=axes[idx], legend=False,
                    cmap='GnBu', edgecolor='black',
                    vmin=overall_min, vmax=overall_max)
    axes[idx].set_title(f"Hours {start_hour}-{end_hour}")
    axes[idx].axis('off')

cbar_ax = fig.add_axes([0.95, 0.3, 0.01, 0.5])  # [left, bottom, width, height] in figure coordinate
sm = plt.cm.ScalarMappable(cmap='GnBu', norm=plt.Normalize(vmin=overall_min, vmax=overall_max))
fig.colorbar(sm, cax=cbar_ax, orientation='vertical', label='Median breakeven time value, $/hr')

plt.tight_layout()
plt.show()
