import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import matching
import itertools
from datetime import datetime

start=datetime.now()

def calculate_graph(Ville):
    G = ox.graph_from_place(Ville + ', Canada', "drive")
    G = ox.distance.add_edge_lengths(G)
    ox.io.save_graph_geopackage(G, filepath="./data/" + Ville + ".gpkg") #save geopackages
    ox.io.save_graphml(G, filepath="./data/" + Ville + ".graphml") # read graph

calculate_graph('Montreal')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Outremont')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Verdun')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Anjou')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Rivière-des-prairies-pointe-aux-trembles')
### ---------------------------------------------------------------------------------------------------------------------- ###
calculate_graph('Le Plateau-Mont-Royal')

# Message Box
print("Done in ", datetime.now()-start)