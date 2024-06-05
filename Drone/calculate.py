import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import matching
import itertools
from datetime import datetime

start=datetime.now()

def calculate_graph(Ville):
    G = ox.graph_from_place(Ville, "drive")
    G = ox.distance.add_edge_lengths(G)
    ox.io.save_graph_geopackage(G, filepath="./data/" + Ville + ".gpkg") #save geopackages
    ox.io.save_graphml(G, filepath="./data/" + Ville + ".graphml") # read graph

calculate_graph('Montreal, Canada')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Outremont, Canada')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Verdun, Canada')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Anjou, Canada')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Rivière-des-prairies-pointe-aux-trembles, Canada')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Le Plateau-Mont-Royal, Canada')

# Message Box
print("Done in ", datetime.now()-start)