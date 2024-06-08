import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from utils import *

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
        if 'snow_depth' not in data:
            data['snow_depth'] = np.random.uniform(0, 15)
            if G.has_edge(v,u):
                data1 = G.get_edge_data(v, u)[0]
                data1['snow_depth'] = data['snow_depth']
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


def Show_Snow(G, path = None):

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)

    for u, v, key, data in G.edges(keys=True, data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        snow_depth = G[u][v][0]['snow_depth']
        edge_color = get_edge_color(snow_depth)
        #if ('demi-tour' in data):
        #    edge_color = 'red'
        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=2)
    
    plt.show()

def deneiger(H, G, depart):
    to_suppr = []
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['snow_depth'] >= 15 :
            to_suppr.append((u,v))
    for u,v in to_suppr:
        G.remove_edge(u,v)
    G = handle_one_way_streets(G)
    G = find_largest_scc(G)
    total_snow = sum(data['snow_depth'] for u, v, data in G.edges(data=True) if data['snow_depth'] >= 2.5)

    current = list(G.nodes)[0]  # Commencer à un nœud arbitraire
    total_path = nx.shortest_path(H, source=depart, target=current, weight='length')
    total_path.pop()
    distance = nx.shortest_path_length(H, source=depart, target=current, weight='length')

    while total_snow > 0:
        total_path.append(current)
        find_an_edge = False

        for suc in G.successors(current):
            data = G.get_edge_data(current, suc)[0]
            if data['snow_depth'] >= 2.5:
                total_snow -= data['snow_depth']
                data['snow_depth'] = 0
                if G.has_edge(suc, current):
                    data2 = G.get_edge_data(suc, current)[0]
                    total_snow -= data2['snow_depth']
                    data2['snow_depth'] = 0
                distance += data['length']
                current = suc
                find_an_edge = True
                break
        
        if not find_an_edge:
            # Si aucune arête à déneiger n'a été trouvée, trouver le prochain nœud avec de la neige à déneiger
            target = None
            for node in G.nodes:
                if node != current:
                    for suc in G.successors(node):
                        data = G.get_edge_data(node, suc)[0]
                        if data['snow_depth'] >= 2.5:
                            target = node
                            break
                if target is not None:
                    break
            
            if target is None:
                break
            
            path = nx.shortest_path(G, source=current, target=target, weight='length')
            dist = nx.shortest_path_length(G, source=current, target=target, weight='length')
            distance += dist
            path.pop(0)  # Enlever le nœud courant du début du chemin
            total_path.extend(path)
            current = target
    path = nx.shortest_path(H, source=current, target=depart, weight='length')
    dist = nx.shortest_path_length(H, source=current, target=depart, weight='length')
    distance += dist
    path.pop(0)  # Enlever le nœud courant du début du chemin
    total_path.extend(path)
    return distance, total_path, G
            

def Show_Vehicule_Circuit(G, path):

    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(100,100))

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)
    node_passage = {node: 0 for node in G.nodes()}

    for idx, node in enumerate(path):
        
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
        
        x,y = pos[node]
        offset = node_passage[node] * 10
        ax.annotate(str(idx), xy=(x,y), textcoords='offset points', xytext=(offset,offset + 10), ha='center', fontsize=8, color=textcolor)
        node_passage[node] += 1

    plt.show()

colors = [
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Orange",
    "Purple",
    "Pink",
    "Brown",
    "Black",
    "Gray",
    "Cyan",
    "Magenta",
    "Maroon",
    "Navy",
    "Teal",
    "Olive",
    "Lime",
    "Indigo",
    "Violet",
    "Gold"
]

def Show_clusters(clusters, G):

    fig, ax = plt.subplots(figsize=(100,100))
    pos = {node: (data['x'], data['y']) for node, data in G.nodes(data=True)}    

    nx.draw(G, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)

    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        edge_color = 'black'
        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=2)

    i = 0 
    for graph, gros in clusters:
        pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}    

        nx.draw(graph, pos, ax=ax, node_size=8, node_color='gray', edge_color='lightgray', with_labels=False)

        for u, v in graph.edges():
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            edge_color = colors[i % len(colors)]
            ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=2)
        
        i+=1
        
    plt.show()

def calculs(clusters, G):
    distance = 0
    cout = 0
    temps = 0
    graphs = []
    depart = list(G.nodes)[0]
    for graph, gros in clusters:
        dist, total_path, H = deneiger(G, graph, depart)
        graphs.append(H)
        if (gros):
            tmp = (dist / 5.56) / 3600
            cout = cout + dist * 0.0013 + 800 + tmp * 1.3
        else:
            tmp = (dist / 2.78) / 3600
            cout = cout + dist * 0.0011 + 500 + tmp * 1.1
        if tmp > temps:
            temps = tmp
        distance += dist
    global_graph = nx.compose_all(graphs)
    for u, v, key, data1 in global_graph.edges(keys=True, data=True):
        if (G.has_edge(u,v)):
            data = G.get_edge_data(u, v)[0]
            data['snow_depth'] = data1['snow_depth']
    return distance, temps, cout, G


"""
G = (ox.load_graphml(filepath="./data/Outremont.graphml"))
G = add_snow_depth(G)
G = handle_one_way_streets(G)
G = find_largest_scc(G)
clusters = partitioning(G, 2, 1, 1)

distance, temps, cout, G = calculs(clusters, G)
#Show_Snow(G)

print("Coût Déneigeuses total = ", cout)
print("Temps Déneigeuse total en heure = ", temps)
print("distance totale = ", distance)



G = (ox.load_graphml(filepath="./data/Verdun.graphml"))
G = add_snow_depth(G)
G = handle_one_way_streets(G)
G = find_largest_scc(G)
clusters = partitioning(G, 3, 1, 2)

distance, temps, cout, G = calculs(clusters, G)
#Show_Snow(G)

print("Coût Déneigeuses total = ", cout)
print("Temps Déneigeuse total en heure = ", temps)
print("distance totale = ", distance)


G = (ox.load_graphml(filepath="./data/Anjou.graphml"))
G = add_snow_depth(G)
G = handle_one_way_streets(G)
G = find_largest_scc(G)
clusters = partitioning(G, 8, 0, 8)


distance, temps, cout, G = calculs(clusters, G)
Show_Snow(G)

print("Coût Déneigeuses total = ", cout)
print("Temps Déneigeuse total en heure = ", temps)
print("distance totale = ", distance)



G = (ox.load_graphml(filepath="./data/Riviere.graphml"))
G = add_snow_depth(G)
G = handle_one_way_streets(G)
G = find_largest_scc(G)
clusters = partitioning(G, 3, 1, 2)

distance, temps, cout, G = calculs(clusters, G)
Show_Snow(G)

print("Coût Déneigeuses total = ", cout)
print("Temps Déneigeuse total en heure = ", temps)
print("distance totale = ", distance)

"""
G = (ox.load_graphml(filepath="./data/Plateau.graphml"))
G = add_snow_depth(G)
G = handle_one_way_streets(G)
G = find_largest_scc(G)
clusters = partitioning(G, 11, 7, 4)

distance, temps, cout, G = calculs(clusters, G)
Show_Snow(G)

print("Coût Déneigeuses total = ", cout)
print("Temps Déneigeuse total en heure = ", temps)
print("distance totale = ", distance)