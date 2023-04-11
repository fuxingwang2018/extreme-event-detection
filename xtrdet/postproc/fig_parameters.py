from matplotlib import colors

def get_map_parameters(var):

    map_parameters = {}

    label_colorbar = {
        'tas': 'Temperature (K)', 
         'pr': 'Precipitation (kg m-2 s-1)',
         'pr_threshold_detections': 'Boolean: 0-no extreme, 1-extreme'
         }

    extend = {
        'tas': 'both', 
        'pr': 'max', 
        'pr_threshold_detections': 'neither'
        }

    cmap = {
        'tas': 'OrRd', 
        'pr': 'viridis', 
        'pr_threshold_detections': colors.ListedColormap(['white', 'red'])
        }

    fig_name = {
        'tas': 'heatwave',
        'pr': 'extreme_precipitation',
        'pr_threshold_detections': 'extreme_precipitation',
        }
 
    map_parameters['fig_type'] = '.png'
    map_parameters['extend'] = extend[var]
    map_parameters['fontsize'] = 9
    map_parameters['label_colorbar'] = label_colorbar[var]
    map_parameters['cmap'] = cmap[var]
    map_parameters['fig_name'] = fig_name[var]

    return map_parameters


def get_fig_title(var, title_suffix):

    fig_title = {
        'tas': 'tas at ' + str(title_suffix), 
        'pr': 'precipitation at ' + str(title_suffix), 
        'pr_threshold_detections': 'Extreme event detected',
        }

    return fig_title
