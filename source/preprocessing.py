import os, sys
sys.path.insert(0, '..')
from utils import file_reader
from utils import ncdump
from utils import data_extract
import numpy as np

class PreProcessing(object):

    """
    Read data from input file
    
    """

    def __init__(self, path_in, file_in):
        self.path_in = path_in
        self.file_in = file_in


    def get_rawdata(self, variable_names_of_detection):

        """
        Get the raw data from input files.

        :param variable_names_of_detection: The variable names to be used for detection
        :type variable_names_of_detection: List of strings
        :return: The data dimension, coordinates and variable values in the input file
        :rtype: dictionary 
        """

        filereader = file_reader.FileReader(self.path_in + '/' + self.file_in)
        nc_file_in_id = filereader.open_nc()

        nx_in_rawdata, ny_in_rawdata, longitudes_in_rawdata, latitudes_in_rawdata, time_in_rawdata = \
            filereader.getdimensions_nc(nc_file_in_id)

        variable_in_rawdata = \
            filereader.getparams_nc(nc_file_in_id, params = variable_names_of_detection, close=True)
        #print('variable_in_rawdata', type(variable_in_rawdata), np.shape(variable_in_rawdata))

        raw_data = {}
        raw_data['nx_in_rawdata'] = nx_in_rawdata
        raw_data['ny_in_rawdata'] = ny_in_rawdata
        raw_data['longitudes_in_rawdata'] = longitudes_in_rawdata
        raw_data['latitudes_in_rawdata'] = latitudes_in_rawdata
        raw_data['time_in_rawdata'] = time_in_rawdata

        for vv in variable_names_of_detection:
            try:
                raw_data[vv] = variable_in_rawdata[vv]
            except Exception:
                print("*** Error ***")
                print("Variable " + variable_names_of_detection[vv] + " not found!")
                sys.exit()

        return raw_data


    def get_data_for_detection(self, \
        period_of_detection, \
        variable_names_of_detection, \
        coordinates_of_detection_area):

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

        data_for_detection = {}
        raw_data = self.get_rawdata(variable_names_of_detection)

        #lon_ld, lat_ld = \
        #    data_extract.adjust_coordinates(lon_ld_orig, lat_ld_orig, \
        #    ngrids_relax_zone, ngrids_exten_zone)

        for variable_name_of_detection in variable_names_of_detection:
            data_for_detection[variable_name_of_detection], \
            data_for_detection['latitude'], \
            data_for_detection['longitude'] = \
                data_extract.get_data_over_target_domain(\
                raw_data[variable_name_of_detection], \
                raw_data['longitudes_in_rawdata'], \
                raw_data['latitudes_in_rawdata'], \
                coordinates_of_detection_area)

        return data_for_detection


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
