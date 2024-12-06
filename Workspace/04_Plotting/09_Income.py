import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.colors as mcolors
from statsmodels.nonparametric.kde import KDEUnivariate

from Tools.Cumulative_distribution import plot_cumulative_distribution, plot_cumulative_distribution_comparison, plot_cumulative_distribution_weather


transit_cost = pd.read_csv('dataframe_transit_cost.csv')
df = transit_cost[['Pickup_CA', 'Dropoff_CA', 'Time_Value_Matching', 'Count']]
print(df.columns)

df_income = pd.read_csv('income.csv')
print(df_income.columns)

df['Pickup_CA'] = df['Pickup_CA'].astype(float)
df['Dropoff_CA'] = df['Dropoff_CA'].astype(float)
df_income['CA'] = df_income['CA'].astype(float)

df_pickup = pd.merge(df, df_income, left_on='Pickup_CA', right_on='CA', how='left')
df_dropoff = pd.merge(df, df_income, left_on='Dropoff_CA', right_on='CA', how='left')

print(df_pickup.sample(10))
print(df_dropoff.sample(10))

## Plot
fig, ax = plt.subplots(figsize=(15, 5))
hexbin_plots = []
hexcolor = "magma"
gridsize =50

hb_temperature = ax.hexbin(x=df_pickup['Median household income'], y=df_pickup['Time_Value_Matching'], C=df_pickup['Count'],
                               bins="log", cmap=hexcolor, gridsize=gridsize)
hexbin_plots.append(hb_temperature)
ax.set_xlabel("Median Household Income ($) - Pickup Community Area")
ax.set_ylabel('Value of travel time \n($/hour)')

fig.subplots_adjust(right=0.8)
cb = fig.colorbar(hexbin_plots[-1], orientation='vertical', cmap=hexcolor)
cb.set_label('log10(N)', fontsize=24)
cb.ax.tick_params(labelsize=24)

ax.title.set_fontsize(24)
ax.xaxis.label.set_fontsize(24)
ax.yaxis.label.set_fontsize(24)
ax.tick_params(axis='both', labelsize=24)

plt.tight_layout()
plt.show()

## Plot
fig, ax = plt.subplots(figsize=(15, 5))
hexbin_plots = []
hexcolor = "magma"
gridsize =50

hb_temperature = ax.hexbin(x=df_dropoff['Median household income'], y=df_dropoff['Time_Value_Matching'], C=df_dropoff['Count'],
                           bins="log", cmap=hexcolor, gridsize=gridsize)
hexbin_plots.append(hb_temperature)
ax.set_xlabel("Median Household Income ($) - Dropoff Community Area")
ax.set_ylabel('Value of travel time \n($/hour)')

fig.subplots_adjust(right=0.8)
cb = fig.colorbar(hexbin_plots[-1], orientation='vertical', cmap=hexcolor)
cb.set_label('log10(N)', fontsize=24)
cb.ax.tick_params(labelsize=24)

ax.title.set_fontsize(24)
ax.xaxis.label.set_fontsize(24)
ax.yaxis.label.set_fontsize(24)
ax.tick_params(axis='both', labelsize=24)

plt.tight_layout()
plt.show()

## Income bins
income_bins = [0, 50000, 100000, 1500000]
income_labels = ['<50K','50K-100K', '100K-150K']
df_dropoff['Income Range'] = pd.cut(df_dropoff['Median household income'], bins=income_bins, labels=income_labels)
df_pickup['Income Range'] = pd.cut(df_pickup['Median household income'], bins=income_bins, labels=income_labels)

print("Dropoff:", df_dropoff.groupby("Income Range")['Count'].sum())
print("Pickup:", df_pickup.groupby("Income Range")['Count'].sum())

print("Dropoff:", df_dropoff.groupby("Income Range")['Time_Value_Matching'].median())
print("Pickup:", df_pickup.groupby("Income Range")['Time_Value_Matching'].median())


## box plot
df_dropoff['Income Range'] = pd.cut(df_dropoff['Median household income'], bins=income_bins, labels=income_labels)
fig, ax = plt.subplots(figsize=(5, 5))
df_dropoff.boxplot(column='Time_Value_Matching', by='Income Range', ax=ax, showfliers=False)
ax.set_xlabel("Income Range - Drop-off Area")
ax.set_ylabel("Value of travel time \n($/hour)")
#ax.set_title("Box Plot of Value of Travel Time by Income Range")
ax.tick_params(axis='both', labelsize=12)
plt.suptitle("")
plt.tight_layout()
plt.show()

df_pickup['Income Range'] = pd.cut(df_pickup['Median household income'], bins=income_bins, labels=income_labels)
fig, ax = plt.subplots(figsize=(5, 5))
df_pickup.boxplot(column='Time_Value_Matching', by='Income Range', ax=ax, showfliers=False)
ax.set_xlabel("Income Range - Pick-up Area")
ax.set_ylabel("Value of travel time \n($/hour)")
#ax.set_title("Box Plot of Value of Travel Time by Income Range")
ax.tick_params(axis='both', labelsize=12)
plt.suptitle("")
plt.tight_layout()
plt.show()
