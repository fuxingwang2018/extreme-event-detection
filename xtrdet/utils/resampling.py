import numpy as np
from pandas import to_timedelta
from datetime import timedelta
from functools import reduce


class Resampling:
    """
    Resample data with chosen time frequency and resample method.
    """
    def __init__(self, resample_frequency, resample_method):

        self.res_freq = resample_frequency
        self.res_method = resample_method

    def change_resample_frequency(self, frequency):
        self.res_freq = frequency

    def change_resample_method(self, method):
        self.res_method = method

    def get_time_frequency(self, frequency):

        d = [j.isdigit() for j in frequency]
        if np.any(d):
            freq = int(reduce((lambda x, y: x+y),
                              [x for x, y in zip(frequency, d) if y]))
        else:
            freq = 1

        unit = reduce((lambda x, y: x+y),
                      [x for x, y in zip(frequency, d) if not y])

        if unit in ('M', 'Y'):
            freq = freq*30 if unit == 'M' else freq*365
            unit = 'D'
        elif unit[0] == 'Q':
            # Quarterly frequencies - assuming average 90 days
            freq = 90
            unit = 'D'

        return freq, unit

    def resample(self, data):

        number, units = self.get_time_frequency(self.res_freq)
        resample_in_seconds = to_timedelta(number, units).total_seconds()

        if resample_in_seconds < 24*3600:
            data = eval(
                f"data.resample(time='{self.res_freq}', "
                f"label='right', closed='right').{self.res_method}('time')."
                f"dropna('time', 'all')")
            data['time'] = data.time - np.timedelta64(
                timedelta(seconds=np.round(resample_in_seconds/2)))
        else:
            data = eval(f"data.resample(time='{self.res_freq}')."
                        f"{self.res_method}('time').dropna('time', 'all')")
        return data
