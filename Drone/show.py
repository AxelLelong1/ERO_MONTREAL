import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from eularian import *

def convert(G):
    G = ox.convert.to_undirected(G)
    return to_eulerian(G)


def ShowGraph(G, show_lenght=True):
    # Définir une figure et un axe pour le graphe
    fig, ax = plt.subplots(figsize=(100, 100))
    ax.set_facecolor((0,0,0))

    # Plot le graphe
    ox.plot_graph(G, ax=ax, show=False, close=False, edge_linewidth=1, node_size=25)

    # Annoter chaque arête avec sa longueur
    for u, v, data in G.edges(data=True):
        if 'length' in data:
            x = (G.nodes[u]['x'] + G.nodes[v]['x']) / 2
            y = (G.nodes[u]['y'] + G.nodes[v]['y']) / 2
            length = data['length']
            if (show_lenght):
                ax.text(x, y, s=f'{length:.1f}', fontsize=8, color='red')

    # Afficher la figure
    plt.show()

def add_snow_depth(G):
    np.random.seed(42)  # for reproducibility
    for u, v, key, data in G.edges(keys=True, data=True):
        data['snow_depth'] = np.random.uniform(0, 20)
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

def Show_Snow(G):

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)

    for u, v in G.edges():
        snow_depth = None
        # Access all keys and find snow_depth
        for key, data in G.get_edge_data(u, v).items():
            if 'snow_depth' in data:
                snow_depth = data['snow_depth']
                break

        # If snow_depth is found, color the edge
        #if snow_depth is not None:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        edge_color = get_edge_color(snow_depth)
        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=2)

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
    """OrSnowGraph = G
    G = add_snow_depth(G)

    G = ox.convert.to_undirected(G)
    G = to_eularian(G)"""

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

def Show_Drone_Circuit(G):

    eularian_cycle = list(nx.eulerian_circuit(G))
    eularian_edges = [(u,v) for u,v in eularian_cycle]

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)
    node_passage = {node: 0 for node in G.nodes()}

    for idx, (u, v) in enumerate(eularian_cycle):
        
        if idx <= 10:
            textcolor = 'red'
        elif idx <= 50:
            textcolor = 'coral'
        elif idx <= 100:
            textcolor = 'chocolate'
        elif idx <= 500:
            textcolor = 'orange'
        elif idx <= 1000:
            textcolor = 'yellow'
        elif idx <= 2000:
            textcolor = 'lawngreen'
        else:
            textcolor = 'darkgreen'
        x,y = pos[u]
        offset = node_passage[u] * 10
        ax.annotate(str(idx), xy=(x,y), textcoords='offset points', xytext=(offset,offset + 10), ha='center', fontsize=8, color=textcolor)
        node_passage[u] += 1

    plt.show()



G = (ox.load_graphml(filepath="./data/Outremont.graphml"))
ox.plot_graph(G)
H = convert(G)
H = add_snow_depth(H)
H, G = Calculate_Snow(H, G)
cycle_length = Calculate_Lenght(H)

print("cycle_length = ", cycle_length)
temps = (cycle_length / 20) / 3600
cout = cycle_length * 0.00001
print("Coût Drone = ", cout)
print("Temps Drone en heure = ", temps)

Show_Snow(G)
ox.plot_graph(G)
#Show_Drone_Circuit(S)

"""
G = (ox.load_graphml(filepath="./data/Verdun.graphml"))
ox.plot_graph(G)
S,OrSnowGraph, cycle_length = Calculate_Snow(G)
print("cycle_length = ", cycle_length)
temps = (cycle_length / 20) / 3600
cout = cycle_length * 0.00001
print("Coût Drone = ", cout)
print("Temps Drone en heure = ", temps)
Show_Snow(OrSnowGraph)
ox.plot_graph(OrSnowGraph)
#Show_Drone_Circuit(S)

G = (ox.load_graphml(filepath="./data/Anjou.graphml"))
ox.plot_graph(G)
S,OrSnowGraph, cycle_length = Calculate_Snow(G)
print("cycle_length = ", cycle_length)
temps = (cycle_length / 20) / 3600
cout = cycle_length * 0.00001
print("Coût Drone = ", cout)
print("Temps Drone en heure = ", temps)
Show_Snow(OrSnowGraph)
ox.plot_graph(OrSnowGraph)
#Show_Drone_Circuit(S)
"""
G = (ox.load_graphml(filepath="./data/Montreal.graphml"))
#ox.plot_graph(G)
#S,OrSnowGraph = Calculate_Snow(G)

H = convert(G)
ox.io.save_graphml(H, filepath="./data/" + "Montreal-E" + ".graphml") # read graph
#H = (ox.load_graphml(filepath="./data/Montreal-E.graphml"))
cycle_length = Calculate_Lenght(H)

print("cycle_length = ", cycle_length)
temps = (cycle_length / 20) / 3600
cout = cycle_length * 0.00001
print("Coût Drone = ", cout)
print("Temps Drone en heure = ", temps)

#Show_Drone_Circuit(S)

"""
G = (ox.load_graphml(filepath="./data/Plateau.graphml"))
ox.plot_graph(G)
S,OrSnowGraph, cycle_length = Calculate_Snow(G)
print("cycle_length = ", cycle_length)
temps = (cycle_length / 20) / 3600
cout = cycle_length * 0.00001
print("Coût Drone = ", cout)
print("Temps Drone en heure = ", temps)
Show_Snow(OrSnowGraph)
ox.plot_graph(OrSnowGraph)
#Show_Drone_Circuit(S)
"""