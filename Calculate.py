import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import matching
import itertools
from datetime import datetime

start=datetime.now()

def show(G):
    # Get the geographical positions of the nodes
    node_positions = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    # Plot the MultiDiGraph with geographical positions
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos=node_positions, with_labels=True, node_size=10)
    plt.title("MultiDiGraph of the City with Geographical Positions")
    plt.show()

def to_eularian(G):

    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]

    for i in range(0,len(odd_nodes) - 1,2):
        path = nx.dijkstra_path(G, odd_nodes[i], odd_nodes[i+1])

        for j in range(len(path) - 1):
            G.add_edge(path[j], path[j + 1], length=nx.shortest_path_length(G, source=path[j], target=path[j + 1], weight='length'))
    
    return G

G = ox.graph_from_place('Outremont, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Outremont.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Outremont.graphml") # read graph

G = ox.convert.to_undirected(G)
legranH = to_eularian(ox.convert.to_undirected(G))
print(nx.is_eulerian(legranH))

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Verdun, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Verdun.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Verdun.graphml") # read graph

G = ox.convert.to_undirected(G)
legranH = to_eularian(ox.convert.to_undirected(G))
print(nx.is_eulerian(legranH))

### ---------------------------------------------------------------------------------------------------------------------- ###

G= ox.graph_from_place('Anjou, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Anjou.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Anjou.graphml") # read graph

G = ox.convert.to_undirected(G)
legranH = to_eularian(ox.convert.to_undirected(G))
print(nx.is_eulerian(legranH))

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Rivière-des-prairies-pointe-aux-trembles, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Riviere.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Riviere.graphml") # read graph

G = ox.convert.to_undirected(G)
legranH = to_eularian(ox.convert.to_undirected(G))
print(nx.is_eulerian(legranH))

### ---------------------------------------------------------------------------------------------------------------------- ###

G = ox.graph_from_place('Le Plateau-Mont-Royal, Canada', "drive")
G = ox.distance.add_edge_lengths(G)
ox.io.save_graph_geopackage(G, filepath="./data/Plateau.gpkg") #save geopackages
ox.io.save_graphml(G, filepath="./data/Plateau.graphml") # read graph

G = ox.convert.to_undirected(G)
legranH = to_eularian(ox.convert.to_undirected(G))
print(nx.is_eulerian(legranH))

# Message Box
print("Done in ", datetime.now()-start)