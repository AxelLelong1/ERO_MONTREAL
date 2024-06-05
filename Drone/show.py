import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from graph_utils import *

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