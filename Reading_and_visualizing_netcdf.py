#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 18:29:45 2024

@author: yagizcanurkmezz
"""

import netCDF4 as nc

#%% Giving path for reading

ds_cmip6 = "/Users/yagizcanurkmez/Desktop/cmip6_ssp2/pr_Amon_CNRM-CM6-1_ssp245_r1i1p1f2_gr_20240116-20241216_v20190219.nc" 

ds_ERA5 = "/Users/yagizcanurkmez/Desktop/cmip6_ssp2/era_tp_10years.nc"

#%% Reading from path

data_CMIP6 = nc.Dataset(ds_cmip6)
data_ERA5 = nc.Dataset(ds_ERA5)

print(data_CMIP6) # See information about data and find abbrevation of variables
print(data_ERA5)


#%% Extracting Variables we want (Latitudes, Longitudes and Precipitation)

lat_cmip6 = data_CMIP6["lat"][:]  # : means all of data , if you want get spesific area, you can write as [0:10] for example
lon_cmip6 = data_CMIP6["lon"][:]
lat_era = data_CMIP6["lat"][:]  
lon_era = data_CMIP6["lon"][:]
prec_cmip6 = data_CMIP6["pr"][:]*31*24*60*60 # Multiplied for unit we want 
prec_era5 = data_ERA5["tp"][:]

#%% Make a visualization

import matplotlib.pyplot as plt
import cartopy.crs as ccrs


fig, ax = plt.subplots(figsize=(10,20),subplot_kw={'projection': ccrs.PlateCarree()})
ax.coastlines()
fn = ax.pcolormesh(lon_cmip6[:],lat_cmip6[:],prec_cmip6[0,:,:],cmap= "BuGn" ,vmax=200,vmin=-0)
cb=plt.colorbar(fn,orientation="horizontal",anchor=(0, 2), shrink=1)
cb.set_label("mm/month")
ax.set_title("Precipitation Expectation January 2024 according to CNRM SSP2-4.5")

