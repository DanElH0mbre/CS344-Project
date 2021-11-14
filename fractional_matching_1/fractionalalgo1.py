import math

class Algorithm:
    def __init__(self, epsilon, n):
        self.n = n
        self.dirty_nodes = []
        self.dirty_pointers = [None for i in range(n)]
        self.alpha = 1 + 3*epsilon
        self.beta = 1 + epsilon
        self.L = 1 + math.ceil(math.log(self.n / self.alpha, self.beta))
        self.level = [0 for i in range(n)]
        self.weight = [0 for i in range(n)]
        self.neighbours = [[[] for j in range(self.L)] for i in range(n)]
        self.nbhd_pointers = [[None for j in range(n)] for i in range(n)] # Entry [u][v] corresponds to u's position in the neighbourhood lists of v
        self.is_dirty = [False for i in range(n)]
        self.heavy_nodes = [] #The list of all nodes with weight at least 1
        self.heavy_pointers = [None for i in range(n)]

    def is_violation(self, v): #Invariant 2.4; a violation means that we have a dirty node whose level must be changed.
        w = self.weight[v]
        return not (w <= self.alpha * self.beta) if self.level[v] == 0 else not (w >= 1 and w <= self.alpha*self.beta)

    def edge_weight(self, u, v):
        return self.beta**(-max(self.level[u], self.level[v]))

    # Returns the weight of an edge that has endpoints at the levels specified. 
    def level_edge_weight(self, l1, l2):
        return self.beta**(-max(l1, l2))

    def level_difference(self, u, v):
        return max(0, self.level[u] - self.level[v])

    # Whenever some nodes have their weight updated, we check whether they still belong in the set of heavy nodes. O(1) update time per node.
    def consider_heavy(self, nodes):
        for node in nodes:
            if self.heavy_pointers[node] == None and self.weight[node] >= 1:
                self.heavy_nodes.append(node)
                self.heavy_pointers[node] = len(self.heavy_nodes) - 1
            elif self.heavy_pointers[node] != None and self.weight[node] < 1:
                if self.heavy_pointers[node] != len(self.heavy_nodes) - 1:
                    pos = self.heavy_pointers[node]
                    temp = self.heavy_nodes[-1]
                    self.heavy_nodes[pos] = self.heavy_nodes[-1]
                    self.heavy_pointers[temp] = pos
                self.heavy_nodes.pop()
                self.heavy_pointers[node] = None

    def insert(self, u, v):
        weight = self.edge_weight(u, v)
        self.weight[u] += weight
        self.weight[v] += weight
        self.consider_heavy([u, v])
        self.add_neighbours(u,v)
        self.add_neighbours(v,u)

        for node in [u,v]:
            if node in self.dirty_nodes and not self.is_violation(node):
                self.dirty_nodes.remove(node)
            if self.is_violation(node):
                self.set_dirty(node)

        self.handle_dirty()

    def delete(self, u, v):
        weight = self.edge_weight(u, v)
        self.weight[u] -= weight
        self.weight[v] -= weight
        self.consider_heavy([u, v])
        self.remove_neighbours(u,v)
        self.remove_neighbours(v,u)

        for node in [u,v]:
            if node in self.dirty_nodes and not self.is_violation(node):
                self.dirty_nodes.remove(node)
            if self.is_violation(node):
                self.set_dirty(node)

        self.handle_dirty()


    def add_neighbours(self, u, v):
        pos = max(0, self.level[v]-self.level[u])
        self.neighbours[u][pos].append(v)
        self.nbhd_pointers[v][u] = len(self.neighbours[u][pos])-1

    def remove_neighbours(self, u, v):
        v_pos_in_u = self.nbhd_pointers[v][u]
        level = max(0, self.level[v] - self.level[u])
        if v_pos_in_u != len(self.neighbours[u][level]) - 1:
            self.swap_to_end(v, u)
        self.neighbours[u][level].pop()

    def update_position_levelup(self, v, u): 
        v_pos_in_u = self.nbhd_pointers[v][u]
        leveldiff = max(0, self.level[v]-self.level[u])
        if v_pos_in_u != len(self.neighbours[u][leveldiff]) -1:
            self.swap_to_end(v, u)
        self.neighbours[u][self.level[v]-self.level[u]].pop()
        self.neighbours[u][self.level[v]-self.level[u]+1].append(v)
        self.nbhd_pointers[v][u] = len(self.neighbours[u][self.level[v]-self.level[u]+1]) - 1

    def update_position_leveldown(self, v, u): 
        v_pos_in_u = self.nbhd_pointers[v][u]
        leveldiff = self.level_difference(v, u)
        if v_pos_in_u != len(self.neighbours[u][leveldiff]) -1:
            self.swap_to_end(v, u)
        self.neighbours[u][leveldiff].pop()
        self.neighbours[u][leveldiff-1].append(v)
        self.nbhd_pointers[v][u] = len(self.neighbours[u][leveldiff-1]) - 1

    def swap_to_end(self, v, u): #When a node is being removed from a neighbourhood list, we swap it to the final position to enable constant time deletion
        v_pos_in_u = self.nbhd_pointers[v][u]
        leveldiff = max(0, self.level[v]-self.level[u])
        temp = self.neighbours[u][leveldiff][v_pos_in_u]
        self.neighbours[u][leveldiff][v_pos_in_u] = self.neighbours[u][leveldiff][-1]
        self.neighbours[u][leveldiff][-1] = temp
        switched_node = self.neighbours[u][leveldiff][v_pos_in_u]
        self.nbhd_pointers[switched_node][u] = v_pos_in_u

    def set_dirty(self, v):
        self.dirty_nodes.append(v)
        self.is_dirty[v] = True
        self.dirty_pointers[v] = len(self.dirty_nodes) - 1

    def handle_dirty(self):
        while len(self.dirty_nodes) != 0:
            
            v = self.dirty_nodes[-1]
            if self.weight[v] > self.alpha * self.beta:
                for u in self.neighbours[v][0]:
                    if self.level[u] <= self.level[v]:
                        self.update_position_levelup(v, u)

                    prev_edge_weight = self.edge_weight(u, v)
                    new_edge_weight = self.level_edge_weight(self.level[u], self.level[v]+1)
                    diff = new_edge_weight - prev_edge_weight
                    self.weight[u] += diff
                    if u in self.dirty_nodes and not self.is_violation(u):
                        self.dirty_nodes.remove(u)
                    if u not in self.dirty_nodes and self.is_violation(u):
                        self.dirty_nodes.append(u)
                    self.weight[v] += diff
                    self.consider_heavy([u, v])

                self.level[v] += 1
                temp = self.neighbours[v][0]
                self.neighbours[v].pop(0)
                l = len(self.neighbours[v][0])
                self.neighbours[v][0] = self.neighbours[v][0] + temp
                i = 0
                for node in temp:
                    self.nbhd_pointers[node][v] = l + i
                    i+=1

            elif self.weight[v] < 1 and self.level[v] > 0:
                v = self.dirty_nodes[-1]
                lower_neighbours = []
                equal_neighbours = []
                for u in self.neighbours[v][0]:
                    if self.level[u] < self.level[v]:
                        lower_neighbours.append(u)
                        self.update_position_leveldown(v, u)
                    else:
                        equal_neighbours.append(u)

                    prev_edge_weight = self.edge_weight(u, v)
                    new_edge_weight = self.level_edge_weight(self.level[u], self.level[v]-1)
                    diff = new_edge_weight - prev_edge_weight
                    self.weight[u] += diff
                    if u in self.dirty_nodes and not self.is_violation(u):
                        self.dirty_nodes.remove(u)
                    if u not in self.dirty_nodes and self.is_violation(u):
                        self.dirty_nodes.append(u)
                    
                    self.weight[v] += diff
                    self.consider_heavy([u, v])

                self.level[v] -= 1
                self.neighbours[v] = [lower_neighbours] + [equal_neighbours] + self.neighbours[v][1:]
                i=0
                for node in lower_neighbours:
                    self.nbhd_pointers[node][v] = i
                    i+=1
                i=0
                for node in equal_neighbours:
                    self.nbhd_pointers[node][v] = i
                    i+=1

            if not self.is_violation(v):
                self.dirty_nodes.remove(v)
    
    def toString(self):
        for v in range(self.n):
            print(v, self.level[v], round(self.weight[v], 3))#, self.neighbours[v])
        print("vertex cover:", self.heavy_nodes)
        print("{} out of {}".format(len(self.heavy_nodes), self.n))
        print("fractional matching of weight {}".format(round(sum(self.weight)/2, 3)))

    def vertex_cover(self):
        return self.heavy_nodes

#Running times are incorrect, add pointers to dirty nodes for constant time deletion.
#Reverse neightbourhood lists so that we delete the final element when incrementing level, for constant time update.

"""
G = Algorithm(0.25, 8)
G.insert(0, 1)
G.insert(2, 3)
G.insert(3, 4)
G.delete(0, 1)
G.insert(3, 5)
G.insert(3, 6)
G.insert(0, 6)
G.insert(0, 3)
G.insert(0, 4)
G.insert(1, 5)
G.insert(2, 4)
G.insert(4, 7)
G.insert(6, 4)
G.delete(3, 5)
G.delete(2, 3)
G.insert(7, 3)
G.delete(3, 4)
G.delete(3, 6)
G.insert(2, 7)
G.delete(4, 6)
G.toString()
"""