import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import matching
import itertools
from datetime import datetime
from eularian import *
from graph_utils import *

start=datetime.now()

def calculate_graph(Ville):
    G = ox.graph_from_place(Ville + ', Canada', "drive")
    G = ox.distance.add_edge_lengths(G)
    ox.io.save_graph_geopackage(G, filepath="./data/" + Ville + ".gpkg") #save geopackages
    ox.io.save_graphml(G, filepath="./data/" + Ville + ".graphml") # read graph

def calculate_eulerian(Ville):
    G = ox.load_graphml(filepath="./data/" + Ville + ".graphml")
    
    H = convert(G)
    ox.io.save_graphml(H, filepath="./data/" + Ville +"-E.graphml")


calculate_graph('Montreal')
### ---------------------------------------------------------------------------------------------------------------------- ###
semi=datetime.now()
calculate_graph('Outremont')
print("Done extracting Outremont in ", datetime.now()-semi)

semi=datetime.now()
calculate_eulerian("Outremont")
print("Done calculating Eulerian Outremont in ", datetime.now()-semi)

### ---------------------------------------------------------------------------------------------------------------------- ###
semi=datetime.now()
calculate_graph('Verdun')
print("Done extracting Verdun in ", datetime.now()-semi)

semi=datetime.now()
calculate_eulerian('Verdun')
print("Done calculating Eulerian Verdun in ", datetime.now()-semi)
### ---------------------------------------------------------------------------------------------------------------------- ###
semi=datetime.now()
calculate_graph('Anjou')
print("Done extracting Anjou in ", datetime.now()-semi)

semi=datetime.now()
calculate_eulerian('Anjou')
print("Done calculating Eulerian Anjou in ", datetime.now()-semi)
### ---------------------------------------------------------------------------------------------------------------------- ###
semi=datetime.now()
calculate_graph('Rivière-des-prairies-pointe-aux-trembles')
print("Done extracting Rivière in ", datetime.now()-semi)

semi=datetime.now()
calculate_eulerian('Rivière-des-prairies-pointe-aux-trembles')
print("Done calculating Eulerian Rivière in ", datetime.now()-semi)
### ---------------------------------------------------------------------------------------------------------------------- ###
semi=datetime.now()
calculate_graph('Le Plateau-Mont-Royal')
print("Done extracting Plateau in ", datetime.now()-semi)

semi=datetime.now()
calculate_eulerian('Le Plateau-Mont-Royal')
print("Done calculating Eulerian Plateau in ", datetime.now()-semi)

# Message Box
print("Done all in ", datetime.now()-start)