from Drone.show import *
from Drone.graph_calculus import *
from Vehicule.show import *
import osmnx as ox

def main():
    print("1. Outremont")
    print("2. Verdun")
    print("3. Anjou")
    print("4. Plateau")
    print("5. Rivière")

    res = -1
    while (res == -1):
        res = input("Which city do you want to compute ?")
        if (int(res) < 0 and int(res) > 5):
            res = -1
    
    res = int(res) - 1
    city = ["Outremont", "Verdun", "Anjou", "Le Plateau-Mont-Royal", "Rivière-des-prairies-pointe-aux-trembles"]
    Type1 = [0, 1, 11, 10, 29]
    Type2 = [2, 2, 1, 0, 2]
    
    print("Getting graph of ", city[res])

    G = (ox.load_graphml(filepath="./data/"+city[res]+".graphml"))
    H = (ox.load_graphml(filepath="./data/"+city[res]+"-E.graphml"))

    H = add_snow_depth(H)

    print("Calculating snow depth with the drone")
    H, G = Calculate_Snow(H, G)

    cycle_length = Calculate_Lenght(H)
    temps = (cycle_length / 20) / 3600
    cout = cycle_length * 0.00001 + 100
    print("The drone will travel ", round(cycle_length, 2), " meters")
    print("This will take ", round(temps, 2), " hours to complete at the cost of ", round(cout, 2), " $")

    Show_Snow(G)

    print("Calculating graph optimizations")
    G = handle_one_way_streets(G)
    G = find_largest_scc(G)
    clusters = partitioning(G, Type1[res] + Type2[res], Type1[res], Type2[res])

    distance, temps, cout, G = calculs(clusters, G)
    Show_Snow(G)

    print("Coût Déneigeuses total = ", cout)
    print("Temps Déneigeuse total en heure = ", temps)
    print("distance totale = ", distance)
main()