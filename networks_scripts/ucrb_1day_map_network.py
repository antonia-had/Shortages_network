import os
import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import math


################################################################################################################
def make_day_network(date):
    # create network for a given day
    # format date as YYYY-MM-DD string

    data = pd.read_csv('daily_data/' + date + '.csv')

    # filter to select only users that were put out of priority that day
    data = data.loc[(data.analysisOutOfPriorityPercentOfDay > 0)]
    G = nx.from_pandas_edgelist(df=data, source='locationWdid', target='analysisWdid',  create_using=nx.DiGraph())

    return G

################################################################################################################

date = '2002-09-09'
G = make_day_network(date)

plt.figure(figsize = (12,8))
m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
pos = {}
for count, elem in enumerate(pos_data['nodes']):
     pos[elem] = (mx[count], my[count])
nx.draw_networkx_edges(G, pos = pos, edge_color='blue', alpha=0.1, arrows = False)
m.drawcountries(linewidth = 2)
m.drawstates(linewidth = 0.2)
m.drawcoastlines(linewidth=2)
plt.tight_layout()
plt.savefig("map.png", dpi = 300)
plt.show()
