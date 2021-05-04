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
    path = 'network_csv_files/priorityWdid/v2_network_'
    data = pd.read_csv(path + year + '.csv')

    G = nx.from_pandas_edgelist(df=data, source='priorityWdid', target='analysisWdid', edge_attr = 'sumWtdCount',
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

'''Plot network graph'''

def plot_network_graph(G, year):
    # creates gridspec plot for a given network G
    fig = plt.figure(figsize=(18, 12))
    gspec = GridSpec(nrows=6, ncols=9)
    fig.suptitle(year, fontsize=24, fontweight='bold')
    plt.rcParams.update({'font.size': 12})

    # map extent
    extent = [-109.125, -105.625, 38.875, 40.50]
    # background map tiles
    tiles = cimgt.Stamen('terrain-background')
    # MosartWM gridcells
    xlist = np.linspace(-109.125, -105.625, 29)
    ylist = np.linspace(38.875, 40.50, 17)
    X, Y = np.meshgrid(xlist, ylist)
    Xgrid = np.arange(128, 156)
    Ygrid = np.arange(112, 128)
    Z = np.ones([len(Ygrid), len(Xgrid)])
    # Basin shape
    shape_feature = ShapelyFeature(Reader('../data/Water_Districts.shp').geometries(),
                                   ccrs.PlateCarree(), edgecolor='black', facecolor='None')
    # Stream lines
    flow_feature = ShapelyFeature(Reader('../data/UCRBstreams.shp').geometries(),
                                  ccrs.PlateCarree(), edgecolor='royalblue', facecolor='None', alpha=0.5, zorder=1)

    # 1. SUBPLOT OF NETWORK MAP
    # the first subplot will span 6 rows and 4 columns, top left
    crs = ccrs.PlateCarree()
    ax0 = fig.add_subplot(gspec[:, :], projection=crs)

    # Set map extent
    ax0.set_extent([-109.125, -105.625, 38.875, 40.50])
    # Draw background tiles
    ax0.add_image(tiles, 9)
    # Draw basin
    ax0.add_feature(shape_feature, facecolor='#a1a384', alpha=0.5)
    # Draw streams
    ax0.add_feature(flow_feature, alpha=0.7, linewidth=1.5, zorder=1)
    # Draw grid
    # ax0.pcolor(X, Y, Z, facecolor='none', edgecolor='grey', alpha=0.1, linewidth=0.5, transform=ccrs.PlateCarree())




    # Get latitude and longitude attributes for each node
    latitude = nx.get_node_attributes(G, 'latitude')
    longitude = nx.get_node_attributes(G, 'longitude')
    ds = [longitude, latitude]
    pos = {}
    for k in latitude.iterkeys():
        pos[k] = tuple(d[k] for d in ds)
    print(pos)

    Gcc = G

    # Color nodes by out degree
    degs = Gcc.out_degree() # Dict with Node ID, Degree
    nod = Gcc.nodes()
    color = np.asarray([degs[n] for n in nod])
    # print(sorted(color, reverse=True))

    # Size nodes by net absolute volume log-scaled and set size of nodes with out_degree = 0 to 0
    net_abs = nx.get_node_attributes(Gcc, 'netAbs')
    sizes = [np.log10(net_abs[i])*40 if net_abs[i] > 0 and Gcc.out_degree(i) > 0 else 0 for i in Gcc.nodes]

    # Size edge widths by sumWtdCount
    count = nx.get_edge_attributes(Gcc, 'sumWtdCount').values()
    print(count)
    count = [c/200 + 0.01 for c in count]


    # Add labels only for important users (nodes with out_degree > 20)

    labels = {i: name for i, name in list(nx.get_node_attributes(Gcc, 'name').items()) if degs[i] >= 1}

    # Add nodes with out_degree = 0 colored in white
    sizes2 = [0 if (Gcc.out_degree(node)) > 0 else np.log10(net_abs[node])*20 for node in nod]
    nx.draw_networkx_nodes(Gcc, ax = ax0, pos=pos,node_color='white',node_size=sizes2, zorder=40, alpha=0.6)

    # Draw network
    nx.draw_networkx(Gcc, ax = ax0, pos=pos, edge_color='black', alpha=0.9, arrows=True,
                     with_labels=True, node_color = color, cmap=plt.cm.plasma, vmin=1, vmax=2000,
                     node_size=sizes, labels=labels, width = count, font_size=14, font_weight='bold', zorder=50)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=1, vmax=2000))
    sm._A = []
    cb = plt.colorbar(sm, ax=ax0, orientation='horizontal')
    cb.set_label(label='Out Degree', size=16)


    plt.tight_layout(pad=5)
    plt.savefig( 'by_seniority/' + year  + '.png', dpi=300)



    return

###################################################################################################################

users = pd.read_csv('../data/CDSS_WaterRights.csv')
print(users.columns)

N = 200

# select top 200 users by decree (net absolute)
users_decree = users.sort_values('Net Absolute')
users_decree = users_decree.head(n=N)['WDID'].tolist()
print(users_decree[:10])

# select top 200 users by seniority
users_seniority = users.sort_values('Priority Admin No')
users_seniority = users_seniority.head(n=N)['WDID'].tolist()
print(users_seniority[:10])


years = [str(yr) for yr in range(2000,2019)]
print(years)

for year in years:
    print(year)
    G = make_year_network(year)
    Gcc = G.subgraph(users_seniority)
    plot_network_graph(Gcc, year)
    print(Gcc.number_of_nodes())
