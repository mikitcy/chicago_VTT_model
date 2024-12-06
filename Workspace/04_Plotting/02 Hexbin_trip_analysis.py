import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as ticker
from brokenaxes import brokenaxes
from matplotlib.ticker import PercentFormatter

# Read csv
df = pd.read_csv('Direction_data_clean.csv')

# Convert data type
columns_to_convert = ['TNC_miles', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare', 'WT_min', 'Transit_miles',
                      'Transit_duration', 'Transit_fare',
                      'Bus_duration', 'Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
print(df.dtypes)

df['Transit_duration'] = df['Transit_duration'] + df['Time_gap']
df['TNC_duration_total'] = df['TNC_duration_total'] + df['WT_min']

######################################
# Compare TNC vs transit in duration and distance
df['Duration_gap'] = df['Transit_duration'] - df['TNC_duration_total']
df['Duration_gap_p'] = df['Transit_duration'] / df['TNC_duration_total'] - 1
duration_gap = df['Duration_gap'].mean()
duration_gap_p = df['Duration_gap_p'].mean()
print("Duration Gap in minutes: ", duration_gap, "Duration Gap %: ", duration_gap_p)

df['Mile_gap'] = df['Transit_miles'] - df['TNC_miles']
df['Mile_gap_p'] = df['Transit_miles'] / df['TNC_miles'] - 1
mile_gap = df['Mile_gap'].mean()
mile_gap_p = df['Mile_gap_p'].mean()
print("Mile Gap in minutes: ", mile_gap, "Mile Gap %: ", mile_gap_p)

######################################
def format_tick(x, pos):
    return '{:,}'.format(int(x))

######################################
# Analyze transit type
sum_counts = df.groupby('Transit_type_all')['Count'].sum().reset_index()
sum_counts = sum_counts.sort_values(by='Transit_type_all')
sum_counts = sum_counts.sort_values(by='Count', ascending=False)
new_row = pd.DataFrame({'Transit_type_all': ['No direction available'], 'Count': [1807]})
sum_counts = pd.concat([sum_counts, new_row], ignore_index=True)
transit_colors = {transit_type: color for transit_type, color in zip(sum_counts['Transit_type_all'], colors)}

######################################
# hexbin plot (Duration)
# Transit type
transit_types = df['Transit_type_all'].unique()
df = df.sort_values(by='Transit_type_all')
num_types = len(df['Transit_type_all'].unique())

# Selected Transit type
selected_transit_types = ["Bus", "Bus & Subway", "Subway", "Walk"]
# Filter the DataFrame to only include the selected transit types
df = df[df['Transit_type_all'].isin(selected_transit_types)]

fig, axes = plt.subplots(1, 4, figsize=(35, 12), constrained_layout=True, sharex=True, sharey=True)
axes = axes.flatten()
hexcolor = "viridis_r"

def plot_hexbin(subset, x_variable, y_variable, weights, ax, xlims, ylims):
    ax.hexbin(x=subset[x_variable], y=subset[y_variable],
              C=subset[weights], reduce_C_function=np.sum, bins="log", cmap=hexcolor, gridsize=30)
    bound = max(xlims + ylims)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.plot([min(xlims), bound], [min(ylims), bound], 'k-', alpha=1, zorder=3)

hexbin_plots = []

# Duration
for i, transit_type in enumerate(df['Transit_type_all'].unique()):
    subset_df = df[df['Transit_type_all'] == transit_type]
    hb = plot_hexbin(subset_df, 'TNC_duration_total', 'Transit_duration', 'Count',
                axes[i], (0, 500), (0, 500))
    hexbin_plots.append(hb)
    axes[i].set_title(transit_type)
    if i == 0 or i == 0:  # Add y-label to the first subplot of the row
        axes[i].set_ylabel('Transit Duration (minutes)')
    if i >= 0:  # Add x-label to the second row
        axes[i].set_xlabel('TNC Duration (minutes)')

# Set common x-axis labels
#fig.subplots_adjust(bottom=0.15)
#fig.text(0.5, 0.1, 'TNC Duration (minutes)', ha='center', va='center', fontsize=40)

for ax in axes:
    ax.title.set_fontsize(40)
    ax.xaxis.label.set_fontsize(40)
    ax.yaxis.label.set_fontsize(40)
    ax.tick_params(axis='both', labelsize=40)

cbar = fig.colorbar(hexbin_plots[-1], ax=axes.tolist(), orientation='vertical', cmap=hexcolor, aspect=30)
cbar.set_label('Trip count, log10(N)', fontsize=40)
cbar.ax.tick_params(labelsize=40)

plt.show()

######################################
# hexbin plot (Distance)
# Transit type
transit_types = df['Transit_type_all'].unique()
df = df.sort_values(by='Transit_type_all')
num_types = len(df['Transit_type_all'].unique())

fig, axes = plt.subplots(1, 4, figsize=(35, 12), constrained_layout=True, sharex=True, sharey=True)
axes = axes.flatten()
hexcolor = "viridis_r"

def plot_hexbin(subset, x_variable, y_variable, weights, ax, xlims, ylims):
    ax.hexbin(x=subset[x_variable], y=subset[y_variable],
              C=subset[weights], reduce_C_function=np.sum, bins="log", cmap=hexcolor, gridsize=30)
    bound = max(xlims + ylims)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.plot([min(xlims), bound], [min(ylims), bound], 'k-', alpha=1, zorder=3)

hexbin_plots = []

# Distance
for i, transit_type in enumerate(df['Transit_type_all'].unique()):
    subset_df = df[df['Transit_type_all'] == transit_type]
    hb = plot_hexbin(subset_df, 'TNC_miles', 'Transit_miles', 'Count',
                axes[i], (0, 50), (0, 50))
    hexbin_plots.append(hb)
    axes[i].set_title(transit_type)
    if i == 0 or i == 0: # Add y-label to the first subplot of the row
        axes[i].set_ylabel('Transit Distance (miles)')
    if i >= 0:  # Add x-label to the second row
        axes[i].set_xlabel('TNC Distance (miles)')

for ax in axes:
    ax.title.set_fontsize(40)
    ax.xaxis.label.set_fontsize(40)
    ax.yaxis.label.set_fontsize(40)
    ax.tick_params(axis='both', labelsize=40)

cbar = fig.colorbar(hexbin_plots[-1], ax=axes.tolist(), orientation='vertical', cmap=hexcolor, aspect=30)
cbar.set_label('Trip count, log10(N)', fontsize=40)
cbar.ax.tick_params(labelsize=40)

plt.show()

