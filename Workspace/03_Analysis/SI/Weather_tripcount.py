import pandas as pd
import matplotlib.pyplot as plt

# Read csv
df = pd.read_csv('dataframe_transit_cost.csv')

# Convert data type
columns_to_convert = ['TNC_miles', 'TNC_duration_total', 'TNC_fare', 'TNC_total_fare', 'WT_min', 'Transit_miles',
                      'Transit_duration', 'Transit_fare',
                      'Bus_duration', 'Subway_duration', 'Train_duration', 'Other_duration', 'Walk_duration', 'Time_gap',
                      'Time_Value_Matching', 'Time_Value_Matching_Social_ice_58', 'Time_Value_Matching_Social_ev40_58',
                      'Time_Value_Matching_Social_ev60_58']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column], errors='coerce')
print(df.dtypes)

df['snow_depth'] = df['snow_depth'].fillna(0)
df['precipitation'] = df['precipitation'].fillna(0)

df = df[['Year', 'Month', 'Day', 'Hour', 'Count', 'Time_Value_Matching', 'temperature', 'precipitation', 'snow_depth']]
df = df.groupby(['Year', 'Month', 'Day', 'Hour']).agg({
    'Count': 'sum',
    'Time_Value_Matching': 'mean',
    'temperature': 'mean',
    'precipitation': 'max',
    'snow_depth': 'max'
}).reset_index()
print(df.columns)
######################################
# Palette and marker
#colors = ['Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Blue']
#colors = ['Orange', 'Blue', 'lightblue', 'brown', 'Green', 'Yellow', 'Purple', 'Pink']
colors = [
    "#e6194B", # bright red
    "#3cb44b", # bright green
    "#ffe119", # yellow
    "#4363d8", # bright blue
    "#fabebe",  # pink
    "#911eb4", # purple
    "#46f0f0", # cyan
    "#f032e6", # magenta
    "#bcf60c", # lime
    "#f58231" # orange
]
marker_shapes = ['o', '^', 's', 'D', 'P', '*', '>', '<', 'H', '+', '1']
marker_size = 10


######################################
# hexbin
hexcolor = "magma"

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
hexbin_plots = []

# Temperature
hb_temperature = axs[0].hexbin(x=df['temperature'], y=df['Count'],
                               bins="log", cmap=hexcolor, gridsize=30)
hexbin_plots.append(hb_temperature)
axs[0].set_xlabel("Temperature (F)")
axs[0].set_ylabel('Hourly trip count')

# Precipitation
hb_precipitation = axs[1].hexbin(x=df['precipitation'], y=df['Count'],
                                  bins="log", cmap=hexcolor, gridsize=30)
hexbin_plots.append(hb_precipitation)
axs[1].set_xlabel("Precipitation (mm/hour)")

# Snow depth
hb_snow_depth = axs[2].hexbin(x=df['snow_depth'], y=df['Count'],
                               bins="log", cmap=hexcolor, gridsize=30)
hexbin_plots.append(hb_snow_depth)
axs[2].set_xlabel("Snow depth (inch)")

for ax in axs:
    ax.title.set_fontsize(24)
    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)
    ax.tick_params(axis='both', labelsize=24)

# Create a single color bar that is shared by all subplots
fig.subplots_adjust(right=0.8)
cb = fig.colorbar(hexbin_plots[-1], orientation='vertical', cmap=hexcolor)
cb.set_label('log10(N)', fontsize=24)
cb.ax.tick_params(labelsize=24)

plt.tight_layout()
plt.show()

###########
## scatter plot
fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# Temperature
axs[0].scatter(x=df['temperature'], y=df['Count'], alpha=0.1)
axs[0].set_xlabel("Temperature (F)")
axs[0].set_ylabel('Hourly trip count')

# Precipitation
axs[1].scatter(x=df['precipitation'], y=df['Count'], alpha=0.5)
axs[1].set_xlabel("Precipitation (mm/hour)")

# Snow depth
axs[2].scatter(x=df['snow_depth'], y=df['Count'], alpha=0.5)
axs[2].set_xlabel("Snow depth (inch)")

for ax in axs:
    ax.title.set_fontsize(24)
    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)
    ax.tick_params(axis='both', labelsize=24)

plt.tight_layout()
plt.show()


######################################
# hexbin - temp vs timecost
hexcolor = "magma"

df = df[(df['Time_Value_Matching'] > -100) & (df['Time_Value_Matching'] < 500)]

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
hexbin_plots = []
gridsize =30

# Temperature
hb_temperature = axs[0].hexbin(x=df['temperature'], y=df['Time_Value_Matching'], C=df['Count'],
                               bins="log", cmap=hexcolor, gridsize=gridsize)
hexbin_plots.append(hb_temperature)
axs[0].set_xlabel("Temperature (F)")
axs[0].set_ylabel('Value of travel time \n($/hour)')
#axs[0].set_ylim(bottom=0, top=150)

# Precipitation
hb_precipitation = axs[1].hexbin(x=df['precipitation'], y=df['Time_Value_Matching'], C=df['Count'],
                                  bins="log", cmap=hexcolor, gridsize=gridsize)
hexbin_plots.append(hb_precipitation)
axs[1].set_xlabel("Precipitation (mm/hour)")

# Snow depth
hb_snow_depth = axs[2].hexbin(x=df['snow_depth'], y=df['Time_Value_Matching'], C=df['Count'],
                               bins="log", cmap=hexcolor, gridsize=gridsize)
hexbin_plots.append(hb_snow_depth)
axs[2].set_xlabel("Snow depth (inch)")

for ax in axs:
    ax.title.set_fontsize(24)
    ax.xaxis.label.set_fontsize(24)
    ax.yaxis.label.set_fontsize(24)
    ax.tick_params(axis='both', labelsize=24)

# Create a single color bar that is shared by all subplots
fig.subplots_adjust(right=0.8)
cb = fig.colorbar(hexbin_plots[-1], orientation='vertical', cmap=hexcolor)
cb.set_label('log10(N)', fontsize=24)
cb.ax.tick_params(labelsize=24)

plt.tight_layout()
plt.show()

