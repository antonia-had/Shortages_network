# finds daily user networks with interesting properties in a given year

import networkx as nx
import os
import pandas as pd
import csv
import numpy as np


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


###################################################################################################################

def measure_network_props(G):
    # returns a dictionary of centrality measure values for a given undirected networkx graph
    props = {} # dictionary where each centrality measure is a key

    # 1. in_degree_centrality(G)
    try:
        props['in_degree_centrality'] = nx.in_degree_centrality(G)
    except:
        print("Something went wrong with in degree_centrality")
        props['in_degree_centrality'] = {}

    try:
        props['out_degree_centrality'] = nx.out_degree_centrality(G)
    except:
        print("Something went wrong with out degree_centrality")
        props['out_degree_centrality'] = {}

    # 2. eigenvector_centrality(G, max_iter=100, tol=1e-06, nstart=None, weight=None)
    try:
        props['eigenvector_centrality'] = nx.degree_centrality(G)
    except:
        print("Something went wrong with eigenvector_centrality")
        props['eigenvector_centrality']= {}

    # 3. closeness_centrality(G, u=None, distance=None, wf_improved=True)
    try:
        props['closeness_centrality'] = nx.closeness_centrality(G)
    except:
        print("Something went wrong with closeness_centrality")
        props['closeness_centrality'] = {}

    # 4. betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    try:
        props['betweenness_centrality'] = nx.betweenness_centrality(G)
    except:
        print("Something went wrong with betweenness_centrality")
        props['betweenness_centrality'] = {}

    # 5. communicability_betweenness_centrality(G, normalized=True)
    try:
        props['communicability_betweenness_centrality'] = nx.communicability_betweenness_centrality(G)
    except:
        print("Something went wrong with communicability_betweenness_centrality")
        props['communicability_betweenness_centrality'] = {}

    # 6. load_centrality(G, v=None, cutoff=None, normalized=True, weight=None)
    try:
        props['load_centrality'] = nx.load_centrality(G)
    except:
        print("Something went wrong with load_centrality")
        props['load_centrality'] = {}

    # 7. second_order_centrality(G)
    try:
        props['second_order_centrality'] = nx.second_order_centrality(G)
    except:
        print("Something went wrong with second_order_centrality")
        props['second_order_centrality'] = {}

        # 1st q, median, 3rd q, max, min, mean



    return props

################################################################################################################

'''ACTUAL NON-FUNCTION CODE'''

path = 'yearly_networks/'
years_list = os.listdir(path)
years_list.remove('.DS_Store')
# years_list = ['network_2008.csv']

stats = []
for year in years_list:
    print(year)
    print(year[8:12])
    G = make_year_network(year[8:12])
    props = measure_network_props(G)

    for prop, v in props.items():
        d = {'prop': '', '1st_q': 0, 'median': 0, '3rd_q': 0, 'max': 0, 'min': 0, 'mean': 0}
        vl = list(v.values())
        vl = sorted(vl)
        # print(vl)
        d['year'] = year[8:12]
        d['prop'] = prop

        if vl:
            # exclude empty lists
            # print(vl)
            d['1st_q'] = np.percentile(vl, 25)
            d['median'] = np.percentile(vl, 50)
            d['3rd_q'] = np.percentile(vl, 75)
            d['max'] = max(vl)
            d['min'] = min(vl)
            d['mean'] = np.mean(vl)
        stats += [d]

df = pd.DataFrame(stats)
print(df.head)

df.to_csv('../data/network_properties.csv', index = False)

