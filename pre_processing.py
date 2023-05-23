import pandas

"Import and introducing data"

list_time = list(range(365*24))                                                         # [h]
time_step = list_time[1] - list_time[0]                                                 # [h]
life = 20                                                                               # [years] lifetime of the plant
LHV = 33.33                                                                             # [kWh/kg]
h2_density = 0.0899                                                                     # [kg/m3]
water_density = 1000                                                                    # [kg/m3]
flow_rate_m3 = 420                                                                      # [Nm3/h] (500 said Eduardo) but 420 from https://www.h-tec.com/fileadmin/user_upload/produkte/produktseiten/HCS/spec-sheet/H-TEC-Datenblatt-HCS-EN-23-03.pdf
flow_rate = flow_rate_m3 / 3600 * h2_density                                            # [kg/s]

import_PV_supply = pandas.read_excel("pv_supply_barcelona_1kwp.xlsx", sheet_name='pv_supply_barcelona_1kwp', header=None, index_col=None)

efficiency_ele = 0.75                                                                   # [-] H-TEC SYSTEMS PEM Electrolyzer: Hydrogen Cube System and H2GLASS
efficiency_bur = 0.75                                                                   # [-] https://thermalprocessing.com/high-efficiency-gas-burners-make-good-economic-sense/ @1300°C and eta=0.8
loh_ht = 0.75                                                                           # [-] [??????????????????????????]
thermal_load = 42.2 * 1000 / 7 / 24                                                     # [kW] waiting for the H2GLASS value [average kW/week]*[week/year]
specific_work_cp = 4                                                                    # [MJ/kgH2]
compression_work = specific_work_cp * 1000 / 3600 * flow_rate * 3600                    # [kWh] = [MJ/kgH2] * [kJ/MJ] * [kWh/kJ] * [kgH2/s] * [s]
capacity_volume_bo = 850                                                                # [liters] https://www.mahytec.com/wp-content/uploads/2021/03/CL-DS10-Data-sheet-60bar-850L-EN.pdf
capacity_rated_bo = capacity_volume_bo / 1000 * h2_density * LHV                        # [kWh] = [litri] * [m3/l] * [kg/s] * [kWh/kg]

perc_max_ele = 1                                                                        # [-] Marocco Gandiglio
perc_min_ele = 0.1                                                                      # [-] Marocco Gandiglio
perc_max_bur = 1                                                                        # [-] Marocco Gandiglio
perc_min_bur = 0                                                                        # [-] Marocco Gandiglio
perc_max_ht = 0.95                                                                       # [-] [??????????????????????????]
perc_min_ht = 0                                                                          # [-] [??????????????????????????]

CAPEX_ele = 1188                                                                        # [€/kWe/year]  https://www.iea.org/reports/electrolysers + Marocco Gandiglio
OPEX_ele = 15.84                                                                        # [€/kWe/year]  Marocco Gandiglio

CAPEX_bur = 63.32                                                                       # [€/kWth/year]  Marocco Gandiglio
OPEX_bur = CAPEX_bur*0.05                                                               # [€/kWth/year]  Marocco Gandiglio

CAPEX_pv_USD = 0.61                                                                     # [USD/We/year]  https://www.statista.com/statistics/971982/solar-pv-capex-worldwide-utility-scale/
CAPEX_pv = CAPEX_pv_USD / 0.92 * 1000                                                   # [€/kWe/year] = [USD/W] * [€/USD] * [W/kW]  https://www.statista.com/statistics/971982/solar-pv-capex-worldwide-utility-scale/
OPEX_pv = OPEX_ele*0.05                                                                 # [€/kWe/year]  https://it.scribd.com/document/514697464/COSTOS-DETALLADO-CAPEX-2019-PLANTA-CALLAO

CAPEX_cp = 1600                                                                         # [€/kWe/year]  Marocco Gandiglio
OPEX_cp_USD = 19                                                                        # [USD/kW] https://emp.lbl.gov/publications/benchmarking-utility-scale-pv
OPEX_cp = OPEX_cp_USD / 0.92                                                            # [€/kWe]

CAPEX_ht = 470                                                                          # [€/kgH2/year]  Marocco Gandiglio
OPEX_ht = OPEX_ele*0.02                                                                 # [€/kgH2/year]  Marocco Gandiglio

CAPEX_bo = 470                                                                          # [€/kgH2/year] [ask momo]
OPEX_bo = OPEX_ele*0.02                                                                 # [€/kgH2/year] [ask momo]

cost_energy_grid = 0.2477                                                               # [€/kWh*h] https://electricityinspain.com/electricity-prices-in-spain/ in 2018

water_flowrate_h = 600                                                                  # [kg/h] H-TEC SYSTEMS PEM Electrolyzer: Hydrogen Cube System
water_flowrate = water_flowrate_h / 3600                                                # [kg/s]
cost_water_m3 = 2                                                                       # [€/m3] https://www.waternewseurope.com/water-prices-compared-in-36-eu-cities/
cost_water_kg = 2 / water_density                                                       # [€/kg]
cost_water = cost_water_kg / flow_rate                                                  # [€/s]



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
    if xx == 'capacity_rated_bo':
        return capacity_rated_bo
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
    if xx == 'CAPEX_bo':
        return CAPEX_bo
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
    if xx == 'OPEX_bo':
        return OPEX_bo
    else:
        return

def get_cost_energy(xx):
    if xx == 'cost_energy_grid':
        return cost_energy_grid
    else:
        return



""""
something to write in the report
1) the massflow rate is 500
2) efficiencies
3) thermal load
4) 30 bar at electrolyser + 200 bar storage tank
5) INSTALLATION COSTS?
6) raga il burner cost è in €/kgH -----> I have multiplied it h2_density*3600
7) assumo bottle cost equal to tank cost
8) 20 anni lifetime
9) devo aggiungere il costo dell'acqua ???


"""