import json
import copy

class Transit:

    def __init__(self, name, fuel_consumption, electric_ratio, occupancy, winter_penalty, summer_penalty, lifetime_year, vmt_per_year,
                ghg_operation_emissions, So2_operation_emissions, Nox_operation_emissions, PM_operation_emissions, VOC_operation_emissions,
                PM_lifetime_cost, So2_lifetime_cost, Nox_lifetime_cost, VOC_lifetime_cost,
                lifetime_GHG, lifetime_So2, lifetime_Nox, lifetime_PM, lifetime_VOC,
                Collision_cost, Congestion_cost, Noise_cost):
        """
        Fuel consumption: float
            Fuel consumption; kWh per mile or gallon per mile.

        Electric_ratio: float
            Only for train. Electric vehicle mile % vs diesel miles

        operation_emissions: float
            emissions per mile

        Lifetime_cost: float
            MD $ per kg-emissions, calculated MD based on FIPS of each activity (mining, production, manufacturing)
            Source: Census CBP datasets

        Lifetime emissions: float
            kg/car-lifetime mile

        Transit cost: float
            USD per mile
        """
        self.name = name
        self.fuel_consumption = fuel_consumption
        self.electric_ratio = electric_ratio
        self.occupancy = occupancy
        self.winter_penalty = winter_penalty
        self.summer_penalty = summer_penalty
        self.lifetime_year = lifetime_year
        self.vmt_per_year = vmt_per_year
        self.ghg_operation_emissions = ghg_operation_emissions
        self.So2_operation_emissions = So2_operation_emissions
        self.Nox_operation_emissions = Nox_operation_emissions
        self.PM_operation_emissions = PM_operation_emissions
        self.VOC_operation_emissions = VOC_operation_emissions
        self.PM_lifetime_cost = PM_lifetime_cost
        self.So2_lifetime_cost = So2_lifetime_cost
        self.Nox_lifetime_cost = Nox_lifetime_cost
        self.VOC_lifetime_cost = VOC_lifetime_cost
        self.lifetime_GHG = lifetime_GHG
        self.lifetime_So2 = lifetime_So2
        self.lifetime_Nox = lifetime_Nox
        self.lifetime_PM = lifetime_PM
        self.lifetime_VOC = lifetime_VOC
        self.Collision_cost = Collision_cost
        self.Congestion_cost = Congestion_cost
        self.Noise_cost = Noise_cost

    def copy(self, **kwargs) -> "Transit":
        res = copy.copy(self)
        for k, v in kwargs.items():
            setattr(res, k, v)
        return res
