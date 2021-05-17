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
import os




path = '../R_networks_scripts/network_csv_files/priorityWdid/monthly/'
m_list = os.listdir(path)
#m_list.remove('.DS_Store')
m_list = ['2003-09.csv']

print(m_list)

attr = pd.read_csv('../R_networks_scripts/network_csv_files/priorityWdid/Attributes.csv', index_col=[0])
new_df = pd.DataFrame()

for m in m_list:
    print(m)
    df = pd.read_csv(path + m)
    #df = df.sort_values('analysisStreamMile')
    new_df = pd.merge(df, attr, how="left", left_on=["analysisWdid"], right_on=["wdid"])
    new_df = new_df.rename(columns={"streamMile": "analysisStreamMile", "sum_netAbs": "analysisNetAbs",
                           "waterDistrict": "analysisWaterDistrict", "sum_wtd_count": "sumWtdCount"})
    #print(new_df.columns)
    new_df = pd.merge(new_df, attr, how="left", left_on=["priorityWdid"], right_on=["wdid"])
    new_df = new_df.rename(columns={"streamMile": "priorityStreamMile", "sum_netAbs": "priorityNetAbs",
                           "waterDistrict": "priorityWaterDistrict"})
    #df['edgeWt'] = df['analysisNetAbs'] * df['sumWtdCount']
    df = new_df
    print(df.columns)

    df.to_csv(path + m, index = False)
