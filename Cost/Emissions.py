

def calc_emissions_tnc(df, TNC, Fuel):
    trip_miles = df['TNC_miles']
    miles_with_deadhead = trip_miles * (1 + TNC.deadheading)

    #Get seasonal penalty
    df['Season'] = df['Season'].astype(str).str.strip()

    def get_season_penalty(season):
        if season == 'Winter':
            return TNC.winter_penalty
        elif season == 'Summer':
            return TNC.summer_penalty
        else:
            return 0

    season_penalty = df['Season'].apply(get_season_penalty)

    #Fuel consumption in gallon or kWh
    fuel_consumption = TNC.fuel_consumption * (1 + season_penalty) * miles_with_deadhead #kWh or gallon

    ##### emissions calculation for upstream and tailpipe only #####
    # Get GHG emissions
    ghg_emissions = fuel_consumption * TNC.ghg_operation_emissions # For engine combustion (vehicle operation)
    ghg_fuel_emissions = fuel_consumption * Fuel.ghg_factor_fuel #kWh * kgCO2/kWh (well-to-pump)
    lifecycle_ghg = 0 # vehicle manufacturing, EoL. Input is already in USD, so not adding as emissions here.

    #Air pollutant emissions
    So2_emissions = miles_with_deadhead * TNC.So2_operation_emissions + TNC.So2_gallon_emissions * fuel_consumption * season_penalty
    So2_fuel_emissions = fuel_consumption * Fuel.So2_factor_fuel
    lifecycle_So2 = 0 # vehicle manufacturing, EoL. Input is already in USD, so not adding as emissions here.

    Nox_emissions = miles_with_deadhead * TNC.Nox_operation_emissions + TNC.Nox_gallon_emissions * fuel_consumption * season_penalty
    Nox_fuel_emissions = fuel_consumption * Fuel.Nox_factor_fuel
    lifecycle_Nox = 0 # vehicle manufacturing, EoL. Input is already in USD, so not adding as emissions here.

    PM_emissions = miles_with_deadhead * TNC.PM_operation_emissions + TNC.PM_gallon_emissions * fuel_consumption * season_penalty
    PM_fuel_emissions = fuel_consumption * Fuel.PM_factor_fuel
    lifecycle_PM = 0 # vehicle manufacturing, EoL. Input is already in USD, so not adding as emissions here.

    df.loc[:, 'GHG_emissions'] = ghg_emissions + ghg_fuel_emissions
    df.loc[:, 'GHG_upstream_emissions'] = ghg_fuel_emissions
    df.loc[:, 'GHG_tailpipe_emissions'] = ghg_emissions
    df.loc[:, 'GHG_lifecycle_emissions'] = lifecycle_ghg
    df.loc[:, 'So2_upstream_emissions'] = So2_fuel_emissions
    df.loc[:, 'Nox_upstream_emissions'] = Nox_fuel_emissions
    df.loc[:, 'PM_upstream_emissions'] = PM_fuel_emissions
    df.loc[:, 'So2_tailpipe_emissions'] = So2_emissions
    df.loc[:, 'Nox_tailpipe_emissions'] = Nox_emissions
    df.loc[:, 'PM_tailpipe_emissions'] = PM_emissions

    return df


def calc_emissions_transit_per_mile(df, Transit, Fuel):
    transit_miles = 1

    #Get seasonal penalty
    df['Season'] = df['Season'].astype(str).str.strip()

    def get_season_penalty(season):
        if season == 'Winter':
            return Transit.winter_penalty
        elif season == 'Summer':
            return Transit.summer_penalty
        else:
            return 0

    season_penalty = df['Season'].apply(get_season_penalty)

    #Fuel consumption in gallon / kWh
    fuel_consumption_vkt = Transit.fuel_consumption * (1 + season_penalty) #kWh or gallon
    fuel_consumption_pkt = fuel_consumption_vkt / Transit.occupancy
    fuel_consumption = fuel_consumption_pkt * transit_miles

    # Get GHG emissions
    ghg_emissions = fuel_consumption * Transit.ghg_operation_emissions # For engine combustion (vehicle operation)
    ghg_fuel_emissions = fuel_consumption * Fuel.ghg_factor_fuel #kWh * kgCO2/kWh (well-to-pump)
    lifecycle_ghg = transit_miles * Transit.lifetime_GHG  / (Transit.lifetime_year * Transit.vmt_per_year * Transit.occupancy) # vehicle manufacturing, EoL

    #Air pollutant emissions
    So2_emissions = fuel_consumption * Transit.So2_operation_emissions
    So2_fuel_emissions = fuel_consumption * Fuel.So2_factor_fuel
    lifecycle_So2 = transit_miles * Transit.lifetime_So2  / (Transit.lifetime_year * Transit.vmt_per_year * Transit.occupancy)

    Nox_emissions = fuel_consumption * Transit.Nox_operation_emissions
    Nox_fuel_emissions = fuel_consumption * Fuel.Nox_factor_fuel
    lifecycle_Nox = transit_miles * Transit.lifetime_Nox  / (Transit.lifetime_year * Transit.vmt_per_year * Transit.occupancy)

    PM_emissions = fuel_consumption * Transit.PM_operation_emissions
    PM_fuel_emissions = fuel_consumption * Fuel.PM_factor_fuel
    lifecycle_PM = transit_miles * Transit.lifetime_PM  / (Transit.lifetime_year * Transit.vmt_per_year * Transit.occupancy)

    df.loc[:, 'Penalty'] = season_penalty
    df.loc[:, 'GHG_emissions'] = ghg_emissions + ghg_fuel_emissions + lifecycle_ghg
    df.loc[:, 'GHG_upstream_emissions'] = ghg_fuel_emissions
    df.loc[:, 'GHG_tailpipe_emissions'] = ghg_emissions
    df.loc[:, 'GHG_lifecycle_emissions'] = lifecycle_ghg
    df.loc[:, 'So2_upstream_emissions'] = So2_fuel_emissions
    df.loc[:, 'Nox_upstream_emissions'] = Nox_fuel_emissions
    df.loc[:, 'PM_upstream_emissions'] = PM_fuel_emissions
    df.loc[:, 'So2_tailpipe_emissions'] = So2_emissions
    df.loc[:, 'Nox_tailpipe_emissions'] = Nox_emissions
    df.loc[:, 'PM_tailpipe_emissions'] = PM_emissions
    df.loc[:, 'So2_lifecycle_emissions'] = lifecycle_So2
    df.loc[:, 'Nox_lifecycle_emissions'] = lifecycle_Nox
    df.loc[:, 'PM_lifecycle_emissions'] = lifecycle_PM

    return df
