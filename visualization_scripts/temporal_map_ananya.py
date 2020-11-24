
import numpy as np
import cartopy.feature as cpf
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
import pandas as pd
import matplotlib.animation as animation
import math
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs

#read csv files with structures
# structures = pd.read_csv('../data/modeled_diversions.csv', index_col=0)
gauges = pd.read_csv("../data/div5_gauges.csv", index_col=0) #streamflow
stations = pd.read_csv("../data/CDSS_climate_stations.csv", index_col=0)

#read csv files with operational life in monthly time steps
# structures_life = pd.read_csv('../data/demands.csv', index_col=0)
gauges_life = pd.read_csv("../data/gauges_life_yrs.csv", index_col=0)
stations_life = pd.read_csv("../data/stations_life_yrs.csv", index_col=0)

#set up map
extent = [-109.069,-105.6,38.85,40.50]
rivers_10m = cpf.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
tiles = cimgt.Stamen('terrain-background')


fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=tiles.crs)
ax.add_feature(rivers_10m, facecolor='None', edgecolor='b')
ax.set_extent(extent)
ax.add_image(tiles,9)
diversion_clr='#003049'
gauge_clr = '#D62728'
climate_clr = '#FFD700'

#plot points
# structure_points = ax.scatter(structures['X'], structures['Y'], marker = '.', s = structures_life['0']*10, c = diversion_clr, transform=ccrs.PlateCarree())
gauge_points = ax.scatter(gauges['longitude'], gauges['latitude'], marker = '.', s = gauges_life['0']*100, c = gauge_clr, transform=ccrs.PlateCarree())
station_points = ax.scatter(stations['longitude'], stations['latitude'], marker = '.', s = stations_life['0']*100, c = climate_clr, transform=ccrs.PlateCarree())

#make legend showing number of active water rights and stations at given time step
l2 = ax.scatter(-110,37, s=50, c = gauge_clr, transform=ccrs.PlateCarree())
l4 = ax.scatter(-110,37, s=50, c = climate_clr,transform=ccrs.PlateCarree())
# gauge_label = ax.scatter(-110,37, s=0, transform=ccrs.PlateCarree())
# station_label = ax.scatter(-110,37, s=0, transform=ccrs.PlateCarree())
num_gauges = gauges_life['0'].sum
num_stations = stations_life['0'].sum
labels = [str(num_gauges) + ' Streamflow gauges', str(num_stations) + ' Climate stations']
legend = ax.legend([l2, l4], labels, ncol=2, loc = 'upper left', title = 'Year: '+ str(0+1893)+'\n', fontsize=10, title_fontsize = 14, borderpad=2, handletextpad = 1.3)


#update points through time
def update_points(num, gauge_points, station_points, legend):
    # structure_points.set_sizes(structures_life[str(num)] / 10)
    gauge_points.set_sizes(gauges_life[str(num)] * 100)
    station_points.set_sizes(stations_life[str(num)] * 100)

    #fix legend date
    # legend.set_title('Year: ' + str(num + 1893))
    g = gauges_life[str(num)].to_list()
    g = [int(ele) for ele in g]
    s = stations_life[str(num)].to_list()
    s = [int(ele) for ele in s]
    num_gauges = sum(g)
    num_stations = sum(s)
    labels = [str(num_gauges) + ' Streamflow gauges', str(num_stations) + ' Climate stations']
    legend = ax.legend([l2, l4], labels, ncol=2, loc='upper left', title='Year: ' + str(num + 1893) + '\n', fontsize=10,title_fontsize=14, borderpad=2, handletextpad=1.3)
    return gauge_points, station_points, legend


anim = animation.FuncAnimation(fig, update_points, 127, fargs=(gauge_points, station_points, legend), interval=200, blit=False)
anim.save('basin_animation_yrs.gif', fps=10, dpi=150, writer="Pillow")

