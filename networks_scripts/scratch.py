import os
import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from matplotlib.gridspec import GridSpec
import math

date = '2002-09-09'
# day_water_rights(date)

# make a list of graph edges as tuple pairs

rights_data = pd.read_csv(date + '.csv')
# select only those rights that were put out of priority on that day
rights_data = rights_data.loc[rights_data['analysisOutOfPriorityPercentOfDay'] > 0]
edges = rights_data[['analysisWdid', 'locationWdid']]

# convert  df to list of tuples
edges = edges.astype('int64').to_records(index=False)

# create network graph
G = nx.Graph()
edges = edges[:30] #only focusing on a few edges
G.add_edges_from(edges)

# obtain volume of water used by each user/node
water_rights = pd.read_csv('../data/CDSS_WaterRights.csv')
vol = water_rights[['WDID', 'Net Absolute']]

# add node attributes
nodes = list(G.nodes)
print(nodes)

for n in nodes:
    size = vol.loc[vol['WDID'] == n]['Net Absolute']
    if len(size.values) != 0:
        G.node[n]['size'] = int(max(size.values)/100000)
    else:
        G.node[n]['size'] = 0


sizes = nx.get_node_attributes(G, "size")
print(sizes.values())

print(sorted(G.nodes(data=True), key=lambda x: x[1]['size'], reverse=True))

new_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['size'], reverse=True)
n = int(math.ceil(len(new_nodes)/10))
new_nodes = new_nodes[:n]
new_nodes = [node[0] for node in new_nodes]
print(new_nodes)

Gcc = G.subgraph(new_nodes)

print(list(Gcc.nodes))



