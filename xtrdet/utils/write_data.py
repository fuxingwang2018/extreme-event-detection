import os


class WriteData(object):
    """
    Write data to netcdf
    """

    def __init__(self, data, method, outpath, fprx):

        self.data = data
        self.outpath = outpath
        self.fprx = fprx
        self.method = method

    def save_data(self):
        save_funcs = {
            'threshold_optim': self.save_threshold_optim_output,
            'extreme_forecast_index': self.save_efi_output,
            'machine_learning_based_algorithm':
            self.save_threshold_optim_output
        }

        save_funcs[self.method](self.data, self.outpath)

    def save_threshold_optim_output(self, data, outpath):
        fname = f"{self.fprx}.{self.method}.nc"
        data.to_netcdf(os.path.join(self.outpath, fname))

    def save_efi_output(self, data, outpath):
        fname = f"{self.fprx}.efi.nc"
        data.to_netcdf(os.path.join(self.outpath, fname))
