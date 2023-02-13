
import numpy as np
import numpy.ma as ma
import sys
import warnings
import pandas as pd
import scipy.stats as stats
#from utils import tools
import random 


class Statistics(object):

    def __init__(self, var_ref):

        self.var_ref = var_ref


    def extreme_threshold(self, threshold_method, pctl_threshold):
        """
        Calculate the threshold values over each pixel for extreme.

        :param threshold_method: Options for different methods to calculate threshold values
        :type file_in: string
        :param pctl_threshold: Pre-defined N-th percentile (e.g. N = 95) for the entire chosen (sub)domain and time period
        :type pctl_threshold: integer
        :return: thresholds for triggering extremes
        :rtype: array
        """

        if threshold_method == 'percentile':
            threshold_for_extreme = np.percentile(self.var_ref, pctl_threshold)
        elif threshold_method == 'climatology':
            pass

        return threshold_for_extreme


    def extreme_statistics(self, threshold_for_extreme): 
        """
        Calculate weather statistics.

        :param threshold_for_extreme:  The threshold for extreme (N-th percentile (e.g. N = 95)) over each grid
        :type threshold_for_extreme: 2-D array
        :return: potential_extreme_over_time, weather statistics for each time step
        :rtype: 1-D array (time)
        """

        extreme_grids_mask = (self.var_ref >= threshold_for_extreme)
        extremes_filtered = ma.masked_array(self.var_ref, ~extreme_grids_mask)
        # For each day, find grid points with var_ref > threshold_for_extreme and adds them together to get a single value over the (sub)domain for all grid points
        accumulated_extreme_values = np.sum(extremes_filtered, axis = (1,2) if self.var_ref.ndim == 3 else 1)
        number_of_extreme_grids = np.sum(extreme_grids_mask, axis = (1,2))
        statistics_for_extremes = {
            'number_of_extreme_grids':    number_of_extreme_grids,
            'accumulated_extreme_values': accumulated_extreme_values}

        return statistics_for_extremes


    def extreme_triggering(self, filter_method, statistics_for_extremes, perc_of_time_periods): 
        """
        Extreme triggering by different statistics.

        :param filter_method: percentile or number
        :type filter_method: string
        :param statistics_for_extremes: statistics of weather
        :type statistics_for_extremes: array
        :param perc_of_time_periods: Percentage (e.g. 10%) of the days with the largest cr_sum as the potential events of interest (extreme events) to downscale them
        :type perc_of_time_periods: integer
        :return: time_period_of_extreme_triggered, time period with extremes
        :rtype: 1-D array (time)
        """

        if filter_method == 'percentile':
            statistics = statistics_for_extremes['accumulated_extreme_values']
        elif filter_method == 'number':
            statistics = statistics_for_extremes['number_of_extreme_grids']
        else:
            sys.exit('filter_method not defined')

        mask_of_extreme_time_period = (statistics >= np.percentile(statistics, 100 - perc_of_time_periods))
        time_period_of_extreme_triggered = np.where(mask_of_extreme_time_period)[0] + 1

        return time_period_of_extreme_triggered


    def extreme_warning(self, statistics_for_extremes): 
        """
        Issue extreme warning with different warning levels.

        :param statistics_for_extremes: statistics of weather
        :type statistics_for_extremes: dictionary
        :return: extreme_warning_levels
        :rtype: 1-D array (string)
        """

        KELVIN = 273.15
        extreme_warning_level = []
        category_warning_levels = {
           'extreme_value': {40:'High', 35:'Medium', 30:'Low'}, 
           'percent_number_grids': {50:'High', 30:'Medium', 10:'Low'} }
        if self.var_ref.ndim >= 2:
            total_grids = len(self.var_ref[0]) * len(self.var_ref[0][0])
        else:
            total_grids = len(self.var_ref[0])

        percent_of_grids = statistics_for_extremes['number_of_extreme_grids'] / total_grids * 100
        extreme_value    = statistics_for_extremes['accumulated_extreme_values'] / statistics_for_extremes['number_of_extreme_grids']

        percent_of_grids_max = np.max(percent_of_grids)
        percent_of_grids_mean = np.mean(percent_of_grids)
        extreme_value_max  = np.max(extreme_value)
        extreme_value_mean = np.mean(extreme_value)

        if percent_of_grids_max > 10:
            extreme_warning_level = 'low' 
        elif percent_of_grids_max > 30:
            extreme_warning_level = 'medium' 
        elif percent_of_grids_max > 50:
            extreme_warning_level = 'high' 

        return extreme_warning_level

