# we extract results

# from pre_processing import *
# from main import *
import pandas

def post_processing(instance,time_vec):

    power_pv = instance.power_pv.get_values()
    power_grid = instance.power_grid.get_values()

    power_rated_ele = instance.power_rated_ele.get_values()[None]

    # time dependent
    dict_col = {}
    dict_col['list_pv [kW]'] = list(power_pv.values())        #Excel column called 'list_pv [kW]' with values dict_PV at each time
    dict_col['list_grid [kW]'] = list(power_grid.values())
    table_h_general = pandas.DataFrame(dict_col, index=time_vec)

    #single values
    dict_sizing = {'Value':[power_rated_ele]}
    names_sizing = ['P_PV [kW]']
    table_sizing = pandas.DataFrame(dict_sizing, index=names_sizing)

    with pandas.ExcelWriter('results/' + 'Results.xlsx') as writer:
        table_h_general.to_excel(writer, sheet_name='Time_dependent')
        table_sizing.to_excel(writer, sheet_name='Sizing')

    return


