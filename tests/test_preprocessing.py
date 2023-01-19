
import sys
from netCDF4 import Dataset 
sys.path.insert(0, '..')
from utils  import ncdump
from source import preprocessing

def test_preprocessing():

    #file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    #path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'
    file_in = 'sampledata.nc'
    path_in = 'tests/'
    dt_start = ''
    dt_end = ''
    vars_name = ['tas']


    preproc = preprocessing.PreProcessing(path_in, file_in)
    Nx, Ny, lons, lats, time, varsOut = preproc.get_data_for_detection(dt_start, dt_end, vars_name)

    nc_file_in_id = Dataset(path_in + '/' + file_in, 'r')
    nc_attrs, nc_dims, nc_vars = ncdump.ncdump(nc_file_in_id)

    dims_mandatory = ['y', 'x', 'time']
    assert all(item in nc_dims for item in dims_mandatory)
    assert Nx == len(nc_file_in_id.dimensions['x'])
    assert Ny == len(nc_file_in_id.dimensions['y'])
    assert len(time) == len(nc_file_in_id.dimensions['time'])

    nc_file_in_id.close()

 
