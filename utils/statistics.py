
import numpy as np
import sys
import warnings
import pandas as pd
import scipy.stats as stats
#from utils import tools
import random 


class Statistics(object):

    def __init__(self, var_ref):

        self.var_ref = var_ref


    def get_statistics_daily(self, filter_method, var_pctl): 
        """
        Get weather statistics for each day, which are used to filter out days of extreme events

        Args:
            filter_method:    percentile or number 
            var_in:           input variable values
            var_pctl:         N-th percentile (e.g. N = 95) of all the data in var_in

        Returns:
            statistics_daily: weather statistics for each day
        """

        if filter_method == 'percentile':
            # For each day, find grid points with var_in > var_pctl and adds them together to get a single value over the (sub)domain for all grid points
            statistics_daily = np.sum(ma.masked_array(self.var_ref, ~var_pctl), axis = (1,2) if self.var_ref.ndim == 3 else 1)
        elif filter_method == 'number':
            statistics_daily = np.sum(var_pctl, axis = (1,2))
        else:
            sys.exit('filter_method not defined')

        return statistics_daily

