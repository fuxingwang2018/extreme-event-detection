
import sys
from netCDF4 import Dataset 
from utils  import ncdump
from source import preprocessing

def test_preprocessing():

    #file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    #path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'
    file_in = 'sampledata.nc'
    path_in = 'tests/'


    #period_of_detection  = []
    #coordinates_of_detection_area = {'lonmin':18, 'lonmax':19, 'latmin':59, 'latmax':60} 
    variable_name_of_detection = ['tas']
    preproc = preprocessing.PreProcessing(path_in, file_in)
    #data_for_detection = preproc.get_data_for_detection(period_of_detection, \
    #    variable_name_of_detection, coordinates_of_detection_area)
    raw_data = preproc.get_rawdata(variable_name_of_detection)
    #nx, ny, lons, lats, time, varsout = preproc.get_rawdata(variable_name_of_detection)


    nc_file_in_id = Dataset(path_in + '/' + file_in, 'r')
    nc_attrs, nc_dims, nc_vars = ncdump.ncdump(nc_file_in_id)

    dims_mandatory = ['y', 'x', 'time']
    assert all(item in nc_dims for item in dims_mandatory)
    assert raw_data['nx_in_rawdata'] == len(nc_file_in_id.dimensions['x'])
    assert raw_data['ny_in_rawdata'] == len(nc_file_in_id.dimensions['y'])
    assert len(raw_data['time_in_rawdata']) == len(nc_file_in_id.dimensions['time'])

    nc_file_in_id.close()

 
