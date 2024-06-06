import networkx as nx
from utils import *

def eulerize_directed_graph(G):
    # Créer une copie de G pour éviter de modifier l'original
    H = G.copy()
    
    # Calculer les degrés entrants et sortants de chaque sommet
    in_degrees = {node: 0 for node in G.nodes()}
    out_degrees = {node: 0 for node in G.nodes()}
    
    for u, v in G.edges():
        out_degrees[u] += 1
        in_degrees[v] += 1
    
    # Identifier les déséquilibres
    imbalance = {node: out_degrees[node] - in_degrees[node] for node in G.nodes()}
    
    # Listes de nœuds avec excès de sorties et entrées
    excess_out = [node for node in G.nodes() if imbalance[node] > 0]
    excess_in = [node for node in G.nodes() if imbalance[node] < 0]
    
    # Ajouter des arêtes pour équilibrer les degrés entrants et sortants
    while excess_out and excess_in:
        u = excess_out[0]
        v = excess_in[0]
        
        if (u, v) in G.edges():
            H.add_edge(u, v)
            imbalance[u] -= 1
            imbalance[v] += 1
            
            if imbalance[u] == 0:
                excess_out.pop(0)
            if imbalance[v] == 0:
                excess_in.pop(0)
        else:
            excess_out.append(excess_out.pop(0))
    
    return H

def make_semi_eulerian_with_existing_edges(G):
    G = handle_one_way_streets(G)
    G = find_largest_scc(G)
    in_degrees = G.in_degree()
    out_degrees = G.out_degree()
    
    # Listes pour les sommets avec des déséquilibres
    excess_out = []
    excess_in = []

    for node in G.nodes():
        in_deg = in_degrees[node]
        out_deg = out_degrees[node]
        if out_deg > in_deg:
            excess_out.extend([node] * (out_deg - in_deg))
        elif in_deg > out_deg:
            excess_in.extend([node] * (in_deg - out_deg))

    # Ajouter des arêtes pour équilibrer les degrés
    for u, v in zip(excess_out, excess_in):
        if G.has_edge(u, v):
            edge_data = G.get_edge_data(u, v)
            G.add_edge(u, v, **edge_data)
        else:
            # Chercher un remplacement parmi les arêtes existantes sortantes de u ou entrantes de v
            for successor in G.successors(u):
                if G.has_edge(successor, v):
                    edge_data = G.get_edge_data(successor, v)
                    G.add_edge(successor, v, **edge_data)
                    break
                else:
                    # Si aucun remplacement n'a été trouvé, lever une erreur
                    raise ValueError(f"Impossible de trouver une arête existante pour équilibrer le sommet {u} vers {v}.")

    return G