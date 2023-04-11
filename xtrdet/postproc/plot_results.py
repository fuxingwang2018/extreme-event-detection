import numpy as np
from xtrdet.postproc import plot_map
from xtrdet.postproc import fig_parameters
from xtrdet.postproc import get_colorscale
import xarray as xa

def map_extreme_detected(var_name, extreme_dectedted, extreme_type, map_configuration, outdir):
    """
    Plot extreme event dection results
    Args:

    Returns:
    """
    #extreme_dectedted = xa.open_dataset(outdir + '/target.norcp12_ald.pr_climtlgy.norcp12_ald.pr.South_Sweden_threshold_optim.nc')

    ndim_time = extreme_dectedted.dims['time']

    var_name_to_plot = [var_name, f'{var_name}_threshold_detections']
    nsubplot = len(var_name_to_plot)

    map_parameters = {}
    scale = {}
    get_cscale = get_colorscale.GetColorScale()
    for var in var_name_to_plot:
        scale[var] = get_cscale.get_scale(extreme_dectedted[var], centered=False)
        map_parameters[var] = fig_parameters.get_map_parameters(var)

    for idim_time in range(ndim_time):

        plotmap = plot_map.PlotMap( \
            map_configuration['proj'], \
            map_configuration['res'], \
            map_configuration['zoom_geom'][0], \
            map_configuration['zoom_geom'][1], \
            map_configuration['lat_0'], \
            map_configuration['lon_0'], \
            nsubplot = nsubplot)

        for isubplot in range(nsubplot):
            var = var_name_to_plot[isubplot]
            fig_title = fig_parameters.get_fig_title(var, extreme_dectedted['time'][idim_time].values)
            print('fig_title:', fig_title)

            plotmap.plot_2dfield( \
                extreme_dectedted['lat'].values, \
                extreme_dectedted['lon'].values, \
                extreme_dectedted[var].isel(time=slice(idim_time, idim_time + 1)).squeeze("time"), \
                scale[var]['scale_min'], \
                scale[var]['scale_max'], \
                fig_title[var], \
                map_parameters[var]['cmap'], \
                map_parameters[var]['fontsize'], \
                isubplot + 1)

            plotmap.plot_colorbar(\
                map_parameters[var]['label_colorbar'], \
                map_parameters[var]['extend'], \
                isubplot + 1)

        plotmap.plot_save( \
            outdir + '/' + \
            map_parameters[var_name]['fig_name'] + '_' +  \
            str(idim_time) + \
            map_parameters[var_name]['fig_type'] )
