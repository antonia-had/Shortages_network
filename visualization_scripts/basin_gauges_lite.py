#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon October 12 2020

@author: Ananya Gangadhar
Adapted from Antonia's basin_model_representation.py
"""
import pandas as pd
import cartopy.io.img_tiles as cimgt
import matplotlib.pyplot as plt
import numpy as np
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

# StateMod diversion locations
structures = pd.read_csv('../data/modeled_diversions.csv',index_col=0)

# Important streamflow gauge locations
gauges = pd.read_csv('../data/importantgages.csv', index_col=1)

'''
Map setup
'''
# map extent
extent = [-109.125,-105.625,38.875,40.50]

# background map tiles
tiles = cimgt.Stamen('terrain-background')
# MosartWM gridcells
xlist = np.linspace(-109.125,-105.625, 29)
ylist = np.linspace(38.875, 40.50, 17)
X, Y = np.meshgrid(xlist, ylist)
Xgrid = np.arange(128, 156)
Ygrid = np.arange(112,128)
Z = np.ones([len(Ygrid), len(Xgrid)])
#Basin shape
shape_feature = ShapelyFeature(Reader('../data/Water_Districts.shp').geometries(),
                               ccrs.PlateCarree(), edgecolor='black', facecolor='None')
#Stream lines
flow_feature = ShapelyFeature(Reader('../data/UCRBstreams.shp').geometries(),
                              ccrs.PlateCarree(), edgecolor='royalblue', facecolor='None')

'''
Figure generation
'''
mosart_clr='#D62828'
statemod_clr='#003049'
gauge_clr = '#D62728'

fig = plt.figure(figsize=(18, 12))
ax = plt.axes(projection=tiles.crs)
# Set map extent
ax.set_extent(extent,crs=ccrs.Geodetic())
# Draw background tiles
ax.add_image(tiles,9)
# Draw basin
ax.add_feature(shape_feature, facecolor='#a1a384', alpha = 0.6)
# Draw streams
ax.add_feature(flow_feature, alpha = 0.8, linewidth=1.5, zorder=4)
# Draw grid
ax.pcolor(X, Y, Z, facecolor='none', edgecolor='grey', alpha=0.5, linewidth=0.5, transform=ccrs.PlateCarree())
# Draw StateMod nodes
stru = ax.scatter(structures['X'], structures['Y'], marker = '.', s = 200,
           c =statemod_clr, transform=ccrs.PlateCarree(),zorder=5)
gaug = ax.scatter(gauges['LongDecDeg'], gauges['LatDecDeg'], marker = '.', s = 200, c = gauge_clr,
           transform=ccrs.PlateCarree(),zorder=5)
ax.legend((stru, gaug),('Diversion Structures', 'Important Gauges'))
plt.savefig('basin_gauges_lite.png')