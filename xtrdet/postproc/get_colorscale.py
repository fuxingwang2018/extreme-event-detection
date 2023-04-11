import math
import numpy as np

class GetColorScale(object):
    """
    Get min/max scale for map plot
    """

    def __init__(self):

        #self.data = data
        pass

    def _round_down(self, n, decimals=0):

        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier


    def _round_up(self, n, decimals=0):

        multiplier = 10 ** decimals
        print('n, multiplier=', n, multiplier)
        return math.ceil(n * multiplier) / multiplier

    def get_scale(self, data, centered=False):

        print('type data', type(data))
        print('data', data)
        #if len(data.chunks['time']) > 1:
        #    data = data.chunk({'time': -1})
        if data.dtype != 'bool':
            data = data.chunk(dict(time=-1))
            abs_max = data.quantile(98/100)
            abs_min = data.quantile(2/100)
            print('abs_max', abs_max)
            print('abs_max sizes', abs_max.sizes)
            print('abs_max values', abs_max.values)
            print('abs_min values', abs_min.values)

            if centered:
                abs_max = np.maximum(abs(abs_max), abs(abs_min))
                abs_min = -abs_max

            round_max = self._round_up(abs_max, 1)
            round_min = self._round_down(abs_min, 1)

        elif data.dtype == 'bool':
            round_max = 1
            round_min = 0

        scale = {'scale_max': round_max, 'scale_min': round_min}        

        print('scale', scale)
        return scale
 
