#!/usr/bin/env python3

'''generates strain rate products from MEaSUREs data'''

import os
import re
import numpy as np
import xarray as xr
import iceutils as ice
import dask
import datashader
import datashader.transfer_functions as tf
from datashader.colors import inferno

class data:
    
    def __init__(self, path, product_dir='/products', verbose=True):
        '''loads the data file, generates strain products, and outputs a strain netcdf with plots'''
        self.product_dir = product_dir
        self.output_path = os.path.join(product_dir, 'strain.nc')
        if not os.path.exists(self.output_path):
            dask.config.set(**{'array.slicing.split_large_chunks': True})
            self.ds = xr.open_dataset(path, chunks={})
            if verbose:
                print('Generating stress/strain arrays. This may take some time...')
            self.gen_stress_strain()
            self.save()
        else:
            self.ds = xr.open_dataset(self.output_path, chunks={})
        self.save_plots(verbose=verbose)

    @property
    def vx(self):
        return self.ds['VX']
    
    @property
    def vy(self):
        return self.ds['VY']

    @property
    def shape(self):
        return self.ds['VX'].shape

    @property
    def dy(self):
        res = self.ds.attrs.get('spatial_resolution', None)
        return float(re.search(r"(\d+(\.\d+)?)", res).group(1))

    @property
    def dx(self):
        res = self.ds.attrs.get('spatial_resolution', None)
        return float(re.search(r"(\d+(\.\d+)?)", res).group(1))

    def gen_stress_strain(self):
        strain, stress = ice.stress.compute_stress_strain(self.vx, self.vy, dx=self.dx, dy=self.dy, rotate=True)
        for item in strain.keys():
            self.ds[item] = strain[item]

    def save(self):
        self.ds.to_netcdf(self.output_path)

    def save_plots(self, verbose=True):
        names = {'eta': 'effective_dynamic_viscosity', 'e_xx': 'longitudinal_strain_rate', 'e_yy': 'transverse_strain_rate', 'e_xy': 'shear_strain_rate', 'effective': 'effective_strain_rate',
                'dilatation': 'dilatation', 't_xx': 'longitudinal_stress', 't_yy': 'transverse_stress', 't_xy': 'effective_stress'}
        for var_name, variable in self.ds.data_vars.items():
            if var_name in names.keys():
                var_name = names.get(var_name, 'unknown')
            # correct for 3 dimensional arrays
            if len(variable.shape) > 2:
                variable = np.nanmean(variable, axis=0)
            outpath = os.path.join(self.product_dir, var_name + '.png')
            plot(variable, outpath, verbose=verbose)

def plot(data_array, file_path, max_res=2000., verbose=True):
    if isinstance(data_array, np.ndarray):
        data_array = xr.DataArray(data_array)
    if verbose:
        # if array is huge, decrease it's shape to max_res
        r,c = data_array.shape
        h, w = r, c 
        if float(r) * float(c) > float(max_res) * float(max_res):
             ratio = float(r)/float(c)
             h = int(max_res * ratio)
             w = int(max_res)
             if ratio > 1.:
                 h = int(max_res)
                 w = int(max_res / ratio)
        if verbose:
            print('width: {}, height: {}, ratio: {}'.format(w, h, ratio))
            print('saving to {}'.format(file_path))
    canvas = datashader.Canvas(plot_width=w, plot_height=h)
    agg = canvas.raster(data_array)
    img = tf.shade(agg, cmap=inferno)
    img.to_pil().save(file_path)


if __name__ == '__main__':
    data('/products/mean.nc', product_dir='/products/')