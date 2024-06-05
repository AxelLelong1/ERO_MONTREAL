import networkx as nx
from itertools import combinations

"""
def to_eulerian(G):

    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]

    for i in range(0,len(odd_nodes) - 1,2):
        path = nx.dijkstra_path(G, odd_nodes[i], odd_nodes[i+1])

        for j in range(len(path) - 1):
            G.add_edge(path[j], path[j + 1], length=nx.shortest_path_length(G, source=path[j], target=path[j + 1], weight='length'))
    
    return G

def to_eulerian(G):
    # Find all nodes with an odd degree
    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]
    print(f"Initial number of odd-degree nodes: {len(odd_nodes)}")

    # List to store edges to add
    edges_to_add = []

    # Find the shortest path between all pairs of odd nodes
    odd_node_pairs = list(combinations(odd_nodes, 2))
    shortest_paths = {}
    for u, v in odd_node_pairs:
        distance, path = nx.single_source_dijkstra(G, u, target=v, weight='length')
        shortest_paths[(u, v)] = (distance, path)

    # Pair up odd-degree nodes to minimize the added edge length
    while odd_nodes:
        u = odd_nodes.pop()
        closest_pair = None
        closest_distance = float('inf')
        
        for v in odd_nodes:
            if (u, v) in shortest_paths:
                distance, path = shortest_paths[(u, v)]
            else:
                distance, path = shortest_paths[(v, u)]
            
            if distance < closest_distance:
                closest_distance = distance
                closest_pair = (v, path)
        
        v, path = closest_pair
        odd_nodes.remove(v)

        # Add the shortest path edges to the edges_to_add list
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i + 1])
            if edge_data:
                for key in edge_data:
                    data = edge_data[key]
                    edges_to_add.append((path[i], path[i + 1], data))

    # Add all the edges in edges_to_add to the graph
    for u, v, data in edges_to_add:
        G.add_edge(u, v, **data)

    # Check if there are still odd-degree nodes
    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]
    print(f"Final number of odd-degree nodes: {len(odd_nodes)}")

    return G
"""


def to_eulerian(G):
    # Find all nodes with an odd degree
    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]
    print(f"Initial number of odd-degree nodes: {len(odd_nodes)}")

    # List to store edges to add
    edges_to_add = []

    # Find the shortest path between all pairs of odd nodes
    odd_node_pairs = list(combinations(odd_nodes, 2))
    shortest_paths = {}
    for u, v in odd_node_pairs:
        distance, path = nx.single_source_dijkstra(G, u, target=v, weight='length')
        shortest_paths[(u, v)] = (distance, path)

    # Pair up odd-degree nodes to minimize the added edge length
    while odd_nodes:
        u = odd_nodes.pop()
        closest_pair = None
        closest_distance = float('inf')
        
        for v in odd_nodes:
            if (u, v) in shortest_paths:
                distance, path = shortest_paths[(u, v)]
            else:
                distance, path = shortest_paths[(v, u)]
            
            if distance < closest_distance:
                closest_distance = distance
                closest_pair = (v, path)
        
        v, path = closest_pair
        odd_nodes.remove(v)

        # Add the shortest path edges to the edges_to_add list
        for j in range(len(path) - 1):
            G.add_edge(path[j], path[j + 1], length=closest_distance)

    # Check if there are still odd-degree nodes
    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]
    print(f"Final number of odd-degree nodes: {len(odd_nodes)}")

    return G

def eularian_cycle(G):
    if(not nx.is_eulerian(G)):
        G = to_eulerian(G)
    l = [u for u, v in nx.eulerian_circuit(G)]
    l.append(l[0])
    return l