import argparse as ap


import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr
from cartopy.mpl.gridliner import (LATITUDE_FORMATTER, LONGITUDE_FORMATTER,
                                   Gridliner)
from IPython import embed
from .process_era5 import read_data
import matplotlib as mpl

def draw_map_orogaphic_east_asia(ax):
    ylocator = mpl.ticker.FixedLocator([-20,0,20,40,60,80])
    xlocator = mpl.ticker.FixedLocator([-150,-130,-100,-70,-40,-10,20,50,80,110,140,170])
    # yformatter=mpl.ticker.FixedFormatter([(80,-20),(80,0),(80,20),(80,40),(80,60),(80,80)])

    ax.coastlines('110m')
    gl=ax.gridlines(transform = ccrs.PlateCarree(), linestyle ='--', draw_labels=False,ylocs=ylocator,linewidth=2,
                            xlocs=xlocator)
    return ax

def draw_map(ax=None, top_labels=False, right_labels=False):
    if ax==None:
        ax=plt.gca()
    gl = ax.gridlines(transform = ccrs.PlateCarree(), draw_labels = True, linestyle ='--')
    gl.top_labels = top_labels
    gl.right_labels = right_labels
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    ax.coastlines('110m', color='gray', alpha=0.8)
    return ax 

def plot_contour(da,ax=None, colors='black', levels=None, **kwargs):
    if ax == None:
        ax = plt.gca()

    
    if type(levels) is np.ndarray:
        levels=levels
        im = ax.contour(da['longitude'],da['latitude'],da,transform=ccrs.PlateCarree()
                    ,levels=levels, colors=colors,zorder=1000)
    else:
        im = ax.contour(da['longitude'],da['latitude'],da,transform=ccrs.PlateCarree(), colors=colors, zorder=1000)
        levels=im.levels
    ax.clabel(im, levels, inline=True, fmt='%d')
    return im

def plot_contourf(da, ax=None, cmap='viridis',**kwargs):
    if ax == None:
        ax = plt.gca()
    im =ax.contourf(da['longitude'],da['latitude'],da ,transform=ccrs.PlateCarree(), cmap=cmap,**kwargs)

    return im 

def plot_pcolormesh(da, ax=None, cmap='viridis'):
    """
    Create pcolormesh plot

    """

    if ax==None:
        ax=plt.gca()
 
    da.plot.pcolormesh(ax=ax,transform=ccrs.PlateCarree(), cmap=cmap)

    return ax



def plot_geopot_temperature(ax,temp_winter, temp_summer,geopot_winter,geopot_summer, extent=None):

    ds_temp_winter=read_data(temp_winter)
    ds_temp_summer=read_data(temp_summer)
    ds_geopot_winter=read_data(geopot_winter) 
    ds_geopot_summer=read_data(geopot_summer)
    da_temp_winter = ds_temp_winter[ds_temp_winter.varName]
    da_temp_summer = ds_temp_summer[ds_temp_summer.varName]
    da_geopot_winter=ds_geopot_winter[ds_geopot_winter.varName]
    da_geopot_summer=ds_geopot_summer[ds_geopot_summer.varName]
    min_gepot=np.ceil(da_geopot_winter.min()/10)*10
    max_gepot=np.ceil(da_geopot_summer.max()/10)*10
    levels= np.arange(min_gepot,max_gepot,np.round((max_gepot-min_gepot)/5))

    vmin=np.floor(da_temp_winter.min()/10)*10
    vmax=np.floor(da_temp_summer.max()/10)*10
    ax[0]=draw_map(ax[0])
    ax[1]=draw_map(ax[1])
    if extent:
        for axes in ax:
            axes.set_extent(extent)
            axes.set_aspect('auto')
    ax[0].text(0.05,0.88,'a)',transform=ax[0].transAxes, fontsize=14)
    ax[1].text(0.05,0.88,'b)',transform=ax[1].transAxes, fontsize=14)

    ax[0].text(0.9,0.88,'JJA',transform=ax[0].transAxes, fontsize=14, color='white')
    ax[1].text(0.9,0.88,'DJF',transform=ax[1].transAxes, fontsize=14, color='white')

    plot_contourf(da_temp_winter,ax[1],vmax=vmax,vmin=vmin, extend='both')
    plot_contour(da_geopot_winter,ax[1],levels=levels)
    plot_contour(da_geopot_summer,ax[0],levels=levels)
    im=plot_contourf(da_temp_summer,ax[0],vmin=vmin,vmax=vmax, extend='both')

    return ax, im

