import pandas

"Import and introducing data"

list_time = list(range(365*24))                                                         # [h]
time_step = list_time[1] - list_time[0]                                                 # [h]   ##################################################################
life = 25                                                                               # [years] lifetime of the plant
LHV = 33.33                                                                             # [kWh/kg]
h2_density = 0.0899                                                                     # [kg/m3]
flow_rate_m3 = 500                                                                      # [Nm3/h]
flow_rate = flow_rate_m3 / 3600 * h2_density                                            # [kg/s]

import_PV_supply = pandas.read_excel("pv_supply_barcelona_1kwp.xlsx", sheet_name='pv_supply_barcelona_1kwp', header=None, index_col=None)

efficiency_ele = 0.80                                                                   # [-] https://www.iea.org/reports/electrolysers and H2GLASS
efficiency_bur = 0.75                                                                   # [-] https://thermalprocessing.com/high-efficiency-gas-burners-make-good-economic-sense/ @1300°C and eta=0.8
loh_ht = 0.75                                                                           # [-] ##################################################################
thermal_load = 42.2*52*1000        #### DA MODIFICARE                                   # [kW] waiting for the H2GLASS value [average kW/week]*[week/year]
compression_work = 1000            #### DA MODIFICARE                                   # [kWh] DA MODIFICARE

perc_max_ele = 0.8                                                                       # [-]
perc_min_ele = 0                                                                         # [-]
perc_max_bur = 0.95                                                                      # [-]
perc_min_bur = 0                                                                         # [-]
perc_max_ht = 0.95                                                                       # [-]   ##################################################################
perc_min_ht = 0                                                                          # [-]   ##################################################################

CAPEX_ele = 1000                                                                        # [USD/kWe/year]  https://www.iea.org/reports/electrolysers
CAPEX_bur = CAPEX_ele*0.05

OPEX_ele = 13.6                                                                         # [USD/kWe/year]  https://www.iea.org/reports/electrolysers
OPEX_bur = OPEX_ele*0.05                                                                # [USD/kWe/year]  https://it.scribd.com/document/514697464/COSTOS-DETALLADO-CAPEX-2019-PLANTA-CALLAO

CAPEX_pv = 1000                                                                        # [USD/kWe/year]  https://www.iea.o
OPEX_pv = OPEX_ele*0.05                                                                # [USD/kWe/year]  https://it.scribd.com/document/514697464/COSTOS-DETALLADO-CAPEX-2019-PLANTA-CALLAO

CAPEX_cp = 1000                                                                        # [USD/kWe/year]
OPEX_cp = OPEX_ele*0.05                                                                # [USD/kWe/year]

CAPEX_ht = 1000                                                                        # [USD/kWe/year]  ##################################################################
OPEX_ht = OPEX_ele*0.05                                                                # [USD/kWe/year]  ##################################################################
cost_energy_grid = 0.2477                                                                # [€/kWh*h] https://electricityinspain.com/electricity-prices-in-spain/ in 2018



"Pre-processing"
list_pv = list(range(1, import_PV_supply.shape[1]))                                     # list of PV data and dimension

def get_l(xx):
    if xx == 'list_time':
        return list_time
    if xx == 'time_step':
        return time_step
    if xx == 'time_vec':
        return list_time

def get_pv():
    return import_PV_supply

def dict_Forecast(xx):
    dict_Forecast = {t: xx.iloc[4+t, 2] for t in list_time}
    return dict_Forecast

def get_prop(xx):
    if xx == 'life':
        return life
    if xx == 'LHV':
        return LHV
    if xx == 'h2_density':
        return h2_density
    if xx == 'compression_work':
        return compression_work
    else:
        return

def get_flow_rate(xx):
    if xx == 'flow_rate':
        return flow_rate
    else:
        return

def get_efficiency(xx):
    if xx == 'efficiency_ele':
        return efficiency_ele
    if xx == 'efficiency_bur':
        return efficiency_bur
    if xx == 'loh_ht':
        return loh_ht
    else:
        return

def get_thermal_load(thermal_load):
    dict_load = {t: thermal_load for t in list_time}
    return dict_load

def get_contstraint_ele(xx):
    if xx == 'perc_max_ele':
        return perc_max_ele
    if xx == 'perc_min_ele':
        return perc_min_ele
    else:
        return

def get_contstraint_bur(xx):
    if xx == 'perc_max_bur':
        return perc_max_bur
    if xx == 'perc_min_bur':
        return perc_min_bur
    else:
        return

def get_contstraint_ht(xx):
    if xx == 'perc_max_ht':
        return perc_max_ht
    if xx == 'perc_min_ht':
        return perc_min_ht
    else:
        return

def get_CAPEX(xx):
    if xx == 'CAPEX_ele':
        return CAPEX_ele
    if xx == 'CAPEX_bur':
        return CAPEX_bur
    if xx == 'CAPEX_pv':
        return CAPEX_pv
    if xx == 'CAPEX_cp':
        return CAPEX_cp
    if xx == 'CAPEX_ht':
        return CAPEX_ht
    else:
        return

def get_OPEX(xx):
    if xx == 'OPEX_ele':
        return OPEX_ele
    if xx == 'OPEX_bur':
        return OPEX_bur
    if xx == 'OPEX_pv':
        return OPEX_pv
    if xx == 'OPEX_cp':
        return OPEX_cp
    if xx == 'OPEX_ht':
        return OPEX_ht
    else:
        return

def get_cost_energy(xx):
    if xx == 'cost_energy_grid':
        return cost_energy_grid
    else:
        return



