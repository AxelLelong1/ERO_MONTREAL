import osmnx as ox
import numpy as np

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
 
        for succ in G.successors(node):
            if succ['marque'] is None:
                succ['marque'] = 1
                pile.append(succ)

    return null