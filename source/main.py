
import os
import extreme_detection_algorithm
import get_configuration
import preprocessing

def main():

    os.system('ulimit -c')

    # Get configuration 
    args = get_configuration.get_args()
    config_file = args.config
    if not os.path.isfile(config_file):
        raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
    cdict = get_configuration.get_settings(config_file)

    #file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    #path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'
    file_in = 'sampledata.nc'
    path_in = '../tests'
    period_of_detection  = []
    coordinates_of_detection_area = {'lonmin':18, 'lonmax':19, 'latmin':59, 'latmax':60} 
    variable_name_of_detection = ['tas']
    preproc = preprocessing.PreProcessing(path_in, file_in)
    data_used_for_detection = preproc.get_data_for_detection(period_of_detection, \
        variable_name_of_detection, coordinates_of_detection_area)

    """ 
    extreme_detection = extreme_detection_algorithm.ExtremeDetectionAlgorithm(algorithm, var)
    days_of_extreme_detected = extreme_detection.threshold_based_algorithm(filter_method, pctl_threshold, perc_of_days)


    Evaluation()

    PostProcessing()

    UnitTest()
    """


if __name__ == "__main__":
    main()

