from show import *
from graph_calculus import *
from graph_utils import *

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

G = (ox.load_graphml(filepath="./data/Anjou.graphml"))
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



G = (ox.load_graphml(filepath="./data/Le Plateau-Mont-Royal.graphml"))
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
#Show_Drone_Circuit(G)

G = (ox.load_graphml(filepath="./data/Rivière-des-prairies-pointe-aux-trembles.graphml"))
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