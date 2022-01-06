import math


class Vertex_Cover:
    def __init__(self, n, epsilon):
        self.n = n
        self.epsilon = epsilon
        self.num_edges = 0
        self.D = 0
        self.edges = [[] for i in range(n)]
        self.edge_pointers = [[None for j in range(n)] for i in range(n)]
        self.degree = [0 for i in range(n)]
        self.matching = []
        self.matching_pointers = [[None for j in range(n)] for i in range(n)]
        self.mate = [None for i in range(n)]
        self.vertex_cover = []
        self.vc_pointers = [None for i in range(n)]
        self.c = 0


    def update_D(self):
        self.D = math.ceil(8 * (self.num_edges)**0.5 / self.epsilon)

    def insert_unilateral(self, u, v):
        self.edges[u].append(v)
        self.edge_pointers[v][u] = len(self.edges[u]) - 1

    def insert(self, u, v):
        self.insert_unilateral(u, v)
        self.insert_unilateral(v, u)
        self.num_edges += 1
        self.update_D()
        if self.is_free(u) and self.is_free(v):
            self.match(u, v)
        else:
            self.handle_free(u, v)

    def handle_free(self, u, v):
        for w in [u,v]:
            if self.is_free(w):
                for neighbour in range(min(self.D, len(self.edges[w]))):
                    if self.is_free(neighbour):
                        self.match(w, neighbour)

    def delete_unilateral(self, u, v):
        pos = self.edge_pointers[u][v]
        w = self.edges[v][-1]
        self.edges[v][pos] = w
        self.edge_pointers[w][v] = pos
        self.edges[v].pop()
        self.edge_pointers[v][u] = 0
    
    def delete(self, u, v):
        self.delete_unilateral(u, v)
        self.delete_unilateral(v, u)
        self.num_edges -= 1
        self.update_D()
        if self.mate[u] == v:
            self.unmatch(u, v)
        self.handle_free( u, v)

    def insert_vc(self, v):
        self.vertex_cover.append(v)
        self.vc_pointers[v] = len(self.vertex_cover) - 1

    def delete_vc(self, v):
        pos = self.vc_pointers[v]
        w = self.vertex_cover[-1]
        self.vertex_cover[pos] = w
        self.vc_pointers[w] = pos
        self.vertex_cover.pop()
        self.vc_pointers[v] = None

    def match(self, u, v):
        edge = (min(u, v), max(u, v))
        self.matching.append(edge)
        self.matching_pointers[edge[0]][edge[1]] = len(self.matching) - 1
        self.mate[u] = v
        self.mate[v] = u
        self.vertex_cover.append(u)
        self.insert_vc(u)
        self.insert_vc(v)

    def unmatch(self, u, v):
        edge = (min(u, v), max(u, v))
        pos = self.matching_pointers[edge[0]][edge[1]]
        last_edge = self.matching[-1]
        self.matching[pos] = last_edge
        self.matching_pointers[last_edge[0]][last_edge[1]] = pos
        self.matching.pop()
        self.matching_pointers[edge[0]][edge[1]]
        self.mate[u] = None
        self.mate[v] = None

    def is_free(self, v):
        return self.mate[v] == None
