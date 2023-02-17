
from plot_map import PlotMap
import fig_parameters
import numpy as np

def map_extreme_detected(data_for_detection, extreme_dectedted, map_configuration, outdir):

    number_of_extreme_grids = extreme_dectedted['statistics_for_extremes']['number_of_extreme_grids']
    accumulated_extreme_values = extreme_dectedted['statistics_for_extremes']['accumulated_extreme_values']
    extremes_filtered = extreme_dectedted['statistics_for_extremes']['extremes_filtered']

    map_parameters = fig_parameters.get_map_parameters('tas', 'map_ref')

    data_to_plot = {}
    data_to_plot['data_for_detection'] = np.nanmean(data_for_detection['tas'], axis = 0)
    data_to_plot['extremes_filtered']  = np.nanmean(extremes_filtered, axis = 0)
    nsubplot = len(data_to_plot)

    plotmap = PlotMap( \
        map_configuration['proj'], \
        map_configuration['res'], \
        map_configuration['zoom_geom'][0], \
        map_configuration['zoom_geom'][1], \
        map_configuration['lat_0'], \
        map_configuration['lon_0'], \
        nsubplot = 2)

    isubplot = 0
    for key, value in data_to_plot.items():
        isubplot += 1
        plotmap.plot_2dfield( \
            data_for_detection['latitude'], \
            data_for_detection['longitude'], \
            data_to_plot[key], \
            map_parameters['scale_min'], \
            map_parameters['scale_max'], \
            map_parameters['fig_title'], \
            map_parameters['cmap'], \
            map_parameters['fontsize'], \
            isubplot)

    plotmap.plot_colorbar(\
        map_parameters['label_colorbar'], \
        map_parameters['extend'])

    plotmap.plot_save( outdir + '/' + map_parameters['fig_name'] + map_parameters['fig_type'])


