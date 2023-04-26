import pandas

"Import and introducing data"

list_time = list(range(365*24))                                                         # [h]
life = 25                                                                               # [years] lifetime of the plant
LHV = 33.33                                                                             # [kWh/kg]
h2_density = 0.0899                                                                     # [kg/m3]
flow_rate_m3 = 500                                                                      # [Nm3/h]
flow_rate = flow_rate_m3 / 3600 * h2_density                                            # [kg/s]

import_PV_supply = pandas.read_excel("pv_supply_barcelona_1kwp.xlsx", sheet_name='pv_supply_barcelona_1kwp', header=None, index_col=None)

efficiency_ele = 0.80                                                                   # [-] https://www.iea.org/reports/electrolysers and H2GLASS
efficiency_bur = 0.75                                                                   # [-] https://thermalprocessing.com/high-efficiency-gas-burners-make-good-economic-sense/ @1300°C and eta=0.8
cap_installed = 1                  #### DA MODIFICARE                                   # [KWpeak]
thermal_load = 42.2*52*1000        #### DA MODIFICARE                                   # [kW] waiting for the H2GLASS value [average kW/week]*[week/year]

max_power_ele = 10_000_000                                                                  # [kW]
max_power_bur = 10_000_000                                                                  # [kW]
min_power_ele = 0                                                                           # [kW]
min_power_bur = 0                                                                           # [kW]

CAPEX_ele = 1000                                                                        # [USD/kWe/year]  https://www.iea.org/reports/electrolysers
CAPEX_bur = CAPEX_ele*0.05
#max_Power = max(power_time.values())                                                   # [kW] max value of power

OPEX_ele = 13.6                                                                         # [USD/kWe/year]  https://www.iea.org/reports/electrolysers
OPEX_bur = OPEX_ele*0.05                                                                # [USD/kWe/year]  https://it.scribd.com/document/514697464/COSTOS-DETALLADO-CAPEX-2019-PLANTA-CALLAO

cost_energy = 0.2477              #### DA CONVERTIRE                                    # [€/kWh] https://electricityinspain.com/electricity-prices-in-spain/ in 2018



"Pre-processing"
list_pv = list(range(1, import_PV_supply.shape[1]))                                     # list of PV data and dimension

def get_l(xx):
    if xx == 'list_time':
        return list_time

def dict_Forecast(xx):
    dict_Forecast = {t: xx.iloc[t, 1] for t in list_time}
    return dict_Forecast

def get_prop(xx):
    if xx == 'lifee':
        return life
    if xx == 'LHV':
        return LHV
    if xx == 'h2_density':
        return h2_density
    else:
        return

def get_flow_rate(xx):
    if xx == 'flow_rate':
        return flow_rate
    else:
        return

def get_max(xx):
    if xx == 'max_power_ele':
        return max_power_ele
    if xx == 'max_power_bur':
        return max_power_bur
    else:
        return

def get_min(xx):
    if xx == 'min_power_ele':
        return min_power_ele
    if xx == 'min_power_bur':
        return min_power_bur
    else:
        return

def get_efficiency(xx):
    if xx == 'efficiency_ele':
        return efficiency_ele
    if xx == 'efficiency_bur':
        return efficiency_bur
    else:
        return

def get_cap_installed(xx):
    if xx == 'cap_installed':
        return cap_installed
    else:
        return

def get_thermal_load(xx):
    dict_load = {t: xx.iloc[t, 1] for t in list_time}
    return dict_load

def get_CAPEX(xx):
    if xx == 'CAPEX_ele':
        return CAPEX_ele
    if xx == 'CAPEX_bur':
        return CAPEX_bur
    else:
        return

def get_OPEX(xx):
    if xx == 'OPEX_ele':
        return OPEX_ele
    if xx == 'OPEX_bur':
        return OPEX_bur
    else:
        return

def get_cost_energy(xx):
    if xx == 'cost_energy':
        return cost_energy
    else:
        return



