import json
import copy

class Cost:

    def __init__(self, name, Carbon_cost, PM_tailpipe_cost, So2_tailpipe_cost, Nox_tailpipe_cost, VOC_tailpipe_cost, Time_value, Time_walk_value, Static_life_value,
                 Walk_collision_cost, Walk_congestion_cost, Walk_noise_cost, Walk_benefit_per_mile):
        """
        Emissions: float
            Emissions cost factors are $/kg emissions

        Externality cost: float
            Collision, congestion, noise cost: $/mile
            Value of travel time saving: $/hr (1/3 of regional wage)

        tailpipe_cost:
            Marginal damage in Cook County (Chicago City). This is used for damage calculation for tailpipe emissions only
        """
        self.name = name
        self.Carbon_cost = Carbon_cost
        self.PM_tailpipe_cost = PM_tailpipe_cost
        self.So2_tailpipe_cost = So2_tailpipe_cost
        self.Nox_tailpipe_cost = Nox_tailpipe_cost
        self.VOC_tailpipe_cost = VOC_tailpipe_cost
        self.Time_value = Time_value
        self.Time_walk_value = Time_walk_value
        self.Static_life_value = Static_life_value
        self.Walk_collision_cost = Walk_collision_cost
        self.Walk_congestion_cost = Walk_congestion_cost
        self.Walk_noise_cost = Walk_noise_cost
        self.Walk_benefit_per_mile = Walk_benefit_per_mile

    def copy(self, **kwargs) -> "Cost":
        res = copy.copy(self)
        for k, v in kwargs.items():
            setattr(res, k, v)
        return res
