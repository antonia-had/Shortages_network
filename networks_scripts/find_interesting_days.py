# finds daily user networks with interesting properties in a given year

import networkx as nx
import os
import pandas as pd
import csv

def measure_network_props(G):
    # returns a dictionary of centrality measure values for a given undirected networkx graph
    props = {} # dictionary where each centrality measure is a key

    # 1. degree_centrality(G)
    try:
        props['degree_centrality'] = nx.degree_centrality(G)
    except:
        print("Something went wrong with degree_centrality")

    # 2. eigenvector_centrality(G, max_iter=100, tol=1e-06, nstart=None, weight=None)
    try:
        props['eigenvector_centrality'] = nx.degree_centrality(G)
    except:
        print("Something went wrong with eigenvector_centrality")

    # 3. closeness_centrality(G, u=None, distance=None, wf_improved=True)
    try:
        props['closeness_centrality'] = nx.closeness_centrality(G)
    except:
        print("Something went wrong with closeness_centrality")

    # 4. betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
    try:
        props['betweenness_centrality'] = nx.betweenness_centrality(G)
    except:
        print("Something went wrong with betweenness_centrality")

    # 5. communicability_betweenness_centrality(G, normalized=True)
    try:
        props['communicability_betweenness_centrality'] = nx.communicability_betweenness_centrality(G)
    except:
        print("Something went wrong with communicability_betweenness_centrality")

    # 6. load_centrality(G, v=None, cutoff=None, normalized=True, weight=None)
    try:
        props['load_centrality'] = nx.load_centrality(G)
    except:
        print("Something went wrong with load_centrality")

    # 7. second_order_centrality(G)
    try:
        props['second_order_centrality'] = nx.second_order_centrality(G)
    except:
        print("Something went wrong with second_order_centrality")

    return props

################################################################################################################
def make_day_network(date):
    # create network for a given day
    # format date as YYYY-MM-DD string

    data = pd.read_csv('daily_data/' + date + '.csv')

    # filter to select only users that were put out of priority that day
    data = data.loc[(data.analysisOutOfPriorityPercentOfDay > 0)]
    G = nx.from_pandas_edgelist(df=data, source='locationWdid', target='analysisWdid',  create_using=nx.DiGraph())

    return G

#################################################################################################################

