import json
import copy

class TNC:

    def __init__(self, name, fuel_consumption, deadheading, wait_minutes, winter_penalty, summer_penalty, lifetime_mile,
                 ghg_operation_emissions, So2_operation_emissions, Nox_operation_emissions, PM_operation_emissions,
                 VOC_operation_emissions, So2_gallon_emissions, Nox_gallon_emissions, PM_gallon_emissions,
                 VOC_gallon_emissions, lifetime_GHG, lifetime_So2, lifetime_Nox, lifetime_PM, lifetime_VOC,
                 Collision_cost, Congestion_cost, Noise_cost):
        """
        Fuel consumption: float
            Fuel consumption; kWh per mile or gallon per mile.

        Deadheading: float
            Deadheading addition to the trip distance

        operation_emissions: float
            kg per mile <- ***input from Mohan 2023 based on MOVES3*** Included cold start, brake/tire emissions etc


        gallon_emissions: float
            kg per gallon emissions for fuel combustion. Used to calculate summer/winter penalty Source: GREET


        Lifetime emissions: float
            USD/car-lifetime mile  <- ***input from Mohan 2023 based on GREET***

        Transit cost: float
            USD per mile
        """
        self.name = name
        self.fuel_consumption = fuel_consumption
        self.deadheading = deadheading
        self.wait_minutes = wait_minutes
        self.winter_penalty = winter_penalty
        self.summer_penalty = summer_penalty
        self.lifetime_mile = lifetime_mile
        self.ghg_operation_emissions = ghg_operation_emissions
        self.So2_operation_emissions = So2_operation_emissions
        self.Nox_operation_emissions = Nox_operation_emissions
        self.PM_operation_emissions = PM_operation_emissions
        self.VOC_operation_emissions = VOC_operation_emissions
        self.So2_gallon_emissions = So2_gallon_emissions
        self.Nox_gallon_emissions = Nox_gallon_emissions
        self.PM_gallon_emissions = PM_gallon_emissions
        self.VOC_gallon_emissions = VOC_gallon_emissions
        self.lifetime_GHG = lifetime_GHG
        self.lifetime_So2 = lifetime_So2
        self.lifetime_Nox = lifetime_Nox
        self.lifetime_PM = lifetime_PM
        self.lifetime_VOC = lifetime_VOC
        self.Collision_cost = Collision_cost
        self.Congestion_cost = Congestion_cost
        self.Noise_cost = Noise_cost

    def copy(self, **kwargs) -> "TNC":
        res = copy.copy(self)
        for k, v in kwargs.items():
            setattr(res, k, v)
        return res
