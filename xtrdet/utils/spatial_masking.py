import numpy as np
import os
import xarray as xa


class SpatialMasking:
    """
    Mask data spatially.

    Args:
        data
        Xarray Dataset object that includes spatial coordinates
    """
    def __init__(self, data, variable):

        self.data = data
        self.variable = variable
        self.xname, self.yname = self.get_spatial_coords(data)
        self.xcoords = self.data[self.xname].values
        self.ycoords = self.data[self.yname].values

    def get_spatial_coords(self, ds):
        """
        Return names for spatial coordinates in data set.
        """
        spcdim = {'x': ['lon', 'longitude', 'x', 'X', 'rlon'],
                  'y': ['lat', 'latitude', 'y', 'Y', 'rlat']}
        xd = [x for x in spcdim['x'] if x in ds.coords][0]
        yd = [y for y in spcdim['y'] if y in ds.coords][0]

        return xd, yd

    def polygons(self, area, polygon_print=False):
        """
        See available polygons and retrieve path to polygon files.

        Parameters
        ----------
        area: string
            name of polygon to be extracted
        polygon_print: boolean
            if available polygons should be printed

        Returns
        -------
        area_file: string
            path to the text file with polygon data
        """

        # -------- Dictionary of predfined regions -------- #
        file_dir = os.path.dirname(os.path.abspath(__file__))
        polypath = os.path.join(file_dir, 'polygon_files')

        errmsg = f"Folder to polygons: {polypath}, does not seem to exist!"
        assert os.path.exists(polypath), errmsg

        polygons = os.listdir(polypath)
        poly_dict = {s.split('.')[0].replace('_', ' '): s for s in polygons}

        if polygon_print:
            print("\nAvailable polygons/regions:\n")
            [print('\t{}'.format(ar)) for ar in poly_dict]
        else:
            errmsg = (f"\n\n\tOohps! '{area}' is not a pre-defined area. "
                      "Check polygon folder for the correct name or create "
                      "a new polygon.")
            assert area in poly_dict, errmsg

            area_file = os.path.join(polypath, poly_dict[area])
            return area_file

    def extract_masked_data(self, data, variable, mask):
        """
        Mask region
        """
        mask_in = xa.DataArray(
            np.broadcast_to(mask, data[variable].shape),
                               dims=data[variable].dims)
        return data.where(mask_in, drop=True)

    def get_mask(self, area, extract_data=False):
        """
        Routine to mask grid points outside a specified polygon.

        Parameters
        ----------
        area: string or list with tuples
            Either name of predefined region to extract,
            or a list with tuples defining a polygon;
            e.g. [(lon1, lat1), (lon2, lat2),...,(lonN, latN), (lon1, lat1)].
            NB! First and last tuple must be the same, closing the polygon.

        Returns
        -------
        mask_out: boolean array
            A 2D mask with True inside region of interest, False outside.
        """

        from matplotlib.path import Path

        # Dimensions of grid
        if self.xcoords.ndim == 2:
            ny, nx = self.xcoords.shape
        else:
            nx = self.xcoords.size
            ny = self.ycoords.size

        # Rearrange grid points into a list of tuples
        points = [(self.xcoords[i, j], self.ycoords[i, j]) if
                  self.xcoords.ndim == 2 else
                  (self.xcoords[j], self.ycoords[i])
                  for i in range(ny) for j in range(nx)]
        if type(area).__name__ == 'str':
            def coord_return(line):
                s = line.split()
                return list(map(float, s))
            reg_file = self.polygons(area)
            with open(reg_file, 'r') as ff:
                ff.readline()       # Skip first line
                poly = [coord_return(ln) for ln in ff.readlines()]
        else:
            poly = area
        reg_path = Path(np.array(poly))
        mask = reg_path.contains_points(points)
        mask = mask.reshape(ny, nx)
        self.poly = poly
        self.mask = mask

        if extract_data:
            out = self.extract_masked_data(self.data, self.variable, self.mask)
        else:
            out = mask.copy()

        return out

    def topo_mask(self, data, orog, height_interval):
        """
        Rotuine to mask grid points outside a specified height interval.

        Parameters
        ----------
        data:  2D numpy array
            the data matrix
        orog:  2D numpy array
            array containing topographical heights (same resolution as data)
        height_interval: 1D array,list,tuple
            the height interval outside which data should be masked.

        Returns
        -------
        masked_data: 2D numpy array
            the masked data

        """

        assert data.ndim == 2, \
            "Error! data array must be two-dimensional."

        assert data.shape() == orog.shape(), \
            "Error! data and orography arrays must have identical grids"

        # Create topographical mask
        orog_mask = np.ma.masked_outside(
            orog, height_interval[0], height_interval[1])
        orog_mask = np.ma.getmask(orog_mask)

        masked_data = np.ma.masked_where(orog_mask, data)

        return masked_data

    def find_geo_indices(lons, lats, x, y):
        """
        Search for nearest decimal degree in an array of decimal degrees and
        return the index.
        np.argmin returns the indices of minimum value along an axis.
        Subtract dd from all values in dd_array, take absolute value and find
        index of minimum.

        Parameters
        ----------
        lons/lats: 1D/2D numpy array
            Latitude and longitude values defining the grid.
        x, y: int/float
            Coordinates of searched for data point

        Returns
        -------
        lat_idx/lon_idx: ints
            The latitude and longitude indices where closest to searched
            data point.
        """
        if lons.ndim == 1:
            lons2d = np.repeat(lons[np.newaxis, :], lats.size, axis=0)
            lats2d = np.repeat(lats[:, np.newaxis], lons.size, axis=1)
        else:
            lons2d = lons
            lats2d = lats

        lonlat = np.dstack([lons2d, lats2d])
        delta = np.abs(lonlat-[x, y])
        ij_1d = np.linalg.norm(delta, axis=2).argmin()
        lat_idx, lon_idx = np.unravel_index(ij_1d, lons2d.shape)
        return lat_idx, lon_idx
