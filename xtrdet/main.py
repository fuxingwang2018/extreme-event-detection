import sys
import os
from dask.distributed import Client
from xtrdet.methods import event_detection_algorithms
from xtrdet.preproc import get_configuration
from xtrdet.utils import open_data
from xtrdet.utils import write_data
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
    Returns
    -------
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

    # os.system('ulimit -c')

    # Get configuration
    args = get_configuration.get_args()
    config_file = args.config
    if not os.path.isfile(config_file):
        raise ValueError(f"\nConfig file, '{config_file}', does not exist!")
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
        log_dir = configuration_dict['log dir']
        sl_kwargs = configuration_dict['cluster kwargs']
        cluster = slurm_cluster_setup(nodes=nnodes, log_directory=log_dir,
                                      **sl_kwargs)
    else:
        print("\n\tCluster type not implemented! Exiting..")
        sys.exit()

    client = Client(cluster)

    # Get Settings
    data_config = configuration_dict['data config']
    variable_config = data_config['variables']
    data_source = data_config['data source']

    region = configuration_dict['region']

    for var in variable_config:

        fn = f"event_detection.{data_source.replace(' ', '_')}.{var}"
        if region is not None:
            fn = f"{fn}.{region.replace(' ', '_')}"

        # Read data
        data_dd = open_data.ReadInputData(data_config)
        trgt_data, clim_data = data_dd.read_data(var)

        if region is not None:
            masking_trgt_data = spatial_masking.SpatialMasking(trgt_data, var)
            trgt_data = masking_trgt_data.get_mask(region, extract_data=True)
            masking_clm_data = spatial_masking.SpatialMasking(clim_data, var)
            clim_data = masking_clm_data.get_mask(region, extract_data=True)

        if variable_config[var]['resample resolution'] is not None:
            res_freq, res_meth = variable_config[var]['resample resolution']
            resample = resampling.Resampling(res_freq, res_meth)
            trgt_data = resample.resample(trgt_data)
            clim_data = resample.resample(clim_data)

        # Run algorithm
        algorithm = configuration_dict['detection method']
        method_args = configuration_dict['method args']

        event_detection = event_detection_algorithms.ExtremeDetectionAlgorithm(
            data_source, algorithm, method_args, clim_data, trgt_data, var)
        results = event_detection.run_algorithm()

        # Write results to file
        write = write_data.WriteData(results, algorithm, outdir, fn)
        write.save_data()

    client.close()


if __name__ == "__main__":
    main()
