import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

################################################################################
# Trip count per day
# Reading CSV data
df = pd.read_csv('Trip_counts.csv')

# Convert data in the date column to a datetime type
df['Date'] = pd.to_datetime(df['Date'])
print(df)

# Sort the values by Date
df = df.sort_values('Date')

################################################################################
# Trip in a day
# Reading CSV data
df_wd = pd.read_csv('weekday_tripcount.csv')
df_we = pd.read_csv('weekend_tripcount.csv')

plt.figure(figsize=(8, 5))
for column in df_wd.columns[1:]:  # Exclude the 'Time' column
    plt.plot(df_wd['Time'], df_wd[column],label=column)
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(4))  # Set ticks at every hour

plt.ylabel('Trip Counts per 15mins')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()

plt.figure(figsize=(8, 5))
for column in df_we.columns[1:]:  # Exclude the 'Time' column
    plt.plot(df_we['Time'], df_we[column], label=column)
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(4))  # Set ticks at every hour

plt.ylabel('Trip Counts per 15mins')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()

print('Done')