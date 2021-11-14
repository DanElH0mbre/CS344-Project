import math

# A full implementation of the algorithm to compute deterministic fully dynamic vertex covers.
#
# Sayan Bhattacharya, Monika Henzinger, and Guiseppe F. Italiano
# Deterministic Fully Dynamic Data Structures for Dynamic Vertex Cover and Matching
# 2018 Society for Industrial and Applied Mathematics
# DOI: 10.1137/140998925


class Algorithm:


    #Defines the relevant constants and data structures.
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
        self.heavy_nodes = [] #The list of all nodes with weight at least 1
        self.heavy_pointers = [None for i in range(n)]


    # Invariant 2.4; a violation means that we have a dirty node whose level must be changed.
    def is_violation(self, v): 
        w = self.weight[v]
        return not (w <= self.alpha * self.beta) if self.level[v] == 0 else not (w >= 1 and w <= self.alpha*self.beta)


    # The weight of an edge is determined by the levels of its endpoints, as specified in the paper.
    def edge_weight(self, u, v):
        return self.beta**(-max(self.level[u], self.level[v]))


    # Returns the weight of an edge that has endpoints at the levels specified. 
    def level_edge_weight(self, l1, l2):
        return self.beta**(-max(l1, l2))


    # Gets the position of the sublist containing u in the neighbourhood lists of v.
    # Importantly, the neighbourhood lists are ordered backwards, such that Nv(0, i) is the final element of the list
    # Since this is the only element that needs adjusting in each step of the handler, we can delete or add new elements in constant time.
    def level_difference(self, u, v):
        return len(self.neighbours[v]) - 1 -max(0, self.level[u] - self.level[v])


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


    # When the weight of some nodes change, we must ensure that the set of dirty nodes is kept up to date.
    def consider_dirty(self, nodes):
        for node in nodes:
            if self.dirty_pointers[node] != None and not self.is_violation(node):
                self.remove_dirty(node)
            if self.dirty_pointers[node] == None and self.is_violation(node):
                self.set_dirty(node)


    # When we insert an edge, we must:
        # Adjust the weight of its endpoints.
        # Insert each endpoint into the neighbourhood lists of the other endpoint.
        # Consider if the edges violate Invariant 2.4, and thus become dirty.
    def insert(self, u, v):
        weight = self.edge_weight(u, v)
        self.weight[u] += weight
        self.weight[v] += weight

        self.consider_heavy([u, v])

        self.add_neighbours(u,v)
        self.add_neighbours(v,u)

        self.consider_dirty([u,v])
        self.handle_dirty()


    # When we delete an edge, we must:
        # Adjust the weight of its endpoints.
        # Remove each endpoint into the neighbourhood lists of the other endpoint.
        # Consider if the edges violate Invariant 2.4, and thus become dirty.
    def delete(self, u, v):
        weight = self.edge_weight(u, v)
        self.weight[u] -= weight
        self.weight[v] -= weight

        self.consider_heavy([u, v])

        self.remove_neighbours(u,v)
        self.remove_neighbours(v,u)

        self.consider_dirty([u,v])
        self.handle_dirty()

    
    # Places node v into the neighbourhood lists of node u.
    def add_neighbours(self, u, v):
        pos = self.level_difference(v, u) 
        self.neighbours[u][pos].append(v)
        self.nbhd_pointers[v][u] = len(self.neighbours[u][pos])-1


    # Removes node v from the neighbourhood lists of node u, in constant time.
    def remove_neighbours(self, u, v):
        v_pos_in_u = self.nbhd_pointers[v][u]
        level = self.level_difference(v, u)
        if v_pos_in_u != len(self.neighbours[u][level]) - 1:
            self.swap_to_end(v, u)
        self.neighbours[u][level].pop()

    
    # When a node v changes level, we must update its position in the neighbourhood lists of its neighbours.
    # Note that, because the neighbourhood lists are ordered backwards, we subtract the level_change instead of adding it.
    def update_position(self, v, u, level_change):
        v_pos_in_u = self.nbhd_pointers[v][u]
        leveldiff = self.level_difference(v, u)
        if v_pos_in_u != len(self.neighbours[u][leveldiff]) - 1:
            self.swap_to_end(v, u)
        self.neighbours[u][leveldiff].pop()
        self.neighbours[u][leveldiff-level_change].append(v)
        self.nbhd_pointers[v][u] = len(self.neighbours[u][leveldiff-level_change]) - 1


    # When v's level increases, updates v's position in the neighbourhood lists of u.
    def update_position_levelup(self, v, u): 
        self.update_position(v, u, 1)


    # When v's level decreases, updates v's position in the neighbourhood lists of u.
    def update_position_leveldown(self, v, u): 
        self.update_position(v, u, -1)


    # When deleting a node from an array, we first swap it to the end of the array, and then pop the node, which enables constant-time deletion.
    # The pointers must be updated when this happens.
    def swap_to_end(self, v, u): 
        v_pos_in_u = self.nbhd_pointers[v][u]
        leveldiff = self.level_difference(v, u)
        temp = self.neighbours[u][leveldiff][v_pos_in_u]
        self.neighbours[u][leveldiff][v_pos_in_u] = self.neighbours[u][leveldiff][-1]
        self.neighbours[u][leveldiff][-1] = temp
        switched_node = self.neighbours[u][leveldiff][v_pos_in_u]
        self.nbhd_pointers[switched_node][u] = v_pos_in_u


    # A previously clean node becomes dirty. The pointer changed from None to now reflect v's position in the list of dirty nodes.
    def set_dirty(self, v):
        self.dirty_nodes.append(v)
        self.dirty_pointers[v] = len(self.dirty_nodes) - 1


    # A previously dirty node becomes clean. The pointer is set back to None.
    def remove_dirty(self, v):
        pos = self.dirty_pointers[v]
        if pos != len(self.dirty_pointers) - 1:
            last = self.dirty_nodes[-1]
            self.dirty_nodes[pos] = last
            self.dirty_pointers[last] = pos
        self.dirty_nodes.pop()
        self.dirty_pointers[v] = None


    # An implementation of the while loop described in Figure 1, section 2.3
    def handle_dirty(self):
        while len(self.dirty_nodes) != 0:
            
            v = self.dirty_nodes[-1]
            if self.weight[v] > self.alpha * self.beta:
                for u in self.neighbours[v][-1]:
                    if self.level[u] <= self.level[v]:
                        self.update_position_levelup(v, u)

                    prev_edge_weight = self.edge_weight(u, v)
                    new_edge_weight = self.level_edge_weight(self.level[u], self.level[v]+1)
                    diff = new_edge_weight - prev_edge_weight
                    self.weight[u] += diff
                    self.consider_dirty([u])
                    self.weight[v] += diff
                    self.consider_heavy([u, v])

                self.level[v] += 1
                temp = self.neighbours[v][-1]
                self.neighbours[v].pop()
                l = len(self.neighbours[v][-1])
                self.neighbours[v][-1] = self.neighbours[v][-1] + temp
                i = 0
                for node in temp:
                    self.nbhd_pointers[node][v] = l + i
                    i+=1

            elif self.weight[v] < 1 and self.level[v] > 0:
                v = self.dirty_nodes[-1]
                lower_neighbours = []
                equal_neighbours = []
                for u in self.neighbours[v][-1]:
                    if self.level[u] < self.level[v]:
                        lower_neighbours.append(u)
                        self.update_position_leveldown(v, u)
                    else:
                        equal_neighbours.append(u)

                    prev_edge_weight = self.edge_weight(u, v)
                    new_edge_weight = self.level_edge_weight(self.level[u], self.level[v]-1)
                    diff = new_edge_weight - prev_edge_weight
                    self.weight[u] += diff
                    self.consider_dirty([u])
                    
                    self.weight[v] += diff
                    self.consider_heavy([u, v])

                self.level[v] -= 1
                self.neighbours[v] = self.neighbours[v][:-1] + [equal_neighbours] + [lower_neighbours]
                i=0
                for node in lower_neighbours:
                    self.nbhd_pointers[node][v] = i
                    i+=1
                i=0
                for node in equal_neighbours:
                    self.nbhd_pointers[node][v] = i
                    i+=1

            if not self.is_violation(v):
                self.remove_dirty(v)
    

    # Describes the state of the graph.
    def toString(self):
        for v in range(self.n):
            print(v, self.level[v], round(self.weight[v], 3))
        print("vertex cover:", self.heavy_nodes)
        print("{} out of {}".format(len(self.heavy_nodes), self.n))
        print("fractional matching of weight {}".format(round(sum(self.weight)/2, 3)))


    # The algorithm maintains an approximate vertex cover as the set of nodes with weight at least 1.
    def vertex_cover(self):
        return self.heavy_nodes