import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from eularian import *

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
    if snow_depth <= 2.5:
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

    #G = add_snow_depth(G)

    #G = ox.convert.to_undirected(G)
    #G = to_eularian(G)

    #eularian_cycle = list(nx.eulerian_circuit(G))
    #eularian_edges = [(u,v) for u,v in eularian_cycle]

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)

    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        snow_depth = G[u][v][0]['snow_depth']
        edge_color = get_edge_color(snow_depth)
        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=2)
    
    plt.show()

def Show_Deneig_Circuit(G):
    # Remove streets with to much snow
    to_suppr = []
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['snow_depth'] >= 15 :
            to_suppr.append((u,v))
    for u,v in to_suppr:
        G.remove_edge(u,v)
    #Calculate The eularian graph
    
    """G = to_eularian(G)
    eularian_cycle = list(nx.eulerian_circuit(G))
    eularian_edges = [(u,v) for u,v in eularian_cycle]

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)
    node_passage = {node: 0 for node in G.nodes()}

    # Draw the Eulerian cycle edges with colors based on snow depth

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

    plt.show()"""


G = (ox.load_graphml(filepath="./data/Outremont.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
Show_Deneig_Circuit(G)
Show_Snow(G)


"""G = (ox.load_graphml(filepath="./data/Verdun.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Deneig_Circuit(G)

G = (ox.load_graphml(filepath="./data/Anjou.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Deneig_Circuit(G)

G = (ox.load_graphml(filepath="./data/Riviere.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Deneig_Circuit(G)

G = (ox.load_graphml(filepath="./data/Plateau.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Deneig_Circuit(G)"""
