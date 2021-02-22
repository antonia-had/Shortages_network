# create a network of which user put the other out of priority on a given day

import os
import pandas as pd
import networkx as nx
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import math

def day_water_rights(date = '2002-09-09'):
    # returns .csv file showing all calls for a particular day
    # format date as YYYY-MM-DD string

    # import os
    # import pandas as pd
    # import csv

    date += 'T00:00:00.0000000'
    path = '../water_right_scripts/fetched_data'
    users_list = os.listdir(path)
    users_list.sort()
    users_list = users_list[1:]  # removes .DS store file name
    # users_list = users_list[:20]

    rows = []
    for user in users_list:
        print(user)
        user_info = pd.read_csv(path + '/' + user, dtype=object, error_bad_lines=False)
        row = user_info.loc[user_info['analysisDate'] == date]
        rows += row.values.tolist()

    # print(rows)

    # create .csv file for results of that 1 day
    col_names = list(user_info.columns)

    with open(date[:10] + '.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(col_names)
        write.writerows(rows)

        return
######################################

# call function
date = '2002-04-18'
# day_water_rights(date)

# make a list of graph edges as tuple pairs

rights_data = pd.read_csv(date + '.csv')
# select only those rights that were put out of priority on that day
rights_data = rights_data.loc[rights_data['analysisOutOfPriorityPercentOfDay'] > 0]
edges = rights_data[['analysisWdid', 'locationWdid']]

# convert  df to list of tuples
edges = edges.astype('int64').to_records(index=False)
# print(edges)

# create network graph
G = nx.Graph()
# edges = edges[:50] #only focusing on a few edges
G.add_edges_from(edges)

print(G.number_of_nodes())

# obtain volume of water used by each user/node
water_rights = pd.read_csv('../data/CDSS_WaterRights.csv')
vol = water_rights[['WDID', 'Net Absolute']]

# add node attributes
nodes = list(G.nodes)
print(nodes)

for n in nodes:
    size = vol.loc[vol['WDID'] == n]['Net Absolute']
    if len(size.values) != 0:
        G.node[n]['size'] = int((max(size.values)))/10**6
    else:
        G.node[n]['size'] = 0

sizes = nx.get_node_attributes(G, "size")


###################

degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of graph", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = GridSpec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
# Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

# Plot only the top 10% of users based on allocation amount
new_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['size'], reverse=True)

n = int(math.ceil(len(new_nodes)/1))
new_nodes = new_nodes[:n]
new_nodes = [node[0] for node in new_nodes]
# make sure the central nodes are included in this list
imp_nodes = sorted([(n,d) for n, d in G.degree()], reverse=True, key=lambda x: x[1])[:3]
new_nodes += [node[0] for node in imp_nodes]
new_nodes = list(set(new_nodes))
print(new_nodes)


Gcc = G.subgraph(new_nodes)
sizes = nx.get_node_attributes(Gcc, "size")
print(sizes)

pos = nx.spring_layout(Gcc, seed=1039651)
# set node size


# set node colors


nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=sizes.values(), node_color=range(Gcc.number_of_nodes()),  cmap=plt.cm.Blues)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.2)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

# place a text box in upper left in axes coords
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax0.text(0.05, 0.95, date, transform=ax0.transAxes, fontsize=14, verticalalignment='top', bbox=props)

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
# ax2.set_ylim([0, 200])
# ax2.set_xlim([0,150])
ax2.set_yscale('log')
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.savefig('network_1day.png')

print(Gcc.edges())