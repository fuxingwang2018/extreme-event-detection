
import datetime as dt  # Python standard library datetime  module
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import os, sys
import ncdump as nd

# Author:  Fuxing Wang, 30 June, 2019

class FileWriter(object):
    """Reads a file"""

    def __init__(self, file_out):
        self.file_out = file_out


    def Write_Txt(self, var_dict):
        try:
            with open(self.file_out, 'w') as outFile:
                for key_lev1, value_lev1 in var_dict.items(): 
                    if type(value_lev1) is dict:
                        outFile.write('%s\n' % (key_lev1))
                        for key_lev2, value_lev2 in value_lev1.items(): 
                            outFile.write('%s:%s\n' % (key_lev2, value_lev2))
                    else:
                        outFile.write('%s:%s\n' % (key_lev1, value_lev1))

        except IndexError:
            print("Error - Please specify an output file.")
            sys.exit(2)


    def Write_NC(self, nc_file_2D, nc_var_to_read, nc_vars_to_write, var_2D):

        #nam_lon = 'longitude'
        #nam_lat = 'latitude'
        nam_lon = 'lon'
        nam_lat = 'lat'

        #
        # Read 2D netcdf file
        #
        #nc_file_1D_id = Dataset(nc_file_1D, 'r')  # Dataset is the class behavior to open the file, and create an instance of the ncCDF4 class
        #nc_attrs_1d, nc_dims_1d, nc_vars_1d = nd.ncdump(nc_file_1D_id)

        # Extract data from NetCDF file
        #time_1d = nc_file_1D_id.variables['time'][:]
        #xx_1d = nc_file_1D_id.variables['xx'][:]  # extract/copy the data
        #yy_1d = nc_file_1D_id.variables['yy'][:]
        #nb_point = nc_file_1D_id.variables['Number_of_points'][:]  # extract/copy the data

        #
        # Read 2D netcdf file
        #
        nc_file_2D_id = Dataset(nc_file_2D, 'r')  
        nc_attrs_2d, nc_dims_2d, nc_vars_2d = nd.ncdump(nc_file_2D_id)

        # Extract data from NetCDF file
        #lon_2d = nc_file_2D_id.variables['longitude'][:]  # extract/copy the data
        #lat_2d = nc_file_2D_id.variables['latitude'][:]
        x = nc_file_2D_id.variables['x'][:]
        y = nc_file_2D_id.variables['y'][:] 
        time_2d = nc_file_2D_id.variables['time'][:]

        # Open a new NetCDF file to write the data to. 
        # Choose format from 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
        w_nc_file_out_id = Dataset(self.file_out, 'w', format='NETCDF4')
        w_nc_file_out_id.description = "" 

        # Using our previous dimension info, we can create the new time dimension
        # Even though we know the size, we are going to set the size to unknown
        data_dim = {}
        for dim in nc_dims_2d:
            print 'dim:', dim
            w_nc_file_out_id.createDimension(dim, None)
            if dim in nc_file_2D_id.variables:
                data_dim[dim] = w_nc_file_out_id.createVariable(dim, nc_file_2D_id.variables[dim].dtype,\
                                   (dim,)) 
                # You can do this step yourself but someone else did the work for us.
                for ncattr in nc_file_2D_id.variables[dim].ncattrs():
                    data_dim[dim].setncattr(ncattr, nc_file_2D_id.variables[dim].getncattr(ncattr))


        # Assign the dimension data to the new NetCDF file.
        w_nc_file_out_id.variables['time'][:] = time_2d
        w_nc_file_out_id.variables['y'][:] = y
        w_nc_file_out_id.variables['x'][:] = x

        # Time varied variables
        data_var={}

        #print 'nc_file_2D_id.variables[var].dimensions:', nc_file_1D_id.variables['xx'].dimensions == ('Number_of_points', )
        #print 'nc_file_2D_id.variables[var].dimensions:', nc_file_1D_id.variables['LE'].dimensions # == ('time', 'Number_of_points')

        # Constant variable
        for var in nc_vars_2d:
            if nam_lon in var or nam_lat in var:
	        data_var[var] = w_nc_file_out_id.createVariable(var, nc_file_2D_id.variables[var].dtype,\
                                   nc_file_2D_id.variables[var].dimensions)
                for ncattr in nc_file_2D_id.variables[var].ncattrs():
                    data_var[var].setncattr(ncattr, nc_file_2D_id.variables[var].getncattr(ncattr))
                w_nc_file_out_id.variables[var][:] = nc_file_2D_id.variables[var][:]

        for var in nc_vars_to_write:
            if var != 'time' and var != 'Projection_Type' and var != 'FRC_TIME_STP':
  	        #var_1D = nc_file_1D_id.variables[var][:]  # shape is time, Number_of_points
  	        #print 'shape of var_1D:', np.shape(var_1D), var

                #if nc_file_1D_id.variables[var].dimensions == ('time', 'Number_of_points'):
                    # Convert variables from 1D to 2D
                    #var_2D = np.reshape(var_1D, (len(time_1d), len(y), len(x))) # Shape is time, y, x
                    #print 'shape of var_2D:', np.shape(var_2D)

                # Create variable
                #data_var[var] = w_nc_file_out_id.createVariable(var, nc_file_2D_id.variables[var].dtype, \
		#					('time', 'y', 'x')) 	
                data_var[var] = w_nc_file_out_id.createVariable(var, nc_file_2D_id.variables[nc_var_to_read].dtype, \
							('y', 'x')) 	

                # Attributes:
                for ncattr in nc_file_2D_id.variables[nc_var_to_read].ncattrs():
                    data_var[var].setncattr(ncattr, nc_file_2D_id.variables[nc_var_to_read].getncattr(ncattr))

                # Assign values to variables
                w_nc_file_out_id.variables[var][:] = var_2D
                print ('shape of var_2D', var_2D.shape)
        #
        # Close NetCDF files.
        #
        w_nc_file_out_id.close()  

        #return var_out

