import networkx as nx
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt



################################################################################################################
'''Function that creates a network with edge and node attributes for a given year'''

def make_year_network(year):
    # enter year in YYYY string format

    node_attr = pd.read_csv('../data/Attributes.csv')
    # print(water_rights.WDID.to_list())
    path = 'yearly_networks_v2/network_'
    data = pd.read_csv(path + year + '.csv')

    G = nx.from_pandas_edgelist(df=data, source='priorityWdid', target='analysisWdid', edge_attr = 'priority_sum_wtd_count',
                                create_using=nx.DiGraph())
    # add latitude for each node
    lat_dict = node_attr[['wdid', 'latitude']].set_index('wdid')['latitude'].to_dict()
    nx.set_node_attributes(G, name = 'latitude', values = lat_dict)

    # add longitude for each node
    long_dict = node_attr[['wdid', 'longitude']].set_index('wdid')['longitude'].to_dict()
    nx.set_node_attributes(G, name = 'longitude', values = long_dict)

    # add net absolute for each node
    vol_dict = node_attr[['wdid', 'sum_netAbs']].set_index('wdid')['sum_netAbs'].to_dict()
    nx.set_node_attributes(G, name='netAbs', values=vol_dict)

    # add label for each node
    label_dict = node_attr[['wdid', 'structureName']].set_index('wdid')['structureName'].to_dict()
    nx.set_node_attributes(G, name='name', values=label_dict)

    return G


###################################################################################################################

'''Create network'''


years = [str(yr) for yr in range(2000, 2020)]
print(years)

for year in years:
    print(year)
    G = make_year_network(year)

    # relabel nodes with structure names underscored instead of wdids because R doesnt like col names that start with numbers
    mapping = {i: G.node[i]['name'].replace(" ", "_") for i in G.nodes()}
    print(mapping)
    H = nx.relabel_nodes(G, mapping)

    # only select top 100 nodes by degree
    degree = H.degree()
    N = 100
    top_nodes = sorted(degree, key=lambda x: x[1], reverse=True)[:N]
    top_nodes_list = [n for n, d in top_nodes]
    Hcc = H.subgraph(top_nodes_list)

    A = nx.to_pandas_adjacency(Hcc)
    print(A.head())
    A.to_csv('../R_scripts/' + year+'_adj_matrix.csv')
