
import os
import extreme_detection_algorithm
import get_configuration
import preprocessing
import numpy as np

def main():

    os.system('ulimit -c')

    # Get configuration 
    args = get_configuration.get_args()
    config_file = args.config
    if not os.path.isfile(config_file):
        raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
    cdict = get_configuration.get_settings(config_file)
    print ('var', cdict['variables'])

    #file_in = 'tas_NEU-12_ICHEC-EC-EARTH_historical_r12i1p1_HCLIMcom-HCLIM38-ALADIN_v1_1hr_198501010000-198512312300.nc'
    #path_in = '/nobackup/rossby24/proj/rossby/joint_exp/norcp/netcdf/NorCP_ALADIN_ECE_1985_2005/1hr/tas'
    file_in = 'sampledata.nc'
    path_in = '../tests'
    period_of_detection  = []
    coordinates_of_detection_area = cdict['coordinates_of_detection_area']

    variable_name_of_detection = list(cdict['variables'])
    preproc = preprocessing.PreProcessing(path_in, file_in)
    data_used_for_detection = preproc.get_data_for_detection(period_of_detection, \
        variable_name_of_detection, coordinates_of_detection_area)
    #print('data_used_for_detection', type(data_used_for_detection), np.shape(data_used_for_detection))

    extreme_detection = extreme_detection_algorithm.ExtremeDetectionAlgorithm(data_used_for_detection)
    for stats in cdict['stats_conf']:
        print ('stats', stats)
        if 'threshold_based' in stats:
            time_period_of_extreme_triggered, extreme_warning_level = extreme_detection.threshold_based_algorithm(\
                cdict['stats_conf'][stats]['filter_method'], \
                cdict['stats_conf'][stats]['pctl_threshold'], \
                cdict['stats_conf'][stats]['perc_of_days'])
        #print('days_of_extreme_detected', type(days_of_extreme_detected), np.shape(days_of_extreme_detected))
        print('time_period_of_extreme_triggered, extreme_warning_level:', time_period_of_extreme_triggered, extreme_warning_level)


    """
    Evaluation()

    PostProcessing()

    UnitTest()
    """


if __name__ == "__main__":
    main()

