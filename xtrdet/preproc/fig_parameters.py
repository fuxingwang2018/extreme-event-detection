
# define parameters here

def get_map_parameters(plot_var, plot_type):

    map_parameters = {}
    label_colorbar = {'tas': 'Temperature (K)'}

    map_parameters['fig_type'] = '.png'
    map_parameters['extend'] = 'both'
    map_parameters['fontsize'] = 9
    map_parameters['label_colorbar'] = label_colorbar[plot_var]
    map_parameters['scale_min'] = 285
    map_parameters['scale_max'] = 295
    map_parameters['cmap'] = 'OrRd'
    map_parameters['fig_title'] = ''
    map_parameters['fig_name'] = str(plot_var) + '_' + str(plot_type)

    return map_parameters

