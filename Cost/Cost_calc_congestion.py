import numpy as np
from Cost.Emissions import calc_emissions_tnc, calc_emissions_transit_per_mile

def calc_cost_tnc(df, TNC, Fuel, Cost):
    calc_emissions_tnc(df, TNC, Fuel)

    trip_miles = df['TNC_miles']
    miles_with_deadhead = trip_miles * (1 + TNC.deadheading)

    # Emission externality
    ### Adding lifecycle emissions cost here, as the input from Mohan2023 is in USD/lifetime.
    ghg_emissions = df['GHG_emissions']
    lifecycle_ghg = miles_with_deadhead * TNC.lifetime_GHG / TNC.lifetime_mile
    ghg_cost = ghg_emissions * Cost.Carbon_cost + lifecycle_ghg
    df['GHG_lifecycle_emissions'] = lifecycle_ghg / Cost.Carbon_cost

    upstream_So2 = df['So2_upstream_emissions'] * Fuel.So2_upstream_cost
    tailpipe_So2 = df['So2_tailpipe_emissions'] * Cost.So2_tailpipe_cost
    lifecycle_So2 = miles_with_deadhead * TNC.lifetime_So2 / TNC.lifetime_mile
    So2_cost = upstream_So2 + tailpipe_So2 + lifecycle_So2

    upstream_Nox = df['Nox_upstream_emissions'] * Fuel.Nox_upstream_cost
    tailpipe_Nox = df['Nox_tailpipe_emissions'] * Cost.Nox_tailpipe_cost
    lifecycle_Nox = miles_with_deadhead * TNC.lifetime_Nox / TNC.lifetime_mile
    Nox_cost = upstream_Nox + tailpipe_Nox + lifecycle_Nox

    upstream_PM = df['PM_upstream_emissions'] * Fuel.PM_upstream_cost
    tailpipe_PM = df['PM_tailpipe_emissions'] * Cost.PM_tailpipe_cost
    lifecycle_PM = miles_with_deadhead * TNC.lifetime_PM / TNC.lifetime_mile
    PM_cost = upstream_PM + tailpipe_PM + lifecycle_PM

    air_pollutant_cost = So2_cost + Nox_cost + PM_cost

    # Other externality
    drive_miles = df['TNC_miles']
    miles_with_deadhead = drive_miles * (1 + TNC.deadheading)
    hour = df['Hour']

    Collision_cost = TNC.Collision_cost * miles_with_deadhead

    Congestion_cost = np.where(
        (hour < 9) | ((hour > 15) & (hour < 19)),
        0.18 * miles_with_deadhead, #peak (6-8am)
        0.028 * miles_with_deadhead #off-peak (4-6pm)
    )

    Noise_cost = TNC.Noise_cost * miles_with_deadhead
    other_externality = Collision_cost + Congestion_cost + Noise_cost

    # Total externality
    total_externality = ghg_cost + air_pollutant_cost + other_externality

    trip_time = df['TNC_duration_total']
    wait_time = df['TNC_wait_time']

    # Travel time saving value
    ## trip_time: total trip time. Cost is calculated by total trip time * trip time cost by DoT
    ## Walk time: walking time. Cost is additional amount to the normal "trip time cost" by DoT
    ## Other time: waiting, standing, and transfer time. Cost is additional amount to the normal "trip time cost" by DoT
    time_value_total = trip_time * Cost.Time_value + wait_time * Cost.Time_walk_value
    trip_cost_with_time = df['TNC_total_fare'] + time_value_total
    wait_time_value = wait_time * (Cost.Time_walk_value + Cost.Time_value)

    df_new = df.copy()
    df_new.loc[:, 'GHG_cost'] = ghg_cost
    df_new.loc[:, 'Air_pollutant_cost'] = air_pollutant_cost
    df_new.loc[:, 'Collision_cost'] = Collision_cost
    df_new.loc[:, 'Congestion_cost'] = Congestion_cost
    df_new.loc[:, 'Noise_cost'] = Noise_cost
    df_new.loc[:, 'Other_externality'] = other_externality
    df_new.loc[:, 'Externality'] = total_externality
    df_new.loc[:, 'Time_cost'] = time_value_total
    df_new.loc[:, 'Wait_time_cost'] = wait_time_value
    df_new.loc[:, 'Trip_fare_with_time_cost'] = trip_cost_with_time

    return df_new

def calc_cost_single_transit_per_mile(df, Transit, Fuel, Cost):
    df = calc_emissions_transit_per_mile(df, Transit, Fuel)

    # Emission externality
    ghg_emissions = df['GHG_emissions']
    ghg_cost = ghg_emissions * Cost.Carbon_cost

    upstream_So2 = df['So2_upstream_emissions'] * Fuel.So2_upstream_cost
    tailpipe_So2 = df['So2_tailpipe_emissions'] * Cost.So2_tailpipe_cost
    lifecycle_So2 =  df['So2_lifecycle_emissions'] * Transit.So2_lifetime_cost
    So2_cost = upstream_So2 + tailpipe_So2 + lifecycle_So2

    upstream_Nox = df['Nox_upstream_emissions'] * Fuel.Nox_upstream_cost
    tailpipe_Nox = df['Nox_tailpipe_emissions'] * Cost.Nox_tailpipe_cost
    lifecycle_Nox =  df['Nox_lifecycle_emissions'] * Transit.Nox_lifetime_cost
    Nox_cost = upstream_Nox + tailpipe_Nox + lifecycle_Nox

    upstream_PM = df['PM_upstream_emissions'] * Fuel.PM_upstream_cost
    tailpipe_PM = df['PM_tailpipe_emissions'] * Cost.PM_tailpipe_cost
    lifecycle_PM =  df['PM_lifecycle_emissions'] * Transit.PM_lifetime_cost
    PM_cost = upstream_PM + tailpipe_PM + lifecycle_PM

    air_pollutant_cost = So2_cost + Nox_cost + PM_cost

    # Other externality
    Collision_cost = Transit.Collision_cost / Transit.occupancy
    Congestion_cost = Transit.Congestion_cost / Transit.occupancy
    Noise_cost = Transit.Noise_cost / Transit.occupancy
    other_externality = Collision_cost + Congestion_cost + Noise_cost

    # Total externality
    total_externality = ghg_cost + air_pollutant_cost + other_externality

    # Google_search fare
    trip_fare = df['Transit_fare']

    # Travel time saving value
    ## trip_time: total trip time. Cost is calculated by total trip time * trip time cost by DoT
    ## Walk time: walking time. Cost is additional amount to the normal "trip time cost" by DoT
    ## Other time: waiting, standing, and transfer time. Cost is additional amount to the normal "trip time cost" by DoT
    trip_time = df['Transit_duration']
    walk_time = df['Walk_duration']
    other_time = df['Other_duration']

    time_value_total = trip_time * Cost.Time_value + (walk_time + other_time) * Cost.Time_walk_value
    trip_cost_with_time = trip_fare + time_value_total
    wait_time_value = other_time * (Cost.Time_walk_value + Cost.Time_value)
    walk_time_value = walk_time * (Cost.Time_walk_value + Cost.Time_value)

    df_new = df.copy()
    df_new.loc[:, 'GHG_cost'] = ghg_cost
    df_new.loc[:, 'Air_pollutant_cost'] = air_pollutant_cost
    df_new.loc[:, 'Collision_cost'] = Collision_cost
    df_new.loc[:, 'Congestion_cost'] = Congestion_cost
    df_new.loc[:, 'Noise_cost'] = Noise_cost
    df_new.loc[:, 'Other_externality'] = other_externality
    df_new.loc[:, 'Externality'] = total_externality
    df_new.loc[:, 'Time_cost'] = time_value_total
    df_new.loc[:, 'Walk_time_cost'] = walk_time_value
    df_new.loc[:, 'Wait_time_cost'] = wait_time_value
    df_new.loc[:, 'Trip_fare_with_time_cost'] = trip_cost_with_time

    return df_new

def calc_cost_transit(df, Bus, Subway, Train_diesel, Train_electric, Diesel, Electricity, Electricity_Average, Cost):

    bus_miles = df['Bus_miles']
    subway_miles = df["Subway_miles"]
    train_miles = df["Train_miles"]
    walk_miles = df["Walk_miles"]

    #The last one of below will be shown up in the output excel
    bus_cost = calc_cost_single_transit_per_mile(df, Bus, Diesel, Cost)
    subway_cost = calc_cost_single_transit_per_mile(df, Subway, Electricity_Average, Cost)
    train_diesel_cost = calc_cost_single_transit_per_mile(df, Train_diesel, Diesel, Cost)
    train_electric_cost = calc_cost_single_transit_per_mile(df, Train_electric, Electricity_Average, Cost)

    electric_train_rate = df['Electric_train_rate']

    ghg_cost = (bus_cost['GHG_cost'] * bus_miles + subway_cost['GHG_cost'] * subway_miles
                + train_diesel_cost['GHG_cost'] * train_miles * (1 - electric_train_rate)
                + train_electric_cost['GHG_cost'] * train_miles * electric_train_rate)

    bus_emissions_per_mile = bus_cost['GHG_emissions']
    subway_emissions_per_mile = subway_cost['GHG_emissions']
    train_diesel_emissions_per_mile = train_diesel_cost['GHG_emissions']
    train_electric_emissions_per_mile = train_electric_cost['GHG_emissions']

    air_pollutant_cost = (bus_cost['Air_pollutant_cost'] * bus_miles +
                          subway_cost['Air_pollutant_cost'] * subway_miles +
                          train_diesel_cost['Air_pollutant_cost'] * train_miles * ( 1 - electric_train_rate) +
                          train_electric_cost['Air_pollutant_cost'] * train_miles * electric_train_rate)

    # Other externality
    Collision_cost = (bus_cost['Collision_cost'] * bus_miles + subway_cost['Collision_cost'] * subway_miles
                + train_diesel_cost['Collision_cost'] * train_miles * (1 - electric_train_rate)
                + train_electric_cost['Collision_cost'] * train_miles * electric_train_rate
                + Cost.Walk_collision_cost * walk_miles)

    hour = df['Hour']
    Congestion_cost = np.where(
        (hour < 9) | ((hour > 15) & (hour < 19)),
        (0.047 * bus_miles + 0.0042 * walk_miles), #peak (6-8am)
        (0.007 * bus_miles + 0.0014 * walk_miles) #off-peak (4-6pm)
    )

    Noise_cost = (bus_cost['Noise_cost'] * bus_miles + subway_cost['Noise_cost'] * subway_miles
                + train_diesel_cost['Noise_cost'] * train_miles * (1 - electric_train_rate)
                + train_electric_cost['Noise_cost'] * train_miles * electric_train_rate
                + Cost.Walk_noise_cost * walk_miles)
    other_externality = Collision_cost + Congestion_cost + Noise_cost

    # Total externality
    total_externality = ghg_cost + air_pollutant_cost + other_externality

    # Time value of money
    time_value_total = bus_cost['Time_cost'] #same for all dfs
    trip_cost_with_time = bus_cost['Trip_fare_with_time_cost']
    wait_time_value = bus_cost['Wait_time_cost']
    walk_time_value = bus_cost['Walk_time_cost']

    df_new = df.copy()
    df_new.loc[:, 'Bus_GHG_emissions_per_mile'] = bus_emissions_per_mile
    df_new.loc[:, 'Subway_GHG_emissions_per_mile'] = subway_emissions_per_mile
    df_new.loc[:, 'Train_diesel_GHG_emissions_per_mile'] = train_diesel_emissions_per_mile
    df_new.loc[:, 'Train_electric_GHG_emissions_per_mile'] = train_electric_emissions_per_mile
    df_new.loc[:, 'GHG_cost'] = ghg_cost
    df_new.loc[:, 'Air_pollutant_cost'] = air_pollutant_cost
    df_new.loc[:, 'Collision_cost'] = Collision_cost
    df_new.loc[:, 'Congestion_cost'] = Congestion_cost
    df_new.loc[:, 'Noise_cost'] = Noise_cost
    df_new.loc[:, 'Other_externality'] = other_externality
    df_new.loc[:, 'Externality'] = total_externality
    df_new.loc[:, 'Time_cost'] = time_value_total
    df_new.loc[:, 'Walk_time_cost'] = walk_time_value
    df_new.loc[:, 'Wait_time_cost'] = wait_time_value
    df_new.loc[:, 'Trip_fare_with_time_cost'] = trip_cost_with_time

    return df_new
