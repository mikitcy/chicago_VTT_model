import pandas as pd

from Trip_data_clean.Cleaning import clean, filter

### 2022
tripdata_2022 = pd.read_csv('tripdata.csv')
print(tripdata_2022.dtypes)
print(len(tripdata_2022))

df_cleaned_2022 = clean(tripdata_2022)
print(len(df_cleaned_2022))

df_filtered_2022 = filter(df_cleaned_2022)
df_filtered_2022.to_csv('filtered_tripdata.csv', index=False)

print("Completed")