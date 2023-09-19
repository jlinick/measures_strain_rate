#!/usr/bin/env python3

'''generates MEaSUREs mean data file'''

import os
import numpy as np
import netCDF4
import h5py
import xarray as xr
import dask
import datashader as ds
from functools import partial

def merge_folder(dirname, output_path='/products/mean.nc', crop_bounds=None, mean=True, verbose=True):
    dask.config.set(**{'array.slicing.split_large_chunks': True})    
    fils = [os.path.join(dirname, fil) for fil in os.listdir(dirname) if fil.endswith('.nc')]
    if verbose:
        print('merging {} netcdf files from {}...'.format(len(fils), dirname))
    partial_func = partial(_preprocess, crop_bounds=crop_bounds)
    if not crop_bounds is None and verbose:
        print('cropping dataset to {}...'.format(crop_bounds))
    if not crop_bounds is None:
        ds = xr.open_mfdataset(fils, combine='nested', parallel=True, compat='override', coords='minimal', concat_dim='time',engine='netcdf4', preprocess=partial_func)
    else:
        ds = xr.open_mfdataset(fils, combine='nested', parallel=True, compat='override', coords='minimal', concat_dim='time',engine='netcdf4')
    if mean == True:
        if verbose:
            print('generating mean...')
        ds = gen_mean(ds, verbose=verbose)
    if verbose:
        print('saving data to {}...'.format(output_path))
    ds.to_netcdf(output_path)

def _preprocess(ds, crop_bounds=None):
    if not crop_bounds is None:
        return crop(ds, crop_bounds)
    return ds

def gen_mean(ds, verbose=True) -> xr.DataArray:
    '''generates the mean along the fist axis for VX, VY, STDX, STDY, ERRX, ERRY, and then sums CNT.'''
    variables = ['VX', 'VY', 'STDX', 'STDY', 'ERRX', 'ERRY']
    for variable in variables:
        #first_dim = list(ds[variable].dims)[0]
        if verbose == True:
            print('applying mean of {} over {}'.format(variable, 'time'))
        ds[variable] = ds[variable].mean(dim='time', skipna=True) # take the mean
    ds['CNT'] = ds['CNT'].sum(dim='time', skipna=True) # sum of count
    return ds

def crop(ds, crop_bounds=((-1822691,723307),(-1657028,459924))):
    UL = crop_bounds[0]
    LR = crop_bounds[1]
    lats = [UL[1],LR[1]]
    lons = [UL[0],LR[0]]
    lat_bounds = [max(lats), min(lats)]
    lon_bounds = [min(lons), max(lons)]
    return ds.sel(y=slice(*lat_bounds), x=slice(*lon_bounds))

def save_h5(xarr, file_path):
    '''saves an xarray to the given path'''
    with h5py.File(file_path, 'w') as f:
        dset = f.create_dataset('data', data=xarr, chunks=True, compression="gzip")

def plot(data_array, file_path, width=3000, height=3000):
    canvas = ds.Canvas(plot_width=width, plot_height=height)
    agg = canvas.raster(data_array)
    img = tf.shade(agg, cmap=inferno)
    img.to_pil().save(file_path)

def print_xarr(ds):
    # Print global attributes and their values
    print("Global Attributes:")
    for attr_name, attr_value in ds.attrs.items():
        print(f"{attr_name}: {attr_value}")
    # Print each variable name and its mean value
    print("\nVariable Means:")
    for var_name, variable in ds.data_vars.items():
        try:
            mean_value = np.nanmean(variable)
            print(f"{var_name}: {variable.shape} {mean_value}")
        except:
            print(f"{var_name}: {variable.shape} {variable}")


if __name__ == '__main__':
    crop_bounds = ((-1952393,-63914), (-1143142,-641287)) # cropping region coordinates are UL, LR
    merge_folder('/data', output_path='/products/mean.nc', crop_bounds=None, verbose=True, mean=True)

