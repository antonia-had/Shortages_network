import os
import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import math


################################################################################################################
def make_year_network(year):
    # enter year in YYYY string format

    node_attr = pd.read_csv('../data/Attributes.csv')
    # print(water_rights.WDID.to_list())
    path = 'yearly_networks/network_'
    data = pd.read_csv(path + year + '.csv')

    G = nx.from_pandas_edgelist(df=data, source='locationWdid', target='analysisWdid', edge_attr = 'sum_wtd_count',
                                create_using=nx.DiGraph())
    # add latitude for each node
    lat_dict = node_attr[['wdid', 'latitude']].set_index('wdid')['latitude'].to_dict()
    nx.set_node_attributes(G, name = 'latitude', values = lat_dict)

    # # add longitude for each node
    long_dict = node_attr[['wdid', 'longitude']].set_index('wdid')['longitude'].to_dict()
    nx.set_node_attributes(G, name = 'longitude', values = long_dict)

    # # add net absolute for each node
    vol_dict = node_attr[['wdid', 'sum_netAbs']].set_index('wdid')['sum_netAbs'].to_dict()
    nx.set_node_attributes(G, name='netAbs', values=vol_dict)

    return G

year = '2000'
G = make_year_network(year)
# print(G.nodes())
print(G.node[5103660]['latitude'], G.node[5103660]['longitude'], G.node[5103660]['netAbs'])

###################################################################################################################

# date = '2002-09-09'
# G = make_day_network(date)
#
# plt.figure(figsize = (12,8))
# m = Basemap(projection='merc',llcrnrlon=-160,llcrnrlat=15,urcrnrlon=-60,
# urcrnrlat=50, lat_ts=0, resolution='l',suppress_ticks=True)
# mx, my = m(pos_data['lon'].values, pos_data['lat'].values)
# pos = {}
# for count, elem in enumerate(pos_data['nodes']):
#      pos[elem] = (mx[count], my[count])
# nx.draw_networkx_edges(G, pos = pos, edge_color='blue', alpha=0.1, arrows = False)
# m.drawcountries(linewidth = 2)
# m.drawstates(linewidth = 0.2)
# m.drawcoastlines(linewidth=2)
# plt.tight_layout()
# plt.savefig("map.png", dpi = 300)
# plt.show()
