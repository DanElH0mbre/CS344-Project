import sys, importlib
from hopcroftkarp import HopcroftKarp as approxmcm
from vertex_cover import Vertex_Cover
from collections import defaultdict

class Algorithm:

    def __init__(self, epsilon, n, bip_cut):
        self.epsilon = epsilon
        self.n = n
        self.counter = 0
        self.bip_cut = bip_cut
        self.edges = [[] for i in range(n)]
        self.pointers = [[None for j in range(n)] for i in range(n)] # Entry [u][v] points to u's position in v's adjacency list
        self.is_neighbour = [[False for j in range(n)] for i in range(n)]
        self.matching = set()
        self.vc = Vertex_Cover(n)

    def insert_unilateral(self, u, v):
        self.edges[u].append(v)
        self.pointers[v][u] = len(self.edges[u]) - 1

    def insert(self, u, v):
        self.insert_unilateral(u, v)
        self.insert_unilateral(v, u)
        self.vc.insert(u, v)
        self.handle_counter()

    def delete_unilateral(self, u, v):
        pos = self.pointers[u][v]
        if pos != len(self.edges[v]) - 1:
            node = self.edges[v][-1]
            self.edges[v][pos] = node
            self.pointers[node][v] = pos
        self.edges[v].pop()
        self.pointers[u][v] = None

    def delete(self, u, v):
        x = u if u < v else v
        y = v if u < v else u
        if (x, y) in self.matching:
            self.matching.delete((x, y))
        self.delete_unilateral(u, v)
        self.delete_unilateral(v, u)
        self.vc.delete(u, v)
        self.handle_counter()

    def get_core_subgraph(self):
        vertex_cover = self.vc.vertex_cover
        size = len(vertex_cover)
        subgraph = defaultdict(list)
        for u in vertex_cover:
            c = size + 1
            for v in self.edges[u]:
                if v in vertex_cover and u < v:
                    subgraph[u].append(v)
                elif v not in vertex_cover and u < v and c >= 0:
                    subgraph[u].append(v)
                    c -= 1
        return subgraph

    def format_graph(self, edges):
        dict_graph = {}
        for v in range(self.bip_cut):
            dict_graph[v] = {neighbour for neighbour in self.edges[v]}
        return dict_graph

    def handle_counter(self):
        self.counter -= 1
        if self.counter <= 0:
            subgraph = self.get_core_subgraph()
            self.matching = approxmcm(subgraph).maximum_matching(keys_only=True)
            self.counter = (self.epsilon/4) * len(self.matching)

    def toString(self):
        print(self.matching)
        print(self.bip_cut)
        print(len(self.matching))
        print(self.epsilon)
