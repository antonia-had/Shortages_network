import pandas as pd
import os
import networkx as nx


'''Function that creates a network with edge and node attributes for a given year'''

def make_year_network(year):
    # enter year in YYYY string format

    node_attr = pd.read_csv('../data/Attributes.csv')
    # print(water_rights.WDID.to_list())
    path = '../R_networks_scripts/network_csv_files/priorityWdid/v2_network_'
    data = pd.read_csv(path + year + '.csv')

    G = nx.from_pandas_edgelist(df=data, source='priorityWdid', target='analysisWdid', edge_attr = 'sum_wtd_count',
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