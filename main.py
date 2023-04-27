import pyomo.environ as pyo
import math
from pre_processing import *
import numpy as np


model = pyo.AbstractModel()

## Model SETS
model.t = pyo.Set(initialize=get_l('list_time'))


## Model PARAMETERS
model.list_pv = pyo.Param(model.t, initialize=dict_Forecast(get_pv()))

model.life = pyo.Param(initialize=get_prop('life'))
model.LHV = pyo.Param(initialize=get_prop('LHV'))
model.h2_density = pyo.Param(initialize=get_prop('h2_density'))
model.flow_rate = pyo.Param(initialize=get_flow_rate('flow_rate'))

model.efficiency_ele = pyo.Param(initialize=get_efficiency('efficiency_ele'))
model.efficiency_bur = pyo.Param(initialize=get_efficiency('efficiency_bur'))
model.cap_installed = pyo.Param(initialize=get_cap_installed('cap_installed'))
model.thermal_load = pyo.Param(model.t, initialize=get_thermal_load(thermal_load))

model.power_rated_ele = pyo.Param(initialize=get_contstraint_ele('power_rated_ele'))
model.power_rated_bur = pyo.Param(initialize=get_contstraint_ele('power_rated_bur'))
model.perc_max_ele = pyo.Param(initialize=get_contstraint_ele('perc_max_ele'))
model.perc_min_ele = pyo.Param(initialize=get_contstraint_ele('perc_min_ele'))

model.CAPEX_ele = pyo.Param(initialize=get_CAPEX('CAPEX_ele'))
model.CAPEX_bur = pyo.Param(initialize=get_CAPEX('CAPEX_bur'))
model.OPEX_ele = pyo.Param(initialize=get_OPEX('OPEX_ele'))
model.OPEX_bur = pyo.Param(initialize=get_OPEX('OPEX_bur'))
model.cost_energy = pyo.Param(initialize=get_cost_energy('cost_energy'))


## Model VARIABLE
model.power_pv = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_grid = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.power_in_ele = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_ele = pyo.Var(model.t, within=pyo.NonNegativeReals)
#model.power_rated_ele = pyo.Var(within=pyo.NonNegativeReals)

model.power_in_bur = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_bur = pyo.Var(model.t, within=pyo.NonNegativeReals)



## Model COSTRAINTS
# constraint at POWER PV
def constraint_power_pv(xx, t):
    return xx.power_pv[t] <= xx.cap_installed*xx.list_pv[t]
model.constr_power_pv = pyo.Constraint(model.t, rule=constraint_power_pv)

# constraint at NODE 1
def constraint_n1(xx, t):
    return xx.power_pv[t] + xx.power_grid[t] == xx.power_in_ele[t]
model.constr_n1 = pyo.Constraint(model.t, rule=constraint_n1)

# constraint at ELECTROLYSER
def constraint_out_ele(xx, t):
    return xx.power_out_ele[t] == xx.efficiency_ele*xx.power_in_ele[t]
model.constr_out_ele = pyo.Constraint(model.t, rule=constraint_out_ele)

# constraint at ELECTROLYSER POWER
def constraint_max_power_ele(xx, t):
    return xx.power_in_ele[t] <= xx.power_rated_ele*xx.perc_max_ele
model.constr_max_power_ele = pyo.Constraint(model.t, rule=constraint_max_power_ele)

def constraint_min_power_ele(xx, t):
    return xx.power_in_ele[t] >= xx.power_rated_ele*xx.perc_min_ele
model.constr_min_power_ele = pyo.Constraint(model.t, rule=constraint_min_power_ele)

# constraint at NODE 2
def constraint_n2(xx, t):
    return xx.power_out_ele[t] == xx.power_in_bur[t]
model.constr_n2 = pyo.Constraint(model.t, rule=constraint_n2)

# constraint at BURNER OUTPUT
def constraint_out_bur(xx, t):
    return xx.power_out_bur[t] == xx.efficiency_bur*xx.power_in_bur[t]
model.constr_out_bur = pyo.Constraint(model.t, rule=constraint_out_bur)

# constraint at LOAD
def constraint_load(xx, t):
    return xx.power_out_bur[t] == xx.thermal_load[t]
model.constr_power_load = pyo.Constraint(model.t, rule=constraint_load)


## Model OBJECTIVE FUNCTIONS
def func_object(xx):
    C_npc_CAPEX = xx.power_rated_ele*xx.CAPEX_ele + xx.power_rated_bur*xx.CAPEX_bur
    C_npc_OPEX = xx.power_rated_ele*xx.OPEX_ele + xx.power_rated_bur*xx.OPEX_bur
    C_electricity = sum(xx.power_grid[t]*xx.cost_energy for t in list_time)
    C_npc_TOT = C_npc_CAPEX + C_npc_OPEX*xx.life + C_electricity*xx.life

    return C_npc_TOT
model.func_obj = pyo.Objective(rule=func_object, sense=pyo.minimize)


## OPTIMIZATION SOLVING
instance = model.create_instance()
opt = pyo.SolverFactory('glpk')
results = opt.solve(instance)
results.write()













## LCOE CALCULATION
"""

    LCOE = []
    for year in xx.model.life:
        LCOE_year = 
        LCOE.append(LCOE_year)



"""