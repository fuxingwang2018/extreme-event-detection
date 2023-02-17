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

    def __init__(self, data_in):

        self.data_in = data_in


    def threshold_based_algorithm(self, statistics_configure):
        """
        Detection of extreme convective precipitation events from a coarse model (e.g. GCM)

        :param pctl_threshold: Pre-defined N-th percentile (e.g. N = 95) for the entire chosen (sub)domain and time period
        :type pctl_threshold: integer
        :param perc_of_days: Percentage (e.g. 10%) of the days with the largest cr_sum as the potential events of interest (extreme events) to downscale them
        :type perc_of_days: integer
        :return: days_of_extreme.
        :rtype: True/False masked array.

        """

        assert statistics_configure['pctl_threshold'] > 0.0, "ERROR: negative pctl_threshold"
        assert statistics_configure['perc_of_days'] > 0.0,   "ERROR: negative perc_of_days"

        extreme_detected = {}
        # Finds potential extreme events over time step as values larger than the threshold 
        statis = statistics.Statistics(self.data_in['tas'])
        threshold_for_extreme = statis.extreme_threshold( \
            statistics_configure['threshold_method'], \
            statistics_configure['pctl_threshold'])
        extreme_detected['latitude']  = self.data_in['latitude']
        extreme_detected['longitude'] = self.data_in['longitude']
        extreme_detected['statistics_for_extremes'] = statis.extreme_statistics(threshold_for_extreme)
        extreme_detected['time_period_of_extreme_triggered'] = \
            statis.extreme_triggering( \
            statistics_configure['filter_method'], \
            extreme_detected['statistics_for_extremes'], \
            statistics_configure['perc_of_days'] )
        extreme_detected['extreme_warning_level'] = \
            statis.extreme_warning(extreme_detected['statistics_for_extremes'])
        
        return extreme_detected



    def machine_learning_based_algorithm(self):

        pass


    def extreme_type(self):
        extreme_name = { \
            'tas': 'heatwave', \
            'precipitaiton': 'extreme_precipitation', \
            }
        return extreme_name

