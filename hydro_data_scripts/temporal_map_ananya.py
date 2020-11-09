
import numpy as np
import cartopy.feature as cpf
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.img_tiles as cimgt
import pandas as pd
import matplotlib.animation as animation
import math

gauges = pd.read_csv('../data/div5_gauges.csv', index_col=0, skiprows=2)
#######################
extent = [-109.069,-105.6,38.85,40.50]
rivers_10m = cpf.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m')
tiles = cimgt.Stamen('terrain-background')

fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=tiles.crs)
ax.add_feature(rivers_10m, facecolor='None', edgecolor='b')

ax.set_extent(extent)
################################
gauge_points = ax.scatter(gauges['longitude'], gauges['latitude'], marker = '.', s = 5, c = 'dodgerblue', transform=ccrs.PlateCarree())

# l2 = ax.scatter(-110,37, s=demands.values.max()/50, c = 'dodgerblue', transform=ccrs.PlateCarree())
# l4 = ax.scatter(-110,37, s=shortages.values.max()/50, c = 'coral',transform=ccrs.PlateCarree())
# dem_label = ax.scatter(-110,37, s=0, transform=ccrs.PlateCarree())
# short_label = ax.scatter(-110,37, s=0, transform=ccrs.PlateCarree())
# labels = ['Max Demand' , str(demands.values.max()) + ' af',
#           'Max Shortage' , str(shortages.values.max()) + ' af']
legend = ax.legend([dem_label, l2, short_label, l4], labels, ncol=2, loc = 'upper left', title = 'Month: '+ str((0 + 10) % 12 +1) + '/' + str(int(math.floor(0/12))+1908)+'\n', fontsize=10, title_fontsize = 14, borderpad=2, handletextpad = 1.3)


def update_points(num, gauge_points, legend):
    gauge_points.set_sizes()
    legend.set_title('Month: ' + str((num + 10) % 12 + 1) + '/' + str(int(math.floor(num / 12)) + 1908))
    return legend, gauge_points


anim = animation.FuncAnimation(fig, update_points, 120, fargs=(gauge_points, legend), interval=200, blit=False)
anim.save('gauges_animation.gif', fps=10, dpi=150, writer="Pillow")
