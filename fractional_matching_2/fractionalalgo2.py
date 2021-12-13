import math

# A full implementation of the algorithm to compute deterministic (2+e)-approximate vertex covers in the dynamic setting.
# Adapted from an algorithm for computing set covers.
#
# A New Deterministic Algorithm for Dynamic Set Cover
# Sayan Bhattacharya, Monika Henzinger, Danupon Nanongkai
# Accessible at: https://arxiv.org/pdf/1909.11600.pdf


class Algorithm:



    def __init__(self, epsilon, n):
        self.n = n
        self.epsilon = epsilon
        self.L = 1 + math.ceil(math.log(n, 1 + self.epsilon))
        self.counters = [0 for i in range(self.L)]
        self.level = [0 for i in range(n)]
        self.node_weight = [0 for i in range(n)]
        self.edge_weight = [[None if i == j else 0 for j in range(n)] for i in range(n)]
        self.tight_nodes = []
        self.tight_pointers = [None for i in range(n)]
        self.is_tight = [False for i in range(n)]
        self.active_edges = [[[] for j in range(self.L)] for i in range(n)] # Adjacency list for active edges
        self.active_pointers = [[None for j in range(n)] for i in range(n)] # Pointers for position of node in active edge set
        self.passive_edges = [[[] for j in range(self.L)] for i in range(n)]
        self.passive_pointers = [[None for j in range(n)] for i in range(n)] # Entry [u][v] corresponds to u's position in the adjacency list of v
        self.dead_edges = [[[] for j in range(self.L)] for i in range(n)]
        self.dead_pointers = [[None for j in range(n)] for i in range(n)]
        self.real_input = [[[] for j in range(self.L)] for i in range(n)] # The union of active and passive edges
        self.real_pointers = [[None for j in range(n)] for i in range(n)]



    def is_tight(self, v):
        return (1 + self.epsilon) ** -1 <= self.node_weight[v] and self.node_weight[v] <= 1



    def edge_weight(self, u, v):
        return (1 + self.epsilon) ** (-max(self.level[u], self.level[v]))


    def edge_level(self, u, v):
        return max(self.level[u], self.level[v])

    def set_edge_weight(self, u, v, weight):
        self.edge_weight[u][v] = weight
        self.edge_weight[v][u] = weight

    def add_edge_unilateral(self, edges, pointers, u, v, level):
        edges[u][level].append(v)
        pointers[v][u] = len(edges[u][level]) - 1

    def add_edge(self, edges, pointers, u, v, level):
        
        self.add_edge_unilateral(edges, pointers, u, v, level)
        self.add_edge_unilateral(edges, pointers, v, u, level)


    def remove_edge_unilateral(self, edges, pointers, u, v, level):
        list = edges[u][level]
        pos = pointers[v][u]
        if pos != len(list) - 1:
            last_element = list[-1]
            list[pos] = last_element
            pointers[last_element][u] = pos
        list.pop()
        pointers[v][u] = None

    def remove_edge(self, edges, pointers, u, v, level):
        if pointers[u][v] != None and pointers[v][u] != None:
            self.remove_edge_unilateral(edges, pointers, u, v, level)
            self.remove_edge_unilateral(edges, pointers, v, u, level)

    def insert(self, u, v):
        level = self.edge_level(u, v)

        if self.is_tight[u] or self.is_tight[v]:
            self.add_edge(self.real_input, self.real_pointers, u, v, level)
            self.add_edge(self.passive_edges, self.passive_pointers, u, v, level)
            self.set_edge_weight(u, v, 0)

        else:
            weight = min(1 - self.node_weight[u], 1 - self.node_weight[v])
            self.add_edge(self.real_input, self.real_pointers, u, v, level)
            self.add_edge(self.passive_edges, self.passive_pointers, u, v, level)
            self.set_edge_weight(u, v, weight)
            for node in [u,v]:
                self.node_weight[node] += weight
                if self.node_weight[node] >= (1+self.epsilon)**-1:
                    self.is_tight[node] = True
                    self.tight_nodes.append(node)
                    self.tight_pointers[node] = len(self.tight_nodes) - 1



    def delete(self, u, v):
        level = self.edge_level(u, v)
        self.remove_edge(self.real_input, self.real_pointers, u, v, level)
        self.remove_edge(self.active_edges, self.active_pointers, u, v, level)
        self.remove_edge(self.passive_edges, self.passive_pointers, u, v, level)
        self.add_edge(self.dead_edges, self.dead_pointers, u, v, level)

        level = self.edge_level(u, v)
        for k in range(self.L-1, level-1, -1):
            self.counters[k] -= 1
            if self.counters[k] <= 0:
                self.rebuild(k)
                return


    def rebuild(self, k):
        ini_active = self.active_edges
        ini_passive = self.passive_edges
        ini_real = self.real_input
        ini_dead = self.dead_edges
        u = 0
        for node in ini_real:
            for v in ini_real[u][:k+1]:
                ()#print(v)
            

        


    def toString(self):
        print(self.real_input)
        #print(self.active_edges)
        #print(self.passive_edges)
        #print(self.dead_edges)

    def vertex_cover(self):
        print(self.tight_nodes)