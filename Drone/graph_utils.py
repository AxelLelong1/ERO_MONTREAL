import osmnx as ox
import numpy as np
from Drone.eularian import *

def convert(G):
    G = ox.convert.to_undirected(G)
    return to_eulerian(G)

def add_snow_depth(G):
    np.random.seed(42)  # for reproducibility
    for u, v, key, data in G.edges(keys=True, data=True):
        data['snow_depth'] = np.random.uniform(0, 15)
    return G

def get_edge_color(snow_depth):
    if snow_depth == None:
        return 'green'
    elif snow_depth <= 2.5:
        return 'lightgray'
    elif snow_depth <= 5:
        return 'lightblue'
    elif snow_depth <= 10:
        return 'blue'
    elif snow_depth <= 15:
        return 'darkblue'
    else:
        return 'red'
