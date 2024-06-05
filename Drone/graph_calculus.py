import osmnx as ox
import networkx as nx
import numpy as np

def Calculate_Lenght(G):
    cycle_length = 0

    eularian_cycle = list(nx.eulerian_circuit(G))
    eularian_edges = [(u,v) for u,v in eularian_cycle]

    for u, v in eularian_edges:
        snow_depth = None
        # Access all keys and find snow_depth
        for key, data in G.get_edge_data(u, v).items():
            if 'length' in data:
                cycle_length += data['length']
    
    return cycle_length

def Calculate_Snow(G, OrSnowGraph):

    eularian_cycle = list(nx.eulerian_circuit(G))
    eularian_edges = [(u,v) for u,v in eularian_cycle]

    # Draw the Eulerian cycle edges with colors based on snow depth
    for u, v in eularian_edges:
        snow_depth = None
        # Access all keys and find snow_depth
        for key, data in G.get_edge_data(u, v).items():
            if 'snow_depth' in data:
                snow_depth = data['snow_depth']
                break

        # Copy Snow factor to the other part
        if (snow_depth != None):
            for i, j, k, d in OrSnowGraph.edges(keys=True, data=True):
                if ((i,j) == (u,v)):
                    d['snow_depth'] = snow_depth
                elif ((i,j) == (v,u)):
                    d['snow_depth'] = snow_depth
    
    return G, OrSnowGraph