import sys
import os
from dask.distributed import Client
from xtrdet.methods import event_detection_algorithms
from xtrdet.preproc import get_configuration
from xtrdet.utils import open_data
from xtrdet.utils import write_data
from xtrdet.utils import resampling
from xtrdet.utils import spatial_masking
from xtrdet.postproc import plot_results


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
        cluster = slurm_cluster_setup(nodes=nnodes, log_directory=log_dir, **sl_kwargs)
    else:
        print("\n\tCluster type not implemented! Exiting..")
        sys.exit()

    client = Client(cluster)

    # Get Settings
    target_conf = configuration_dict['target data']
    target_variable_conf = target_conf['variables']
    trgt_name = target_conf['data name']

    climate_conf = configuration_dict['climatology data']
    climate_variable_conf = climate_conf['variables']
    clim_name = climate_conf['data name']

    region = configuration_dict['region']

    for tgvar, clvar in zip(target_variable_conf, climate_variable_conf):

        fn = f"target.{trgt_name}.{tgvar}_climtlgy.{clim_name}.{clvar}"
        if region is not None:
            fn = f"{fn}.{region.replace(' ', '_')}"

        var_conf_trgt = target_variable_conf[tgvar]
        var_conf_clim = climate_variable_conf[clvar]

        # Target data
        trgt_data_dd = open_data.ReadInputData(target_conf)
        trgt_data = trgt_data_dd.read_data(tgvar)

        if region is not None:
            masking_tgt_data = spatial_masking.SpatialMasking(trgt_data, tgvar)
            trgt_data = masking_tgt_data.get_mask(region, extract_data=True)

        if var_conf_trgt['resample resolution'] is not None:
            res_freq, res_meth = var_conf_trgt['resample resolution']
            resample = resampling.Resampling(res_freq, res_meth)
            trgt_data = resample.resample(trgt_data)

        # Climate data
        clim_data_dd = open_data.ReadInputData(climate_conf)
        clim_data = clim_data_dd.read_data(clvar)

        if region is not None:
            masking_clm_data = spatial_masking.SpatialMasking(clim_data, clvar)
            clim_data = masking_clm_data.get_mask(region, extract_data=True)

        if var_conf_clim['resample resolution'] is not None:
            res_freq, res_meth = var_conf_clim['resample resolution']
            resample = resampling.Resampling(res_freq, res_meth)
            clim_data = resample.resample(clim_data)

        # Run algorithm
        algorithm = configuration_dict['detection method']
        method_args = configuration_dict['method args']

        event_detection = event_detection_algorithms.ExtremeDetectionAlgorithm(
            algorithm, method_args, clim_data, clvar, trgt_data, tgvar)
        results = event_detection.run_algorithm()

        # Write results to file
        write = write_data.WriteData(results, algorithm, outdir, fn)
        write.save_data()

        # Plot results
        plot_results.map_extreme_detected(tgvar, results, '', configuration_dict['map configure'], outdir)
 

    client.close()


if __name__ == "__main__":
    main()
