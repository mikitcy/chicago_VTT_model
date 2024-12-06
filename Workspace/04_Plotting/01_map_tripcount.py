import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

shapefile_path = 'Boundaries - Community Areas (current).zip'  # Replace with your shapefile path
gdf = gpd.read_file(shapefile_path)
print(gdf.dtypes)
gdf['area_num_1'] = gdf['area_num_1'].astype(float)

transit_cost = pd.read_csv('dataframe_transit_cost.csv')
df = transit_cost[['Hour', 'Pickup_CA', 'Count']]
df = df.groupby(['Hour', 'Pickup_CA'])['Count'].sum().reset_index()

hour_ranges = [(6, 12), (12, 18), (18, 24)]

overall_min = 5000
overall_max = 8000

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)

for idx, (start_hour, end_hour) in enumerate(hour_ranges):

    filtered_df = df[(df['Hour'] >= start_hour) & (df['Hour'] < end_hour)]
    merged_gdf = gdf.merge(filtered_df, left_on='area_num_1', right_on='Pickup_CA')

    merged_gdf.plot(column='Count', ax=axes[idx], legend=False,
                    cmap='GnBu', edgecolor='black',
                    vmin=overall_min, vmax=overall_max)
    axes[idx].set_title(f"Hours {start_hour}-{end_hour}", fontsize=18)
    axes[idx].axis('off')

cbar_ax = fig.add_axes([0.95, 0.3, 0.01, 0.5])  # [left, bottom, width, height] in figure coordinate
sm = plt.cm.ScalarMappable(cmap='GnBu', norm=plt.Normalize(vmin=overall_min, vmax=overall_max))
fig.colorbar(sm, cax=cbar_ax, orientation='vertical', label='Count')

plt.tight_layout()
plt.show()


df = transit_cost[['Hour', 'Dropoff_CA', 'Count']]
df = df.groupby(['Hour', 'Dropoff_CA'])['Count'].sum().reset_index()

hour_ranges = [(6, 12), (12, 18), (18, 24)]

overall_min = 4000
overall_max = 8000

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)

for idx, (start_hour, end_hour) in enumerate(hour_ranges):

    filtered_df = df[(df['Hour'] >= start_hour) & (df['Hour'] < end_hour)]
    merged_gdf = gdf.merge(filtered_df, left_on='area_num_1', right_on='Dropoff_CA')

    merged_gdf.plot(column='Count', ax=axes[idx], legend=False,
                    cmap='GnBu', edgecolor='black',
                    vmin=overall_min, vmax=overall_max)
    axes[idx].set_title(f"Hours {start_hour}-{end_hour}", fontsize=18)
    axes[idx].axis('off')

cbar_ax = fig.add_axes([0.95, 0.3, 0.01, 0.5])  # [left, bottom, width, height] in figure coordinate
sm = plt.cm.ScalarMappable(cmap='GnBu', norm=plt.Normalize(vmin=overall_min, vmax=overall_max))
fig.colorbar(sm, cax=cbar_ax, orientation='vertical', label='Count')

plt.tight_layout()
plt.show()
