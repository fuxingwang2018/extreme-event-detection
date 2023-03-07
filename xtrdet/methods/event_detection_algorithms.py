import sys


class ExtremeDetectionAlgorithm(object):

    """
    Basic algorithms include:
        - Threshold Based (TB)
    Sophisticated algorithms include:
        - Circulation Pattern based (CP)
        - Machine Learning based (ML)

    """

    def __init__(self, algorithm, algorithm_args,
                 climatology_data, cl_var_in, target_data, tg_var_in):

        self.algorithm = algorithm
        self.args = algorithm_args
        self.clim_data = climatology_data
        self.cl_var_in = cl_var_in
        self.trgt_data = target_data
        self.tg_var_in = tg_var_in

    def update_method_args(self, arg, value):
        self.args[arg] = value

    def run_algorithm(self):
        method_funcs = {
            'threshold_optim': self.threshold_optim,
            'machine_learning_based_algorithm':
            self.machine_learning_based_algorithm
        }

        algorithm_computation = method_funcs[self.algorithm](
            self.clim_data, self.trgt_data, self.cl_var_in, self.tg_var_in,
            self.args)

        return algorithm_computation

    def threshold_optim(self, cdata, tdata, cl_variable, tg_variable,
                        funcargs):
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
            cl_variable:
                Climatology Input variable
            tg_variable:
                Target Input variable
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
        perc_of_days = funcargs['top select percentage']

        if len(cdata.chunks['time']) > 1:
            cdata = cdata.chunk({'time': -1})

        if pctl_dim == 'all':
            thr_clim = cdata.quantile(pctl/100)
        elif pctl_dim == 'time':
            thr_clim = cdata.quantile(pctl/100, dim='time')

        mask = tdata[tg_variable] >= thr_clim
        mask = mask.transpose("time", ...)
        trgt_thr_pass = tdata.where(mask, tdata)

        if filter_method == 'field sum':
            stat_daily = trgt_thr_pass.sum(dim=('x', 'y'))
        elif filter_method == 'field count':
            stat_daily = trgt_thr_pass.count(dim=('x', 'y'))
        else:
            sys.exit('filter_method not defined')

        selected_days = stat_daily.sortby(tg_variable, ascending=False).isel(
            time=slice(0, int((perc_of_days/100)*stat_daily.time.size))).time

        passed_thresholds = mask.sel(time=selected_days).rename(
            {tg_variable: f'{tg_variable}_threshold_detections'})
        days_of_extreme = tdata.sel(time=selected_days)

        ds_out = days_of_extreme.merge(passed_thresholds, compat='override')
        return ds_out

    def machine_learning_based_algorithm(self):

        pass
