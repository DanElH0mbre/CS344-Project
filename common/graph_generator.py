import math
import sys, random

class Generator:
    def __init__(self):
        self.epsilon = sys.argv[1]
        self.n = int(sys.argv[2])
        self.number_of_updates = int(sys.argv[3])
        self.max_edges = (self.n * (self.n - 1)) / 2
        self.create_graph()

    def all_edges(self):
        s = set()
        for i in range(0, self.n):
            for j in range(i+1, self.n):
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
Generator()