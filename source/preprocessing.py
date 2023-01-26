import os, sys
sys.path.insert(0, '..')
from utils import file_reader
from utils import ncdump
from utils import data_extract

class PreProcessing(object):

    """
    Read data from input file
    
    """

    def __init__(self, path_in, file_in):
        self.path_in = path_in
        self.file_in = file_in


    def get_rawdata(self, variable_name_of_detection):

        """
        Get the raw data from input files.

        :param variable_name_of_detection: The variable name to be used for detection
        :type variable_name_of_detection: List of strings
        :return: The data dimension, coordinates and variable values in the input file
        :rtype: 
        """

        filereader = file_reader.FileReader(self.path_in + '/' + self.file_in)
        nc_file_in_id = filereader.open_nc()

        nx_in_rawdata, ny_in_rawdata, longitudes_in_rawdata, latitudes_in_rawdata, time_in_rawdata = \
            filereader.getdimensions_nc(nc_file_in_id)

        variable_in_rawdata = \
            filereader.getparams_nc(nc_file_in_id, params = variable_name_of_detection, close=True)

        return nx_in_rawdata, ny_in_rawdata, longitudes_in_rawdata, latitudes_in_rawdata, time_in_rawdata, variable_in_rawdata


    def get_data_for_detection(self, period_of_detection, \
        variable_name_of_detection, coordinates_of_detection_area):

        """
        Get the data to be used for extreme detection.

        :param period_of_detection: pre-defined period to detect extreme event
        :type period_of_detection: dictionary
        :param variable_name_of_detection: The variable name to be used for detection
        :type variable_name_of_detection: List of strings
        :param coordinates_of_detection_area: Longitudes and latitudes for the detection area
        :type coordinates_of_detection_area: dictionary
        :return: The data used for detection
        :rtype: 
        """

        nx_in_rawdata, ny_in_rawdata, longitudes_in_rawdata, latitudes_in_rawdata, \
            time_in_rawdata, variable_in_rawdata = self.get_rawdata(variable_name_of_detection)

        #lon_ld, lat_ld = \
        #    data_extract.adjust_coordinates(lon_ld_orig, lat_ld_orig, \
        #    ngrids_relax_zone, ngrids_exten_zone)

        data_used_for_detection = \
            data_extract.get_data_over_target_domain(variable_in_rawdata, \
            longitudes_in_rawdata, latitudes_in_rawdata, \
            coordinates_of_detection_area)


        return data_used_for_detection


    def get_data_for_evaluation(self, dt_start, dt_end):
        """
        Read the data (from higher resolution model) to be used for evaluation.

        Args:
            dt_start: 
            dt_end: 

        Returns:
            data:

        """

        return


    def data_combine(self):
        """
        Combine the days from the desired period (e.g. a number of years or seasons) in a single dataset

        """

        pass
