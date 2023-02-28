import os
import sys
from xtrdet.utils import open_data
from xtrdet.utils import ncdump


class PreProcessing(object):

    """
    Read data from input file

    """

    def __init__(self, path_in, file_in):
        self.path_in = path_in
        self.file_in = file_in


    def get_data_for_detection(self, dt_start, dt_end, vars_name):
        """
        Read the data (from coarse model) to be used for extreme detection.

        Args:
            dt_start:
            dt_end:

        Returns:
            data:

        """

        filereader = file_reader.FileReader(self.path_in + '/' + self.file_in)
        nc_file_in_id = filereader.Open_NC()

        Nx, Ny, lons, lats, time = filereader.getDimensions_NC(nc_file_in_id)
        varsOut = filereader.getParams_NC(nc_file_in_id, params = vars_name, close=True)

        return Nx, Ny, lons, lats, time, varsOut


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


    def get_subdomain(self, pctl_threshold):
        """
        Extract data over a pre-defined (sub)domain of the coarse model

        Args:


        Returns:


        """

        return


    def data_combine(self):
        """
        Combine the days from the desired period (e.g. a number of years or seasons) in a single dataset

        """

        pass
