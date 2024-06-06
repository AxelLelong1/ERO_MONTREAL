import osmnx as ox
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
import numpy as np
from itertools import cycle

def find_next_snow(G, current):
    pile = []
    pile.append(current)    

    G.nodes[current]['marque'] = 1

    while pile:
        node = pile.pop(0)

        edges = G.out_edges(node, data=True)
        for u, v, data in edges:
            if data['snow_depth'] >= 2.5: #seuil de déneigement
                return u
 
        for u, v, data in edges:#G.successors(node):
            if G.nodes[v].get('marque', None) is None:
                G.nodes[v]['marque'] = 1
                pile.append(v)
    return None

def find_largest_scc(G):
    # Compute the strongly connected components
    sccs = list(nx.strongly_connected_components(G))
    
    # Find the largest strongly connected component
    largest_scc = max(sccs, key=len)
    
    # Create a subgraph of the largest strongly connected component
    largest_scc_subgraph = G.subgraph(largest_scc).copy()
    
    return largest_scc_subgraph

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

def partitioning(G, k, i, j):
    # Convertir le graphe en matrice de distance
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    node_indices = {node: i for i, node in enumerate(nodes)}
    distance_matrix = np.zeros((num_nodes, num_nodes))
    
    for u, node_u in enumerate(nodes):
        for v, node_v in enumerate(nodes):
            if u != v:
                try:
                    distance_matrix[u, v] = nx.shortest_path_length(G, source=node_u, target=node_v, weight='length')
                except nx.NetworkXNoPath:
                    distance_matrix[u, v] = np.inf

    # Appliquer l'algorithme K-Means pour obtenir les clusters
    kmeans = KMeans(n_clusters=k, random_state=0).fit(distance_matrix)

    # Récupérer les indices des clusters
    cluster_indices = kmeans.labels_

    # Diviser les indices des clusters en deux groupes: i clusters de taille normale et j clusters deux fois plus gros
    cluster_sizes = np.bincount(cluster_indices)
    sorted_indices = np.argsort(cluster_sizes)[::-1]  # Clusters sorted by size in descending order

    j_clusters = sorted_indices[:j]

    # Créer les sous-graphes pour chaque cluster
    clusters = []
    for cluster_index in range(k):
        cluster_nodes = [nodes[node_index] for node_index in np.where(cluster_indices == cluster_index)[0]]
        subgraph = G.subgraph(cluster_nodes).copy()
        if cluster_index in j_clusters:
            clusters.append((subgraph,1))
        else:
            clusters.append((subgraph,0))

    # Ajouter les arêtes inter-cluster aux clusters correspondants
    for u, v, data in G.edges(data=True):
        cluster_u = cluster_indices[node_indices[u]]
        cluster_v = cluster_indices[node_indices[v]]
        
        if cluster_u != cluster_v:
            # Ajouter l'arête aux deux clusters
            clusters[cluster_u][0].add_edge(u, v, **data)
            for node, d in G.nodes(data=True):
                if node == v:
                    clusters[cluster_u][0].add_node(node, **d)

    return clusters

"""
def partitioning(G, k, i, j):
    # Convertir le graphe en matrice de distance
    nodes = list(G.nodes())
    num_nodes = len(nodes)
    node_indices = {node: i for i, node in enumerate(nodes)}
    distance_matrix = np.zeros((num_nodes, num_nodes))
    
    for i, node_u in enumerate(nodes):
        for j, node_v in enumerate(nodes):
            if i != j:
                try:
                    distance_matrix[i, j] = nx.shortest_path_length(G, source=node_u, target=node_v, weight='length')
                except nx.NetworkXNoPath:
                    distance_matrix[i, j] = np.inf

    # Appliquer l'algorithme K-Means pour obtenir les clusters
    kmeans = KMeans(n_clusters=k, random_state=0).fit(distance_matrix)

    # Récupérer les indices des clusters
    cluster_indices = kmeans.labels_

    # Diviser les indices des clusters en deux groupes: i clusters de taille normale et j clusters deux fois plus gros
    i_cluster_indices = np.where(cluster_indices < i)[0]
    j_cluster_indices = np.where(cluster_indices >= i)[0]

    # Créer les sous-graphes pour chaque cluster
    clusters = []
    for cluster_index in range(k):
        if cluster_index in i_cluster_indices:
            cluster_size = len(np.where(cluster_indices == cluster_index)[0])
            cluster_nodes = [nodes[node_index] for node_index in np.where(cluster_indices == cluster_index)[0]]
            clusters.append((G.subgraph(cluster_nodes).copy(), 0))
        elif cluster_index in j_cluster_indices:
            cluster_size = len(np.where(cluster_indices == cluster_index)[0]) * 2
            cluster_nodes = [nodes[node_index] for node_index in np.where(cluster_indices == cluster_index)[0]]
            clusters.append((G.subgraph(cluster_nodes).copy(), 1))

    for edge in G.edges():
        u, v = edge
        # Vérifier si l'arête est entre des nœuds de différents clusters
        if cluster_indices[node_indices[u]] != cluster_indices[node_indices[v]]:
            # Trouver l'indice du cluster qui contient l'un des nœuds
            if cluster_indices[node_indices[u]] in i_cluster_indices:
                cluster_index = cluster_indices[node_indices[u]]
            else:
                cluster_index = cluster_indices[node_indices[v]]
            
            # Convertir les clés en chaînes de caractères
            edge_data = G.get_edge_data(u,v)[0]
            
            # Ajouter l'arête au cluster correspondant
            for node, data in G.nodes(data=True):
                if node == v:
                    clusters[cluster_index][0].add_node(node, **data)
            clusters[cluster_index][0].add_edge(u, v, **edge_data)

    return clusters
"""