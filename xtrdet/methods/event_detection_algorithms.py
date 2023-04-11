import sys
import numpy as np
import xarray as xa


class ExtremeDetectionAlgorithm(object):

    """
    Basic algorithms include:
        - Threshold Based (TB)
    Sophisticated algorithms include:
        - Circulation Pattern based (CP)
        - Machine Learning based (ML)

    """

    def __init__(self, data_source, algorithm, algorithm_args,
                 climatology_data, target_data, variable):

        self.data_src = data_source
        self.algorithm = algorithm
        self.args = algorithm_args
        self.clim_data = climatology_data
        self.trgt_data = target_data
        self.variable = variable

    def update_method_args(self, arg, value):
        self.args[arg] = value

    def run_algorithm(self):
        method_funcs = {
            'threshold_optim': self.threshold_optim,
            'extreme_forecast_index': self.extreme_forecast_index,
            'machine_learning_based_algorithm':
            self.machine_learning_based_algorithm
        }

        algorithm_computation = method_funcs[self.algorithm](
            self.data_src, self.clim_data, self.trgt_data, self.variable,
            self.args)

        return algorithm_computation

    def threshold_optim(self, data_src, cdata, tdata, variable, funcargs):
        """
        Detection of extreme convective precipitation events from a coarse
        model (e.g. GCM)

        STEPS:
            1.
            Find N-th percentile (xN, e.g. N = 95) of all the data in the
            climatology dataset
            2.
            For each day, find grid points with x > xN and take some measure
            ('filtering method'; e.g. 'sum') of these x values over these grid
            points -> x_measure
            3.
            Select a percentage ('top select percentage', e.g. 10%) of the
            days with the largest x_measure as the potential events of interest
            (extreme events).

        Args:
            data_src:
                Type of data
            cdata:
                Input climatology data
            tdata:
                Input target data
            variable:
                Input variable
            funcargs:
                Dictionary with 'filtering method', 'percentile threshold' and
                'top select percentage' argument settings

        Returns:
            days_of_extreme:
                Sub-selection from input target data of days with (potential)
                extremes.
        """

        # Extract arguments
        filter_method = funcargs['filtering method']
        pctl = funcargs['percentile threshold']
        pctl_dim = funcargs['percentile dimension']
        if 'top select percentage' in funcargs:
            perc_of_days = funcargs['top select percentage']

        if len(cdata.chunks['time']) > 1:
            cdata = cdata.chunk({'time': -1})

        if pctl_dim == 'all':
            thr_clim = cdata.quantile(pctl/100)
        elif pctl_dim == 'time':
            if data_src == 'ecmwf ensemble':
                thr_clim = cdata.quantile(pctl/100, dim=('time', 'n'))
            else:
                thr_clim = cdata.quantile(pctl/100, dim='time')

        mask = tdata[variable] >= thr_clim
        trgt_thr_pass = tdata.where(mask, tdata)

        if filter_method == 'field sum':
            stat_daily = trgt_thr_pass.sum(dim=('x', 'y'))
        elif filter_method == 'field count':
            stat_daily = trgt_thr_pass.count(dim=('x', 'y'))
        elif filter_method == '2d threshold fraction':
            stat_daily = tdata[variable]/thr_clim
        else:
            ermsg = f"\n\tfilter method {filter_method} is not defined"
            raise ValueError(ermsg)
            sys.exit()

        if data_src == 'ecmwf ensemble':
            day_stat = stat_daily.rename(
                {variable: f"{variable}_{filter_method.replace(' ', '_')}"})
            passed_thresholds = mask.rename(
                {variable: f"{variable}_threshold_detections"})
            ds_out = tdata.merge(passed_thresholds, compat='override').merge(
                day_stat, compat='override')
        else:
            selected_days = stat_daily.sortby(
                variable, ascending=False).isel(time=slice(
                    0, int((perc_of_days/100)*stat_daily.time.size))).time
            day_stat = stat_daily.sel(time=selected_days).rename(
                {variable: f"{variable}_{filter_method.replace(' ', '_')}"})
            passed_thresholds = mask.sel(time=selected_days).rename(
                {variable: f"{variable}_threshold_detections"})
            days_of_extreme = tdata.sel(time=selected_days)
            ds_out = days_of_extreme.merge(passed_thresholds,
                                           compat='override')

        return ds_out

    def extreme_forecast_index(self, data_src, cdata, tdata, variable,
                               funcargs):
        """
        Calculation of Extreme Forecast Index, EFI
        ECMWF EFI documentation:
            https://confluence.ecmwf.int/display/FUG/Extreme+Forecast+Index+-+EFI

        Args:
            data_src:
                Type of data
            cdata:
                Input climatology data
            tdata:
                Input target data
            variable:
                Input variable
            funcargs:
                Dictionary with 'filtering method', 'percentile threshold' and
                'top select percentage' argument settings

        Returns:
            efi_out:
                The EFI values
        """

        # For now EFI only applies to ECMWF ENS data
        ermsg = "EFI calculation only applies to 'ecmwf ensemble' data source"
        assert data_src == 'ecmwf ensemble', ermsg

        # Extract arguments
        self.quantiles = funcargs['quantiles']
        self.dquantile = self.quantiles[1] - self.quantiles[0]

        if len(cdata.chunks['time']) > 1:
            cdata = cdata.chunk({'time': -1})

        quantiles_climate = cdata.quantile(
            self.quantiles, dim=["n", "time"])
        quantiles_ensemble = tdata.quantile(self.quantiles, dim=["n"])

        clim_bins = quantiles_climate["quantile"].astype(np.float32)
        ens_bins = quantiles_ensemble.isel(time=0)["quantile"].\
            astype(np.float32)

        efi_val = xa.apply_ufunc(
            self.efi_func,
            quantiles_climate.astype(np.float32),
            quantiles_ensemble.astype(np.float32),
            clim_bins, ens_bins,
            input_core_dims=[["quantile"], ["quantile"],
                             ["quantile"], ["quantile"]],
            dask='parallelized', vectorize=True)

        efi_out = efi_val.rename({variable: "efi"})

        return efi_out

    def efi_func(self, quantiles_clim, quantiles_ens, cbins, ebins):
        dq = self.dquantile
        quantiles_clim = quantiles_clim[1:-1]
        quantiles_ens = quantiles_ens[:-1]
        cbins = cbins[1:-1]
        inds = np.searchsorted(quantiles_ens, quantiles_clim)
        efi = 2/np.pi*((cbins - ebins[inds])/np.sqrt(cbins*(1-cbins))*dq).sum()
        return efi

    def machine_learning_based_algorithm(self):

        pass
