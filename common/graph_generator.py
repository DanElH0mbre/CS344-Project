import math
import sys, random

class Generator:
    def __init__(self):
        self.epsilon = sys.argv[1]
        self.n = int(sys.argv[2])
        self.number_of_updates = int(sys.argv[3])
        self.max_edges = (self.n * (self.n - 1)) / 2
        is_bipartite = sys.argv[4]
        self.create_graph() if is_bipartite == "0" else self.create_bipartite_graph()

    def all_edges(self):
        s = set()
        for i in range(0, self.n):
            for j in range(i+1, self.n):
                s.add((i, j))
        return s

    def all_edges_bipartite(self, bip_cut):
        s = set()
        for i in range(0, bip_cut):
            for j in range(bip_cut, self.n):
                s.add((i, j))
        return s

    def create_graph(self):
        file = open("graph.txt", "w")
        file.write(self.epsilon + " " + str(self.n) + "\n")
        added_edges = set()
        possible_edges = self.all_edges()
        for update in range(self.number_of_updates):
            edge_proportion = len(added_edges) / self.max_edges
            del_prob = math.sin(math.pi * 0.5 * edge_proportion)
            if random.random() <= del_prob: 
                edge = random.choice(tuple(added_edges))
                file.write("del " + str(edge[0]) + " " + str(edge[1]) + "\n")
                added_edges.remove(edge)
                possible_edges.add(edge)
            else:
                edge = random.choice(tuple(possible_edges))
                file.write("ins " + str(edge[0]) + " " + str(edge[1]) + "\n")
                possible_edges.remove(edge)
                added_edges.add(edge)

    def create_bipartite_graph(self):
        file = open("graph_bip.txt", "w")
        bip_cut = random.randint(int(self.n/3), int(2*self.n/3))
        file.write(self.epsilon + " " + str(self.n) + " " + str(bip_cut) + "\n")
        added_edges = set()
        possible_edges = self.all_edges_bipartite(bip_cut)
        for update in range(self.number_of_updates):
            edge_proportion = len(added_edges) / self.max_edges
            del_prob = math.sin(math.pi * 0.5 * edge_proportion)
            if random.random() <= del_prob: 
                edge = random.choice(tuple(added_edges))
                file.write("del " + str(edge[0]) + " " + str(edge[1]) + "\n")
                added_edges.remove(edge)
                possible_edges.add(edge)
            else:
                edge = random.choice(tuple(possible_edges))
                file.write("ins " + str(edge[0]) + " " + str(edge[1]) + "\n")
                possible_edges.remove(edge)
                added_edges.add(edge)
Generator()