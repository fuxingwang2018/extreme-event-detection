
import sys
import os
sys.path.insert(0, '..')
from utils import ini_reader

def get_args():
    """
    Read configuration file
    Args:

    Returns:
    """
    import argparse

    # Configuring argument setup and handling
    parser = argparse.ArgumentParser(
        description='Main script for model/obs validation')
    parser.add_argument('--config', '-c',  metavar='name config file',
                        type=str, help='<Required> Full path to config file',
                        required=True)
    return parser.parse_args()


def get_settings(config_file):
    """
    Retrieve information from main configuration file
    """
    conf_dict = ini_reader.get_config_dict(config_file)
    d = {
        'models': conf_dict['MODELS'],
        'obs metadata file': conf_dict['OBS']['metadata file'],
        'obs start year': conf_dict['OBS']['start year'],
        'obs end year': conf_dict['OBS']['end year'],
        'obs months': conf_dict['OBS']['months'],
        'variables': conf_dict['SETTINGS']['variables'],
        'var modification': conf_dict['SETTINGS']['variable modification'],
        #'regions': conf_dict['SETTINGS']['regions'],
        'coordinates_of_detection_area': conf_dict['SETTINGS']['coordinates_of_detection_area'], 
        'requested_stats': conf_dict['STATISTICS']['stats'],
        'stats_conf': mod_stats_config(conf_dict['STATISTICS']['stats']),
        'validation plot': conf_dict['PLOTTING']['validation plot'],
        'map configure': conf_dict['PLOTTING']['map configure'],
        'map grid setup': conf_dict['PLOTTING']['map grid setup'],
        'map kwargs': conf_dict['PLOTTING']['map kwargs'],
        'line grid setup': conf_dict['PLOTTING']['line grid setup'],
        'line kwargs': conf_dict['PLOTTING']['line kwargs'],
        'cluster type': conf_dict['CLUSTER']['cluster type'],
        'nodes': conf_dict['CLUSTER']['nodes'],
        'cluster kwargs': conf_dict['CLUSTER']['cluster kwargs'],
        'outdir': conf_dict['SETTINGS']['output dir'],
    }

    return d


def default_stats_config(stats):
    """
    Get default statistics configurations of stats

    :param stats: A list of statistics
    :type stats: List of strings
    :return: A dictionary with default statistics configurations for a selection of statistics given by input stats
    :rtype: dictionary
    """
    stats_dict = {
        'threshold_based': {
            'filter_method': 'percentile',
            'pctl_threshold': 95,
            'perc_of_days': 10, }
            }

    return {k: stats_dict[k] for k in stats}


def mod_stats_config(requested_stats):
    """
    Get the configuration for the input statistics 'requested_stats'.

    :param stats: A list of statistics
    :type stats: List of strings
    :return: A dictionary with modified statistics configurations for input requested_stats
    :rtype: dictionary
    """
    stats_dd = default_stats_config(list(requested_stats.keys()))

    # Update dictionary based on input
    for k in requested_stats:
        if requested_stats[k] == 'default':
            pass
        else:
            for m in requested_stats[k]:
                msg = "For statistic {}, the configuration key {} is not "\
                        "available. Check possible configurations  in "\
                        "default_stats_config in stats_template "\
                        "module.".format(k, m)
                try:
                    stats_dd[k][m] = requested_stats[k][m]
                except KeyError:
                    print(msg)

    return stats_dd

