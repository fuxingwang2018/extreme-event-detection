
import os
from exed.methods import optim_threshold
from exed.preproc import get_configuration
from exed.preproc import preprocessing

def main():

    os.system('ulimit -c')

    # Get configuration 
    args = get_configuration.get_args()
    config_file = args.config
    if not os.path.isfile(config_file):
        raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
    cdict = get_configuration.get_settings(config_file)

    file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'
    dt_start = ''
    dt_end = ''
    vars_name = ['tas']
    preproc = preprocessing.PreProcessing(path_in, file_in)
    Nx, Ny, lons, lats, time, varsOut = preproc.get_data_for_detection(dt_start, dt_end, vars_name)

    """ 
    extreme_detection = extreme_detection_algorithm.Extreme_Detection_Algorithm(algorithm, var)
    days_of_extreme_detected = extreme_detection.threshold_based_algorithm(filter_method, pctl_threshold, perc_of_days)


    Evaluation()

    PostProcessing()

    UnitTest()
    """


if __name__ == "__main__":
    main()
