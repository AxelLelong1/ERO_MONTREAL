#!/usr/bin/python
# -*- coding: UTF8 -*-
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import matching
import itertools
from datetime import datetime

start=datetime.now()

G = ox.graph_from_place('Outremont, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Outremont.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Outremont.graphml") # read graph

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Verdun, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Verdun.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Verdun.graphml") # read graph

### ---------------------------------------------------------------------------------------------------------------------- ###

G= ox.graph_from_place('Anjou, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Anjou.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Anjou.graphml") # read graph

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Rivière-des-prairies-pointe-aux-trembles, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Riviere.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Riviere.graphml") # read graph

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Le Plateau-Mont-Royal, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Plateau.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Plateau.graphml") # read graph

# Message Box
print("Done in ", datetime.now()-start)