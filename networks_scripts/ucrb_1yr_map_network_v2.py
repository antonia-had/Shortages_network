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
import cartopy.feature as cfeature
import seaborn as sns
from matplotlib.colors import ListedColormap

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

    # ax0.set_title("Full network of user interactions", fontsize=16)

    # Select only top 100% of nodes based on degree
    degree = G.degree()
    N = int(math.ceil(1.00 * len(degree)))
    top_nodes = sorted(degree, key = lambda x: x[1], reverse = True)[:N]
    top_nodes_list = [n for n,d in top_nodes]
    Gcc = G.subgraph(top_nodes_list)


    # Color nodes by out degree
    degs = Gcc.out_degree() # Dict with Node ID, Degree
    nod = Gcc.nodes()
    color = np.asarray([degs[n] for n in nod])
    # print(sorted(color, reverse=True))

    # Size nodes by net absolute volume log-scaled and set size of nodes with out_degree = 0 to 0
    net_abs = nx.get_node_attributes(Gcc, 'netAbs')
    sizes = [np.log10(net_abs[i])*40 if net_abs[i] > 0 and Gcc.out_degree(i) > 0 else 0 for i in Gcc.nodes]


    # Add labels only for important users (nodes with out_degree > 20)

    labels = {i: name for i, name in list(nx.get_node_attributes(Gcc, 'name').items()) if degs[i] >= 20}

    # Add nodes with out_degree = 0 colored in white
    sizes2 = [0 if (Gcc.out_degree(node)) > 0 else np.log10(net_abs[node])*20 for node in nod]
    nx.draw_networkx_nodes(Gcc, ax = ax0, pos=pos,node_color='white',node_size=sizes2, zorder=40, alpha=0.6)

    # Draw network
    nx.draw_networkx(Gcc, ax = ax0, pos=pos, edge_color='black', alpha=0.9, arrows=False,
                     with_labels=True, node_color = color, cmap=plt.cm.plasma, vmin=1, vmax=2000,
                     node_size=sizes, labels=labels, width = 0.1, font_size=14, font_weight='bold', zorder=50)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=1, vmax=2000))
    sm._A = []
    cb = plt.colorbar(sm, ax=ax0, orientation='horizontal')
    cb.set_label(label='Out Degree', size=16)




    # # 2. SUBPLOT OF MEAN ANNUAL FLOWS
    # # the second subplot will span 2 rows and 4 columns, bottom left
    # ax1 = fig.add_subplot(gspec[4:, :6])
    # flows = pd.read_csv('../data/UCRB_mean_annual_flows.csv')
    # ax1.plot(flows['year_nu'], flows['mean_va'], 'bo-')
    # ax1.set_xlabel('Year')
    # ax1.set_ylabel('Mean stream flow (cfs)')
    # ax1.set_title("Mean annual flows for river basin")
    # ax1.set_xticks(flows['year_nu'])
    # ax1.axvline(x=int(year), color = 'red')


    plt.tight_layout(pad=5)
    plt.savefig( 'yearly_networks_plots_v2/cleaned_up_figs/' + year + '_100percent' + '.png', dpi=300)



    return

###################################################################################################################

'''Create network'''
# year = '2000'
# G = make_year_network(year)
# print(G.nodes())
# print(G.node[5103660]['latitude'], G.node[5103660]['longitude'], G.node[5103660]['netAbs'])


# plot_network_graph(G, year)

years = [str(yr) for yr in range(2000, 2020)]
print(years)

for year in years:
    print(year)
    G = make_year_network(year)
    plot_network_graph(G, year)
