import osmnx as ox
import numpy as np
import networkx as nx
import heapq

def find_next_snow(G, current):
    pile = []
    pile.append(current)    

    G.nodes[current]['marque'] = 1

    while pile:
        node = pile.pop(0)

        edges = G.out_edges(node, data=True)
        for u, v, data in edges:
            if data['snow_depth'] >= 2.5: #seuil de déneigement
                return u
 
        for u, v, data in edges:#G.successors(node):
            if G.nodes[v].get('marque', None) is None:
                G.nodes[v]['marque'] = 1
                pile.append(v)
    return None

def find_largest_scc(G):
    # Compute the strongly connected components
    sccs = list(nx.strongly_connected_components(G))
    
    # Find the largest strongly connected component
    largest_scc = max(sccs, key=len)
    
    # Create a subgraph of the largest strongly connected component
    largest_scc_subgraph = G.subgraph(largest_scc).copy()
    
    return largest_scc_subgraph
