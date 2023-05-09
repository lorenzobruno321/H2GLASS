from post_processing import *
import pyomo.environ as pyo
import math
from pre_processing import *
import numpy as np

model = pyo.AbstractModel()

## Model SETS
model.t = pyo.Set(initialize=get_l('list_time'))

## Model PARAMETERS
model.list_pv = pyo.Param(model.t, initialize=dict_Forecast(get_pv()))

time_vec = list(range(365*24))
model.delta_t = pyo.Param(initialize=get_l('time_step'))
model.life = pyo.Param(initialize=get_prop('life'))
model.LHV = pyo.Param(initialize=get_prop('LHV'))
model.compression_work = pyo.Param(initialize=get_prop('compression_work'))
model.h2_density = pyo.Param(initialize=get_prop('h2_density'))
model.flow_rate = pyo.Param(initialize=get_flow_rate('flow_rate'))

model.efficiency_ele = pyo.Param(initialize=get_efficiency('efficiency_ele'))
model.efficiency_bur = pyo.Param(initialize=get_efficiency('efficiency_bur'))
model.loh_ht = pyo.Param(initialize=get_efficiency('loh_ht'))
model.thermal_load = pyo.Param(model.t, initialize=get_thermal_load(thermal_load))

model.perc_max_ele = pyo.Param(initialize=get_contstraint_ele('perc_max_ele'))
model.perc_min_ele = pyo.Param(initialize=get_contstraint_ele('perc_min_ele'))
model.perc_max_bur = pyo.Param(initialize=get_contstraint_bur('perc_max_bur'))
model.perc_min_bur = pyo.Param(initialize=get_contstraint_bur('perc_min_bur'))
model.perc_max_ht = pyo.Param(initialize=get_contstraint_ht('perc_max_ht'))
model.perc_min_ht = pyo.Param(initialize=get_contstraint_ht('perc_min_ht'))

model.CAPEX_ele = pyo.Param(initialize=get_CAPEX('CAPEX_ele'))
model.CAPEX_bur = pyo.Param(initialize=get_CAPEX('CAPEX_bur'))
model.OPEX_ele = pyo.Param(initialize=get_OPEX('OPEX_ele'))
model.OPEX_bur = pyo.Param(initialize=get_OPEX('OPEX_bur'))
model.cost_energy_grid = pyo.Param(initialize=get_cost_energy('cost_energy_grid'))
model.CAPEX_pv = pyo.Param(initialize=get_CAPEX('CAPEX_pv'))
model.OPEX_pv = pyo.Param(initialize=get_OPEX('OPEX_pv'))
model.CAPEX_cp = pyo.Param(initialize=get_CAPEX('CAPEX_cp'))
model.OPEX_cp = pyo.Param(initialize=get_OPEX('OPEX_cp'))
model.CAPEX_ht = pyo.Param(initialize=get_CAPEX('CAPEX_ht'))
model.OPEX_ht = pyo.Param(initialize=get_OPEX('OPEX_ht'))

## Model VARIABLE
model.power_pv = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_grid = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.power_in_ele = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_ele = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_ele_bur = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.power_in_cp = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_ele_cp = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.capacity_ht = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_in_ht = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_ht = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.power_in_bur = pyo.Var(model.t, within=pyo.NonNegativeReals)
model.power_out_bur = pyo.Var(model.t, within=pyo.NonNegativeReals)

model.power_rated_ele = pyo.Var(within=pyo.NonNegativeReals)
model.power_rated_bur = pyo.Var(within=pyo.NonNegativeReals)
model.power_rated_cp = pyo.Var(within=pyo.NonNegativeReals)
model.capacity_rated_ht = pyo.Var(within=pyo.NonNegativeReals)
model.cap_installed = pyo.Var(within=pyo.NonNegativeReals)


## Model COSTRAINTS
# constraint at POWER PV
def constraint_power_pv(xx, t):
    return xx.power_pv[t] <= xx.cap_installed*xx.list_pv[t]
model.constr_power_pv = pyo.Constraint(model.t, rule=constraint_power_pv)

# constraint at NODE 1
def constraint_n1(xx, t):
    return xx.power_pv[t] + xx.power_grid[t] == xx.power_in_ele[t] + xx.power_in_cp[t]
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
    return xx.power_out_ele[t] == xx.power_out_ele_cp[t] + xx.power_out_ele_bur[t]
model.constr_n2 = pyo.Constraint(model.t, rule=constraint_n2)

# constraint at COMPRESSOR
def constraint_compressor_work(xx, t):
    return xx.power_in_cp[t] <= xx.power_out_ele_cp[t]*xx.compression_work/xx.LHV
model.constr_compressor_work = pyo.Constraint(model.t, rule=constraint_compressor_work)

def constraint_equilibrium_cp(xx, t):
    return xx.power_out_ele_cp[t] == xx.power_in_ht[t]
model.constr_equilibrium_cp = pyo.Constraint(model.t, rule=constraint_equilibrium_cp)

# constraint at HYDROGEN TANK
def constraint_equilibrium_ht(xx, t):
    if t == 0:
        return xx.capacity_ht[t] == xx.capacity_ht[time_vec[-1]] + xx.power_in_ht[t]*xx.delta_t - xx.power_out_ht[t]*xx.delta_t
    else:
        return xx.capacity_ht[t] == xx.capacity_ht[t-1] + xx.power_in_ht[t]*xx.delta_t - xx.power_out_ht[t]*xx.delta_t
model.constr_equilibrium_ht = pyo.Constraint(model.t, rule=constraint_equilibrium_ht)

def constraint_initial_ht(xx):
        return xx.capacity_ht[0] == xx.capacity_rated_ht*xx.loh_ht
model.constr_initial_ht = pyo.Constraint(rule=constraint_initial_ht)

def constraint_max_capacity_ht(xx, t):
    return xx.capacity_ht[t] <= xx.capacity_rated_ht*xx.perc_max_ht
model.constr_max_capacity_ht = pyo.Constraint(model.t, rule=constraint_max_capacity_ht)

def constraint_min_capacity_ht(xx, t):
    return xx.capacity_ht[t] >= xx.capacity_rated_ht*xx.perc_min_ht
model.constr_min_capacity_ht = pyo.Constraint(model.t, rule=constraint_min_capacity_ht)

# constraint at NODE 3
def constraint_n3(xx, t):
    return xx.power_out_ele_bur[t] + xx.power_out_ht[t] == xx.power_in_bur[t]
model.constr_n3 = pyo.Constraint(model.t, rule=constraint_n3)

# constraint at BURNER POWER
def constraint_max_power_bur(xx, t):
    return xx.power_in_bur[t] <= xx.power_rated_bur*xx.perc_max_bur
model.constr_max_power_bur = pyo.Constraint(model.t, rule=constraint_max_power_bur)

def constraint_min_power_bur(xx, t):
    return xx.power_in_bur[t] >= xx.power_rated_bur*xx.perc_min_bur
model.constr_min_power_bur = pyo.Constraint(model.t, rule=constraint_min_power_bur)

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
    C_npc_CAPEX = xx.power_rated_ele*xx.CAPEX_ele + xx.power_rated_bur*xx.CAPEX_bur + xx.power_rated_cp*xx.CAPEX_cp + xx.capacity_rated_ht*xx.CAPEX_ht
    C_npc_OPEX = xx.power_rated_ele*xx.OPEX_ele + xx.power_rated_bur*xx.OPEX_bur + xx.power_rated_cp*xx.OPEX_cp + xx.capacity_rated_ht*xx.OPEX_ht

    C_electricity_grid = sum(xx.power_grid[t]*xx.cost_energy_grid for t in list_time)
    C_electricity_pv = xx.cap_installed*xx.CAPEX_pv + xx.cap_installed*xx.OPEX_pv*xx.life

    C_npc_TOT = C_npc_CAPEX + C_npc_OPEX*xx.life + C_electricity_grid*xx.life + C_electricity_pv

    return C_npc_TOT
model.func_obj = pyo.Objective(rule=func_object, sense=pyo.minimize)


## OPTIMIZATION SOLVING
instance = model.create_instance()
opt = pyo.SolverFactory('glpk')
results = opt.solve(instance)
results.write()

post_processing(instance,time_vec)