
import sys
import os
# sys.path.insert(0, '..')
from preproc import ini_reader

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
        'target data': conf_dict['INPUT DATA']['target data'],
        'cont data': conf_dict['INPUT DATA']['contingency data'],
        'start year': conf_dict['SETTINGS']['start year'],
        'end year': conf_dict['SETTINGS']['end year'],
        'months': conf_dict['SETTINGS']['months'],
        'variables': conf_dict['SETTINGS']['variables'],
        'var modification': conf_dict['SETTINGS']['variable modification'],
        'regions': conf_dict['SETTINGS']['target regions'],
        'requested_stats': conf_dict['STATISTICS']['stats'],
        'detection plot': conf_dict['PLOTTING']['detection plot'],
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



