
import datetime as dt  # Python standard library datetime  module
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import numpy as np
import os, sys

class FileReader(object):
    """Reads a file"""

    def __init__(self, file_in):
        self.file_in = file_in

    def Read_TXT(self):
        try:
            with open(self.file_in, 'r') as inFile:
                lines = inFile.readlines()
                x = [line.split()[0] for line in lines]
                y = [line.split()[1] for line in lines]
                return x, y

        except IndexError:
            sys.exit("Error - Please specify an input txt file.")


    def Open_NC(self):
        """
        Function to open netcdf file.

        Args:
            filename:  string with full path to file
 
        Returns:
            nc_file_in_id
        """

        try:
            nc_file_in_id = Dataset(self.file_in, 'r')
            return nc_file_in_id

        except Exception:
            sys.exit("Error - Please specify an input NetCDF file.")


    def getDimensions_NC(self, nc_file_in_id, close=False):
        """ 
        Function to retrieve the dimensions of a netcdf file

        Args:
            nc: Netcdf object opened with function "openFile"
            close: set True if you want the file to be closed after retrieval.

        Returns:
             lons and lats, time as well as gridsize Nx,Ny 
        """

        try:
            Nx = len(nc_file_in_id.dimensions['x'])
            Ny = len(nc_file_in_id.dimensions['y'])
        except:
            print("File does not have 'x' and 'y' \
            dimensions. Returning None.")
            Nx = None
            Ny = None

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

        return Nx, Ny, lons, lats, time



    def getParams_NC(self, nc_file_in_id, params, close=False):

        """ 
        Function to retrieve variables from a netcdf file

        Args:        
            nc: Netcdf object opened with function "openFile"
            params: A list of strings with the parameters to be retrieved
            close: set True if you want the file to be closed after retrieval.

        Returns:
            A list with the given parameters. 
        """

        # Make sure params is a list
        if type(params) != list:
            params = [params]

        varsOut = []
        for vv in range(len(params)):
            try:
                varsOut.append(nc_file_in_id.variables[params[vv]][:])
            except Exception:
                print("*** Error ***")
                print("Variable " + params[vv] + " not found in file!")
                sys.exit()

        if close:
            nc_file_in_id.close()

        return np.array(varsOut).squeeze()
