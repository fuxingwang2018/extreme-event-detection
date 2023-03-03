import os
import numpy as np
import xarray as xa
import glob
import re
from itertools import product


class ReadInputData(object):
    """Reads input data"""

    def __init__(self, data_dict):
        self.data_dict = data_dict

        self.start_year = data_dict['start year']
        self.end_year = data_dict['end year']
        self.mon = data_dict['month']
        self.date = data_dict['date']
        if 'day window size' in data_dict:
            self.day_window_size = data_dict['day window size']

        self.var_dict = data_dict['variables']

    def get_selected_dates(self):
        """
        Specify a list of selected dates
        """
        date_list = [f"{yy}{mm:02d}" for yy, mm in product(
            range(self.start_year, self.end_year+1), self.mon)]

        return date_list

    def get_file_list(self, variable):
        """
        Create a list of files for input data

        Args:
            TBD

        Returns:
            TBD
        """
        var_conf = self.var_dict[variable]
        tres = var_conf['freq']
        fpath = self.data_dict['fpath']
        file_path = os.path.join(fpath, f'{tres}/{variable}/{variable}_*.nc')
        global_flist = glob.glob(file_path)

        date_select = self.get_selected_dates()
        filename_dates = [re.split('-|_', f.rsplit('.')[-2])[-2:]
                          for f in global_flist]
        filename_dates = [(d[0][:6], d[1][:6]) for d in filename_dates]

        idx_date_selection = [
            np.where([d[0] <= date <= d[1] for d in filename_dates])[0]
            for date in date_select]
        select_flist = [global_flist[i]
                        for i in np.unique(np.hstack(idx_date_selection))]
        select_flist.sort()

        return select_flist

    def read_data(self, variable):
        """
        Args:
            TBD

        Returns:
            TBD
        """
        var_conf = self.var_dict[variable]
        ch_t = self.data_dict['chunks_time']
        ch_x = self.data_dict['chunks_x']
        ch_y = self.data_dict['chunks_y']
        scale_factor = var_conf['scale factor']
        offset_factor = var_conf['offset factor']

        file_list = self.get_file_list(variable)

        data = xa.open_mfdataset(
            file_list, parallel=True, combine='by_coords',
            chunks={**ch_t, **ch_x, **ch_y})

        select_data = data.where(
            ((data.time.dt.year >= self.start_year) &
             (data.time.dt.year <= self.end_year) &
             (np.isin(data.time.dt.month, self.mon))),
            drop=True)

        if scale_factor is not None:
            select_data[variable] *= scale_factor

        if offset_factor is not None:
            select_data[variable] += offset_factor

        xd, yd = self.get_spatial_coords(select_data)

        if select_data[xd].max() > 180:
            select_data = self.convert_lon_to_plusminus180(select_data, xd)

        return select_data

    def convert_lon_to_plusminus180(self, ds, xcoord):
        ds.coords[xcoord] = (ds.coords[xcoord] + 180) % 360 - 180
        if ds.coords[xcoord].ndim == 1:
            ds = ds.sortby(ds[xcoord])

        return ds

    def get_spatial_coords(self, ds):
        """
        Return names for spatial coordinates in data set.
        """
        spcdim = {'x': ['lon', 'longitude', 'x', 'X', 'rlon'],
                  'y': ['lat', 'latitude', 'y', 'Y', 'rlat']}
        xd = [x for x in spcdim['x'] if x in ds.coords][0]
        yd = [y for y in spcdim['y'] if y in ds.coords][0]

        return xd, yd
