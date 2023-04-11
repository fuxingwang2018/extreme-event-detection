import sys, os
from netCDF4 import Dataset 
from xtrdet.utils import ncdump
from xtrdet.utils import open_data
from xtrdet.preproc import get_configuration


def test_ReadInputData():

    #file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    #path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'

    """
    config_file = 'xtrdet/config/config_main.ini' #tests/config_test.ini'
    if not os.path.isfile(config_file):
        raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
    configuration_dict = get_configuration.get_settings(config_file)

    print('configuration_dict', configuration_dict)
    # Target data
    var = 'pr'
    target_conf = open_data.ReadInputData(configuration_dict['data config'])
    trgt_data = target_conf.read_data(var)
    print('trgt_data', trgt_data)
    print('trgt_data', trgt_data['x'], len(trgt_data['x']))
    

    nc_file = target_conf.get_file_list(var)
    print('nc_file', nc_file)
    nc_file_in_id = Dataset(nc_file[0], 'r')
    nc_attrs, nc_dims, nc_vars = ncdump.ncdump(nc_file_in_id)

    dims_mandatory = ['y', 'x', 'time']
    assert all(item in nc_dims for item in dims_mandatory)
    assert len(trgt_data['x']) == len(nc_file_in_id.dimensions['x'])
    assert len(trgt_data['y']) == len(nc_file_in_id.dimensions['y'])
    assert len(trgt_data['time']) == len(nc_file_in_id.dimensions['time'])

    nc_file_in_id.close()
    """
    pass
