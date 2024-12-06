import json
import copy

class Fuel:

    def __init__(self, name, ghg_factor_fuel, So2_factor_fuel, Nox_factor_fuel, PM_factor_fuel, VOC_factor_fuel,
                 PM_upstream_cost, So2_upstream_cost, Nox_upstream_cost, VOC_upstream_cost):
        """
        Fuel consumption: float
            Fuel consumption; kWh per mile or gallon per mile.

        Emissions factor fuel: float
            Emissions are in kg per gallon or kWh;
            Gasoline, Diesel: GREET well-to-wheel emissions
            Electricity: PJM marginal damage by CMU tool (based on AP2)

        Upstream cost: float
            Marginal health damage cost for the upstream air pollution.
            For diesel/gasoline, refinery locations {EPA}.
            For electricity, PJM marginal damage by CMU tool (based on AP2)

        """
        self.name = name
        self.ghg_factor_fuel = ghg_factor_fuel
        self.So2_factor_fuel = So2_factor_fuel
        self.Nox_factor_fuel = Nox_factor_fuel
        self.PM_factor_fuel = PM_factor_fuel
        self.VOC_factor_fuel = VOC_factor_fuel
        self.PM_upstream_cost = PM_upstream_cost
        self.So2_upstream_cost = So2_upstream_cost
        self.Nox_upstream_cost = Nox_upstream_cost
        self.VOC_upstream_cost = VOC_upstream_cost

    def copy(self, **kwargs) -> "Fuel":
        res = copy.copy(self)
        for k, v in kwargs.items():
            setattr(res, k, v)
        return res
