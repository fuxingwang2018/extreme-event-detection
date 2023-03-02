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
                 climatology_data, target_data, var_in):

        self.algorithm = algorithm
        self.args = algorithm_args
        self.clim_data = climatology_data
        self.trgt_data = target_data
        self.var_in = var_in

    def update_method_arg(self, arg, value):
        self.args[arg] = value

    def run_algrithm(self):
        method_funcs = {
            'threshold_optim': self.threshold_optim,
            'machine_learning_based_algorithm':
            self.machine_learning_based_algorithm
        }

        algorithm_computation = method_funcs[self.algorithm](
            self.clim_data, self.trgt_data, self.var_in, self.args)

        return algorithm_computation

    def threshold_optim(self, cdata, tdata, variable, funcargs):
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
        perc_of_days = funcargs['top select percentage']

        thr_clim = cdata.quantile(pctl/100)

        trgt_thr_pass = tdata.where(
            tdata[variable] >= thr_clim, tdata)

        if filter_method == 'field sum':
            stat_daily = trgt_thr_pass.sum(dim=('x', 'y'))
        elif filter_method == 'field count':
            stat_daily = trgt_thr_pass.count(dim=('x', 'y'))
        else:
            sys.exit('filter_method not defined')

        selected_days = stat_daily.sortby(variable, ascending=False).isel(
            time=slice(0, int((perc_of_days/100)*stat_daily.time.size))).time

        days_of_extreme = tdata.sel(time=selected_days)
        return days_of_extreme

    def machine_learning_based_algorithm(self):

        pass
