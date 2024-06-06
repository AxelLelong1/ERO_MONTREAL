import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from eularian import *
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

def handle_one_way_streets(G):
    # Identifier les nœuds avec un degré sortant de 0
    impasses = [node for node in G.nodes() if G.out_degree(node) == 0]

    for node in impasses:
        current_node = node
        while True:
            # Trouver le prédécesseur
            predecessors = list(G.predecessors(current_node))
            # Maybe prendre le predec. le moins couteux
            if not predecessors:
                break  # Si pas de prédécesseur, arrêter
            predecessor = predecessors[0]
            
            # Copier les attributs de l'arête existante
            edge_data = G.get_edge_data(predecessor, current_node)
            if edge_data:
                data = edge_data[0]  # Prendre les attributs de la première arête trouvée

                # Ajouter l'arête inverse si nécessaire
                if G.out_degree(predecessor) > 1:
                    data['demi-tour'] = 1
                    G.add_edge(current_node, predecessor, **data)
                    break
                else:
                    data['demi-tour'] = 1
                    G.add_edge(current_node, predecessor, **data)
                    current_node = predecessor
    
    return G


def Show_Deneig_Circuit(G):
    # Remove streets with to much snow
    to_suppr = []
    total_snow = 0
    distance = 0
    total_path = []
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['snow_depth'] >= 15 :
            to_suppr.append((u,v))
    for u,v in to_suppr:
        G.remove_edge(u,v)
    G = handle_one_way_streets(G)
    G = find_largest_scc(G)
    Show_Snow(G)

    for u, v, key, data in G.edges(keys=True, data=True):
        if data['snow_depth'] >= 2.5 :
            total_snow += data['snow_depth']

    current = list(G.nodes)[0]
    while total_snow != 0:
        total_path.append(current)
        find_an_edge = False
        sucs = list(G.successors(current))
        for suc in sucs:
            data1 = G.get_edge_data(current, suc)[0]
            if data1['snow_depth'] >= 2.5:
                total_snow -= data1['snow_depth']
                data1['snow_depth'] = 0
                if G.has_edge(suc, current):
                    data2 = G.get_edge_data(suc, current)[0]
                    total_snow -= data2['snow_depth']
                    data2['snow_depth'] = 0
                distance += data1['length']
                current = suc
                find_an_edge = True
                break
        if not find_an_edge:
            target = find_next_snow(G, current)
            if target is None:
                return distance, total_path, G
            path = nx.shortest_path(G, source=current, target=target, weight='length')
            path.pop(0)
            for j in range(len(path)):
                data = G.get_edge_data(current, path[j])
                sudatat = data[0]
                distance += sudatat['length']
                current = path[j]
                total_path.append(path[j])
            total_path.pop()

    return distance, total_path, G

def deneiger(G):
    to_suppr = []
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['snow_depth'] >= 15 :
            to_suppr.append((u,v))
    for u,v in to_suppr:
        G.remove_edge(u,v)
    G = handle_one_way_streets(G)
    G = find_largest_scc(G)
    #G = handle_one_way_streets(G)
    Show_Snow(G)
    total_snow = sum(data['snow_depth'] for u, v, data in G.edges(data=True) if data['snow_depth'] >= 2.5)
    print(f"Total initial de neige à déneiger: {total_snow:.2f}")

    current = list(G.nodes)[0]  # Commencer à un nœud arbitraire
    total_path = []
    distance = 0

    while total_snow > 0:
        total_path.append(current)
        find_an_edge = False

        for suc in G.successors(current):
            data = G.get_edge_data(current, suc)[0]
            if data['snow_depth'] >= 2.5:
                total_snow -= data['snow_depth']
                print()
                print(data['snow_depth'])
                data['snow_depth'] = 0
                if G.has_edge(suc, current):
                    data2 = G.get_edge_data(suc, current)[0]
                    print(data2['snow_depth'])
                    total_snow -= data2['snow_depth']
                    data2['snow_depth'] = 0
                distance += data['length']
                print()
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
                print("Aucune arête restante à déneiger.")
                break
            
            path = nx.shortest_path(G, source=current, target=target, weight='length')
            path.pop(0)  # Enlever le nœud courant du début du chemin
            total_path.extend(path)
            current = target
        print(f"Total final de neige à déneiger: {total_snow:.2f}")
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


"""
G = (ox.load_graphml(filepath="./data/Outremont.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
distance, total_path, G = deneiger(G)
print("distance total = ", distance)
Show_Vehicule_Circuit(G, total_path)
Show_Snow(G)


G = (ox.load_graphml(filepath="./data/Verdun.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
distance, total_path, G = deneiger(G)
print("distance total = ", distance)
Show_Vehicule_Circuit(G, total_path)
Show_Snow(G)
"""
G = (ox.load_graphml(filepath="./data/Anjou.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
distance, total_path, G = deneiger(G)
print("distance total = ", distance)
Show_Vehicule_Circuit(G, total_path)
Show_Snow(G)
"""
G = (ox.load_graphml(filepath="./data/Riviere.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
Show_Deneig_Circuit(G)
Show_Snow(G)
handle_one_way_streets(G)
Show_Snow(G)

G = (ox.load_graphml(filepath="./data/Plateau.graphml"))
#ShowGraph(G)
G = add_snow_depth(G)
Show_Snow(G)
Show_Deneig_Circuit(G)
Show_Snow(G)
handle_one_way_streets(G)
Show_Snow(G)
"""