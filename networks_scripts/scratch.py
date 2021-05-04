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




path = '../R_networks_scripts/network_csv_files/priorityWdid/'
years_list = os.listdir(path)
years_list.remove('.DS_Store')
# years_list = [years_list[0]]

print(years_list)


for year in years_list:
    print(year)
    df = pd.read_csv(path + year)
    df = df.sort_values('analysisStreamMile')

    df.to_csv(path + year, index = False)
