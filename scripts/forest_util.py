'''
Utility functions for Forest and network analysis
'''
import networkx as nx
import os, glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os.path

def loadGraph(sifFile):
    '''Parses a .sif file from Forest.
    
    pp is undirected, pd directed.
    networkx currently does not support mixed graphs, so for all pp edges,
    a directed edge both to and from each node in the entry is created.
    
    INPUT: sifFile - the filename of the Forest output .sif file
    
    OUTPUT: a networkx DiGraph representing the network from Forest
    '''
    with open(sifFile, 'r') as sf:
        G = nx.DiGraph()
        for line in sf:
            edge = line.split()
            assert len(edge) == 3, '.sif file must contain two nodes and ' \
                'edge type on each line'
            assert edge[1] == 'pp' or edge[1] == 'pd', 'Edge type must be pp or pd'
            
            # Undirected edge is pair of directed edges
            if edge[1] == "pp":
                G.add_edge(edge[0], edge[2])
                G.add_edge(edge[2], edge[0])
            # Must be a directed edge if not undirected
            else:
                G.add_edge(edge[0], edge[2])
    return G

def summaryGraphs(folder):
    GraphList = []
    FilenameList = []
    nodeslist = []
    edgeslist = []
    diameterlist = []
    connectedc= []
    maxd = []

    path = os.path.realpath(folder)

    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith("result_optimalForest.sif")]:
            filepath = os.path.join(dirpath, filename)
            graph = loadGraph(filepath)
            GraphList.append(graph)
            FilenameList.append(filepath)
            nodeslist.append(graph.number_of_nodes())
            edgeslist.append(graph.number_of_edges())
            diameterlist.append(nx.diameter(graph))
            isDirected = nx.is_directed(graph)
            if (isDirected):
                connectedc.append(np.nan)
            else:
                connectedc.append(nx.number_connected_components(graph))
            degree = graph.degree()
            maximum = max(degree, key=degree.get)
            maxd.append(degree[maximum])
    
    
    s = pd.DataFrame(data = FilenameList, columns=['Filenames'])
    s['Graph'] = GraphList
    s['Number of nodes'] = nodeslist
    s['Number of edges'] = edgeslist
    s['Diameter'] = diameterlist
    s['Number of connected components'] = connectedc
    s['Maximum degree (max over all node degrees)'] = maxd
    s.to_csv('info.txt', path = os.path.realpath(folder), sep='\t', index=False)
    return s