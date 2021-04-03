import pandas as pd
import os
import networkx as nx


'''Filter out empty rows and only keep rows where a user was put out of priority for a non-zero % of day'''
# years_list = os.listdir('yearly_data/')
# years_list = years_list[1:]
# # years_list = ['2018.csv']
# print(years_list)
#
# for year in years_list:
#     print(year)
#     df = pd.read_csv('yearly_data/' + year)
#     filtered_df = df.loc[df['analysisOutOfPriorityPercentOfDay'] > 0]
#     print(filtered_df)
#     filtered_df.to_csv('yearly_data/' + year)
#
######################################################################################################

'''Remove unnecessary columns'''
#
# years_list = os.listdir('yearly_data/')
# years_list = years_list[1:]
# # years_list = years_list[2:]
# # years_list = ['2002.csv']
# print(years_list)
#
# for year in years_list:
#     print(year)
#     df = pd.read_csv('yearly_data/' + year, dtype = object)
#     new_df = df.filter(['analysisDate', 'analysisWdid', 'analysisStructureName', 'analysisOutOfPriorityPercentOfDay',
#     'locationWdid', 'locationStructure', 'priorityWdid', 'priorityStructure', ], axis=1)
#     new_df.to_csv('yearly_data_lite/' + year, index = False)

######################################################################################################

'''Create .csv files with network edges and edge attributes'''

path = 'yearly_data_lite/'
years_list = os.listdir(path)
# years_list.remove('.DS_Store')
# years_list = ['2008.csv']
print(years_list)
# years_list = years_list[1:2]

for year in years_list:
    print(year)
    df = pd.read_csv(path + year)
    df = df.drop(['analysisDate', 'analysisStructureName', 'locationStructure',
                   'priorityStructure'], 1)
    # print(df.columns)
    new_df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0: 'count'})
    wtd_count = new_df['analysisOutOfPriorityPercentOfDay'] * new_df['count'] / 100
    new_df['wtd_count'] = list(wtd_count)
    # print(new_df)
    new_df['sum_wtd_count'] = new_df.groupby(['analysisWdid', 'locationWdid'])['wtd_count'].transform('sum')
    new_df['priority_sum_wtd_count'] = new_df.groupby(['analysisWdid', 'priorityWdid'])['wtd_count'].transform('sum')
    new_df = new_df.drop(['analysisOutOfPriorityPercentOfDay', 'count', 'wtd_count'], 1)
    new_df = new_df.drop_duplicates()
    # new_df = new_df.groupby(new_df.columns.tolist()).sum().reset_index().rename(columns={0: 'sum_wtd_count'})
    print(new_df)
    new_df.to_csv('yearly_networks_v2/network_' + year, index = False)

######################################################################################################################

'''Create .csv file with network node attributes'''
#
# df = pd.read_csv('../data/DWR_REST_WaterRights.csv')
# print(df.head())
#
# new_df = df.groupby('wdid').netAbsolute.sum().reset_index().rename(columns={'netAbsolute': 'sum_netAbs'})
# merged = pd.merge(left=df, right=new_df, left_on='wdid', right_on='wdid')
# print(merged.head())
# merged = merged.drop(['netAbsolute', 'adminNumber'], 1)
# merged = merged.drop_duplicates()
#
# print(merged.columns)
#
# merged.to_csv('../data/Attributes.csv', index = False)

###################################################################################################################

'''Add node attributes to network files'''

#
# def make_year_network(year):
#     # enter year in YYYY string format
#
#     node_attr = pd.read_csv('../data/Attributes.csv')
#     # print(water_rights.WDID.to_list())
#     path = 'yearly_networks/network_'
#     data = pd.read_csv(path + year + '.csv')
#
#     G = nx.from_pandas_edgelist(df=data, source='locationWdid', target='analysisWdid', edge_attr = 'sum_wtd_count',
#                                 create_using=nx.DiGraph())
#     # add latitude for each node
#     lat_dict = node_attr[['wdid', 'latitude']].set_index('wdid')['latitude'].to_dict()
#     nx.set_node_attributes(G, name = 'latitude', values = lat_dict)
#
#     # # add longitude for each node
#     long_dict = node_attr[['wdid', 'longitude']].set_index('wdid')['longitude'].to_dict()
#     nx.set_node_attributes(G, name = 'longitude', values = long_dict)
#
#     # # add net absolute for each node
#     vol_dict = node_attr[['wdid', 'sum_netAbs']].set_index('wdid')['sum_netAbs'].to_dict()
#     nx.set_node_attributes(G, name='netAbs', values=vol_dict)
#
#     return G
#
# year = '2000'
# G = make_year_network(year)
# # print(G.nodes())
# print(G.node[5103660]['latitude'], G.node[5103660]['longitude'], G.node[5103660]['netAbs'])

###################################################################################################################


