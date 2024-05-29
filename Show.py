import osmnx as ox
import matplotlib.pyplot as plt

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


G = (ox.convert.to_undirected(ox.load_graphml(filepath="./data/Outremont.graphml")))
ShowGraph(G)

G = (ox.convert.to_undirected(ox.load_graphml(filepath="./data/Verdun.graphml")))
ShowGraph(G)

G = (ox.convert.to_undirected(ox.load_graphml(filepath="./data/Anjou.graphml")))
ShowGraph(G)

G = (ox.convert.to_undirected(ox.load_graphml(filepath="./data/Riviere.graphml")))
ShowGraph(G)

G = (ox.convert.to_undirected(ox.load_graphml(filepath="./data/Plateau.graphml")))
ShowGraph(G)
