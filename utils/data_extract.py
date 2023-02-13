import numpy as np

def adjust_coordinates(lon, lat, ngrids_relax_zone = 0, ngrids_exten_zone = 0):
    """
    Adjust coordinates to get valid values for analysis, e.g., discard values over extention/relaxation zones

    :param lon: Longitudes
    :type lon: 2-dimension array, float
    :param lat: Latitudes
    :type lat: 2-dimension array, float
    :param ngrids_relax_zone: Number of grids used for relaxation zone
    :type ngrids_relax_zone: integer
    :param ngrids_exten_zone: Number of grids used for extention zone
    :type ngrids_exten_zone: integer
    :return: Adjusted longitudes and latitudes to get valid values for analyis
    :rtype: 2-dimension array, float
    """

    if ngrids_relax_zone < 0 or ngrids_exten_zone < 0:
        raise ValueError("ngrids_relax_zone and ngrids_exten_zone should not be negative")
    else:
        ngrids = ngrids_relax_zone + ngrids_exten_zone

    lon_valid = lon[ngrids: -ngrids, ngrids: -ngrids]
    lat_valid = lat[ngrids: -ngrids, ngrids: -ngrids]

    return lon_valid, lat_valid


def get_data_over_target_domain(var_ld, lon_ld, lat_ld, coordinates_of_detection_area):
    """
    Extract data from a larger domain over a smaller target domain

    :param var_ld: Variable for large domain
    :type var_ld: 3-dimension array (time, lat, lon), float
    :param lat_ld: Latitudes for large domain
    :type lat_ld: 2-dimension array (lat, lon), float
    :param lon_sd: Longitudes for small domain
    :type lon_sd: 2-dimension array (lat, lon), float
    :param coordinates_of_detection_area: 
    :type coordinates_of_detection_area: dictionary, string
    :return: var, lat and lon over target domain
    :rtype: array
    """

    #lon_sd_min = lon_sd[0,0]
    #lon_sd_max = lon_sd[-1,-1]
    #lat_sd_min = lat_sd[0,0]
    #lat_sd_max = lat_sd[-1,-1]
    lon_sd_min = coordinates_of_detection_area['lonmin']
    lon_sd_max = coordinates_of_detection_area['lonmax']
    lat_sd_min = coordinates_of_detection_area['latmin']
    lat_sd_max = coordinates_of_detection_area['latmax']

    dif_min = np.sqrt((lat_ld - lat_sd_min)**2 + (lon_ld - lon_sd_min)**2)
    dif_max = np.sqrt((lat_ld - lat_sd_max)**2 + (lon_ld - lon_sd_max)**2)

    ind_lat_ld_min = np.unravel_index(np.argmin(dif_min), lat_ld.shape)[0]
    ind_lon_ld_min = np.unravel_index(np.argmin(dif_min), lat_ld.shape)[1]
    ind_lat_ld_max = np.unravel_index(np.argmin(dif_max), lat_ld.shape)[0]
    ind_lon_ld_max = np.unravel_index(np.argmin(dif_max), lat_ld.shape)[1]

    print('var_ld', np.shape(var_ld))
    print('lat_ld', np.shape(lat_ld))

    var_over_target_domain = var_ld[:, ind_lat_ld_min : ind_lat_ld_max + 1, \
                        ind_lon_ld_min : ind_lon_ld_max + 1]
    lat_over_target_domain = lat_ld[ind_lat_ld_min : ind_lat_ld_max + 1, \
                        ind_lon_ld_min : ind_lon_ld_max + 1]
    lon_over_target_domain = lon_ld[ind_lat_ld_min : ind_lat_ld_max + 1, \
                        ind_lon_ld_min : ind_lon_ld_max + 1]
    #var_ld = varsout[:, ind_lat1_min + RelaxZone : ind_lat1_max + RelaxZone + 1, \
    #                ind_lon1_min + RelaxZone : ind_lon1_max + RelaxZone + 1]

    return var_over_target_domain, lat_over_target_domain, lon_over_target_domain


def get_data_over_target_period(varin, ):
    """
    Extract data from a longer period over a shorter target period (to complete)

    :param lon_ld: Longitudes for large domain
    :type lon_ld: 2-dimension array, float
    :param lat_ld: Latitudes for large domain
    :type lat_ld: 2-dimension array, float
    :param lon_sd: Longitudes for small domain
    :type lon_sd: 2-dimension array, float
    :param lat_sd: Latitudes for small domain
    :type lat_sd: 2-dimension array, float
    :return: The index for large domain corresponding to the small domain
    :rtype: integer
    """
    pass
