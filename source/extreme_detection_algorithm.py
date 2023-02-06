import os, sys
import numpy as np
import numpy.ma as ma
sys.path.insert(0, '..')
from utils import statistics

class ExtremeDetectionAlgorithm(object):

    """
    Basic algorithms include:
        - Threshold Based (TB)
    Sophisticated algorithms include:
        - Circulation Pattern based (CP)
        - Machine Learning based (ML)

    """

    def __init__(self, var_in):
        #self.algorithm = algorithm
        self.var_in = var_in


    def threshold_based_algorithm(self, filter_method, pctl_threshold, perc_of_days):
        """
        Detection of extreme convective precipitation events from a coarse model (e.g. GCM)

        :param pctl_threshold: Pre-defined N-th percentile (e.g. N = 95) for the entire chosen (sub)domain and time period
        :type pctl_threshold: integer
        :param perc_of_days: Percentage (e.g. 10%) of the days with the largest cr_sum as the potential events of interest (extreme events) to downscale them
        :type perc_of_days: integer
        :return: days_of_extreme.
        :rtype: True/False masked array.

        """

        assert pctl_threshold > 0.0, "ERROR: negative pctl_threshold"
        assert perc_of_days > 0.0,   "ERROR: negative perc_of_days"

        # Finds candidate extreme events at each grid point and day as values larger than the threshold 
        var_pctl = (self.var_in >= np.percentile(self.var_in, pctl_threshold))

        statis = statistics.Statistics(self.var_in)
        statistics_daily = statis.get_statistics_daily(filter_method, var_pctl)

        days_of_extreme = (statistics_daily >= np.percentile(statistics_daily, 100 - perc_of_days))

        return days_of_extreme


    def machine_learning_based_algorithm(self):

        pass
