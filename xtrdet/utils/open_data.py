import os
import numpy as np
import xarray as xa
import glob
import re
from itertools import product
from datetime import datetime
from datetime import timedelta


class ReadInputData(object):
    """Reads input data"""

    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.data_src = data_dict['data source']
        self.var_dict = data_dict['variables']

    def get_selected_dates(self, s_year, e_year, mon):
        """
        Specify a list of selected dates
        """
        date_list = [f"{yy}{mm:02d}" for yy, mm in product(
            range(s_year, e_year+1), mon)]

        return date_list

    def get_file_list(self, variable, fpath, start_year, end_year, month):
        """
        Create a list of files for input data

        Args:
            TBD

        Returns:
            TBD
        """
        var_conf = self.var_dict[variable]
        tres = var_conf['freq']
        files = os.path.join(fpath, f'{tres}/{variable}/{variable}_*.nc')
        global_flist = glob.glob(files)

        date_select = self.get_selected_dates(start_year, end_year, month)
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
        readers = {
            'ecmwf ensemble': self.read_ecmwf_ens,
            'norcp': self.read_climate_model_data
        }

        target_data, climate_data = readers[self.data_src](variable)

        var_conf = self.var_dict[variable]
        scale_factor = var_conf['scale factor']
        offset_factor = var_conf['offset factor']

        if scale_factor is not None:
            target_data[variable] *= scale_factor
            climate_data[variable] *= scale_factor

        if offset_factor is not None:
            target_data[variable] += offset_factor
            climate_data[variable] += offset_factor

        return target_data, climate_data

    def read_ecmwf_ens(self, variable):
        """
        Read ECMWF ensemble forecast data
        Args:
            TBD

        Returns:
            TBD
        """
        ch_t = self.data_dict['chunks_time']
        ch_x = self.data_dict['chunks_x']
        ch_y = self.data_dict['chunks_y']

        var_conf = self.var_dict[variable]
        self.dailystat = var_conf['daily statistic']

        # Target data
        self.trgt_fpath = self.data_dict['target']['fpath']
        self.validtime = self.data_dict['target']['valid time']
        self.leadtime = self.data_dict['target']['lead time']
        fprx = (f"{variable}_*ltime_{self.leadtime}"
                f"*validtime_{self.validtime}.nc")
        files = os.path.join(self.trgt_fpath, variable,
                             self.dailystat, fprx)
        trgt_file = glob.glob(files)[0]
        trgt_select_data = xa.load_dataset(trgt_file)

        # Climatology data
        self.clim_fpath = self.data_dict['climatology']['fpath']
        self.clim_start_year = self.data_dict['climatology']['start year']
        self.clim_end_year = self.data_dict['climatology']['end year']
        self.day_window_size = self.data_dict['climatology']['day window size']
        fprx = f"{variable}_*.nc"
        files = os.path.join(self.clim_fpath, variable,
                             self.dailystat, fprx)
        clim_files = glob.glob(files)
        clim_files.sort()
        clim_data = xa.open_mfdataset(
            clim_files, parallel=True, combine='by_coords',
            chunks={**ch_t, **ch_x, **ch_y})

        vt = datetime.strptime(self.validtime, '%Y-%m-%d')
        date_start = (vt - timedelta(days=int(self.day_window_size/2)))
        date_start_str = datetime.strftime(date_start, '%Y-%m-%d')
        date_end = (vt + timedelta(days=int(self.day_window_size/2)))
        date_end_str = datetime.strftime(date_end, '%Y-%m-%d')
        select_dates = np.concatenate(
            [xa.date_range(f"{y}{date_start_str[4::]}T12:00:00",
                           f"{y}{date_end_str[4::]}T12:00:00", freq='D').values
             for y in range(self.clim_start_year, self.clim_end_year+1)])
        clim_select_data = clim_data.sel(time=select_dates)

        return trgt_select_data, clim_select_data

    def read_climate_model_data(self, variable):
        """
        Read ECMWF ensemble forecast data
        Args:
            TBD

        Returns:
            TBD
        """
        ch_t = self.data_dict['chunks_time']
        ch_x = self.data_dict['chunks_x']
        ch_y = self.data_dict['chunks_y']

        # Target data
        self.trgt_fpath = self.data_dict['target']['fpath']
        self.trgt_stat_year = self.data_dict['target']['start year']
        self.trgt_end_year = self.data_dict['target']['end year']
        self.trgt_month = self.data_dict['target']['month']
        file_list = self.get_file_list(variable, self.trgt_fpath,
                                       self.trgt_start_year,
                                       self.trgt_end_year,
                                       self.trgt_month)
        trgt_data = xa.open_mfdataset(
            file_list, parallel=True, combine='by_coords',
            chunks={**ch_t, **ch_x, **ch_y})

        trgt_select_data = trgt_data.where(
            ((trgt_data.time.dt.year >= self.trgt_start_year) &
             (trgt_data.time.dt.year <= self.trgt_end_year) &
             (np.isin(trgt_data.time.dt.month, self.trgt_month))),
            drop=True)

        # Climatology data
        self.clim_fpath = self.data_dict['climatology']['fpath']
        self.clim_stat_year = self.data_dict['climatology']['start year']
        self.clim_end_year = self.data_dict['climatology']['end year']
        self.clim_month = self.data_dict['climatology']['month']
        file_list = self.get_file_list(variable, self.clim_fpath,
                                       self.clim_start_year,
                                       self.clim_end_year,
                                       self.clim_month)
        clim_data = xa.open_mfdataset(
            file_list, parallel=True, combine='by_coords',
            chunks={**ch_t, **ch_x, **ch_y})

        clim_select_data = clim_data.where(
            ((clim_data.time.dt.year >= self.clim_start_year) &
             (clim_data.time.dt.year <= self.clim_end_year) &
             (np.isin(clim_data.time.dt.month, self.clim_month))),
            drop=True)

        return trgt_select_data, clim_select_data

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
