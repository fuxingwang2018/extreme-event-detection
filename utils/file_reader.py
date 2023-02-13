
import datetime as dt  # Python standard library datetime  module
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import numpy as np
import os, sys

class FileReader(object):
    """Reads a file"""

    def __init__(self, file_in):
        self.file_in = file_in

    def read_txt(self):
        """
        Function to read txt file.

        :param file_in: string with full path to file
        :type file_in: string
        :return: Contents in the file: x, y
        :rtype: 
        """
        try:
            with open(self.file_in, 'r') as inFile:
                lines = inFile.readlines()
                x = [line.split()[0] for line in lines]
                y = [line.split()[1] for line in lines]
                return x, y

        except IndexError:
            sys.exit("Error - Please specify an input txt file.")


    def open_nc(self):
        """
        Function to open netcdf file.

        :param file_in: string with full path to file
        :type file_in: string
        :return: nc_file_in_id
        :rtype: object
        """

        try:
            nc_file_in_id = Dataset(self.file_in, 'r')
            return nc_file_in_id

        except Exception:
            sys.exit("Error - Please specify an input NetCDF file.")


    def getdimensions_nc(self, nc_file_in_id, close=False):
        """ 
        Function to retrieve the dimensions of a netcdf file

        :param nc_file_in_id: Netcdf object opened with function "openFile"
        :type nc_file_in_id: object
        :param close: 'True' to close the file after retrieval; 'False' otherwise, default to 'False'.
        :type close: Boolean
        :return: lons, lats, time, gridsize nx, ny.
        :rtype: 
        """

        try:
            nx = len(nc_file_in_id.dimensions['x'])
            ny = len(nc_file_in_id.dimensions['y'])
        except:
            print("File does not have 'x' and 'y' \
            dimensions. Returning None.")
            nx = None
            ny = None

        try:
            time = nc_file_in_id.variables['time'][:]
        except:
            print("File does not have a 'time'"
              "variable. Returning None.")
            time = None

        try:
            lons = nc_file_in_id.variables['lon'][:]
            lats = nc_file_in_id.variables['lat'][:]
        except:
            try:
                lons = nc_file_in_id.variables['longitude'][:]
                lats = nc_file_in_id.variables['latitude'][:]
            except:
                print("*** Error ***")
                print("Could not extract longitudes/latitudes.")
                print("Check that file contains these variables"
                  "and that they have standard names")
                sys.exit()

        if close:
            nc_file_in_id.close()

        return nx, ny, lons, lats, time



    def getparams_nc(self, nc_file_in_id, params, close=False):

        """ 
        Function to retrieve variables from a netcdf file

        :param nc_file_in_id: Netcdf object opened with function "openFile"
        :type nc_file_in_id: object
        :param params: A list of strings with the parameters to be retrieved
        :type params: list
        :param close: 'True' to close the file after retrieval; 'False' otherwise, default to 'False'.
        :type close: Boolean
        :return: A dictionary of arrays with given parameters.
        :rtype: dictionary.
        """

        # Make sure params is a list
        if type(params) != list:
            params = [params]

        varsout = {}
        for vv in params:
            print('vv', type(vv), vv)
            try:
                varsout[vv] = nc_file_in_id.variables[vv][:]
            except Exception:
                print("*** Error ***")
                print("Variable " + vv + " not found in file!")
                sys.exit()

        if close:
            nc_file_in_id.close()

        return varsout



    def get_np_file(self, params):

        """ 
        Function to retrieve variables from .npy, .npz or pickled files.

        :param params: A list of strings with the parameters to be retrieved
        :type params: list
        :return: Data stored in the file.
        :rtype: array, tuple, dict, etc.
        """

        if type(params) != list:
            params = [params]

        varsout = []
        for vv in range(len(params)):
            try:
                with np.load(self.file_in) as data:
                    varsout.append(data[vv])
            except Exception:
                print("*** Error ***")
                print("Variable " + params[vv] + " not found in file!")
                sys.exit()

        return varsout

