import sys
import os
from dask.distributed import Client
from xtrdet.methods import event_detection_algorithms
from xtrdet.preproc import get_configuration
from xtrdet.preproc import preprocessing
from xtrdet.utils import open_data
from xtrdet.utils import resampling
from xtrdet.utils import spatial_masking


def local_cluster_setup():
    """
    Set up local-pc cluster

    """
    from dask.distributed import LocalCluster
    cluster = LocalCluster(processes=False)
    return cluster


def slurm_cluster_setup(nodes=1, **kwargs):
    """
    Set up SLURM cluster

    Parameters
    ----------
    nodes: int
        Number of nodes to use
    **kwargs:
        Keyword arguments for cluster specifications
    """
    from dask_jobqueue import SLURMCluster
    cluster = SLURMCluster(**kwargs)
    cluster.scale(nodes)
    return cluster


def get_args():
    """
    Read configuration file
    Parameters
    ----------
    -
    Returns
    -------
    Input arguments
    """
    import argparse

    # Configuring argument setup and handling
    parser = argparse.ArgumentParser(
        description='Main script for model/obs validation')
    parser.add_argument('--config', '-c',  metavar='name config file',
                        type=str, help='<Required> Full path to config file',
                        required=True)
    return parser.parse_args()


def main():

    os.system('ulimit -c')

    # Get configuration
    # args = get_configuration.get_args()
    # config_file = args.config
    # if not os.path.isfile(config_file):
    #     raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
    config_file = '/home/sm_petli/dev/scripts/python/analysis/DEODE/extreme_event_detection/config_main.ini'  # noqa
    configuration_dict = get_configuration.get_settings(config_file)

    # Create dirs
    outdir = configuration_dict['outdir']
    if not os.path.exists(configuration_dict['outdir']):
        os.makedirs(outdir)

    # Set up distributed client
    if configuration_dict['cluster type'] == 'local':
        cluster = local_cluster_setup()
    elif configuration_dict['cluster type'] == 'slurm':
        nnodes = configuration_dict['nodes']
        sl_kwargs = configuration_dict['cluster kwargs']
        cluster = slurm_cluster_setup(nodes=nnodes, **sl_kwargs)
    else:
        print("\n\tCluster type not implemented! Exiting..")
        sys.exit()

    client = Client(cluster)

    # Settings
    var = 'pr'
    region = 'Norcp Analysis Domain'

    # Target data
    var_conf_trgt = configuration_dict['target data']['variables'][var]
    target_conf = open_data.ReadInputData(configuration_dict['target data'])
    trgt_data = target_conf.read_data(var)

    masking_trgt_data = spatial_masking.SpatialMasking(trgt_data, var)
    trgt_msk_data = masking_trgt_data.get_mask(region, extract_data=True)

    res_freq, res_meth = var_conf_trgt['resample resolution']
    resample = resampling.Resampling(res_freq, res_meth)
    trgt_mask_resampled = resample.resample(trgt_msk_data)

    # Climate data
    var_conf_clim = configuration_dict['climatology data']['variables'][var]
    clim_conf = open_data.ReadInputData(
        configuration_dict['climatology data'])
    clim_data = clim_conf.read_data(var)

    masking_clm_data = spatial_masking.SpatialMasking(clim_data, var)
    clim_msk_data = masking_clm_data.get_mask(region, extract_data=True)

    res_freq, res_meth = var_conf_clim['resample resolution']
    resample = resampling.Resampling(res_freq, res_meth)
    clim_mask_resampled = resample.resample(clim_msk_data)

    
    """
    extreme_detection = event_detection_algorithms.ExtremeDetectionAlgorithm(algorithm, var)
    days_of_extreme_detected = extreme_detection.threshold_based_algorithm(filter_method, pctl_threshold, perc_of_days)

    Evaluation()

    PostProcessing()

    UnitTest()
    """


if __name__ == "__main__":
    main()
