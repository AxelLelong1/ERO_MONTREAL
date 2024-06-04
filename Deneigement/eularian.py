import networkx as nx

def to_eularian(G):

    odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 != 0]

    for i in range(0,len(odd_nodes) - 1,2):
        path = nx.dijkstra_path(G, odd_nodes[i], odd_nodes[i+1])

        for j in range(len(path) - 1):
            G.add_edge(path[j], path[j + 1], length=nx.shortest_path_length(G, source=path[j], target=path[j + 1], weight='length'))
    
    return G

def eularian_cycle(G):
    if(not nx.is_eulerian(G)):
        G = to_eularian(G)
    l = [u for u, v in nx.eulerian_circuit(G)]
    l.append(l[0])
    return l