from typing import Match
from pytrees import AVLTree
from heapq_max import *
import math

#Computes a maximal matching and takes the set of endpoints as the 2-approximate vertex cover.

class Vertex_Cover:
    def __init__(self, n):
        self.matching = AVLTree()
        self.mate = [None for i in range(n)]
        self.neighbours = [AVLTree() for i in range(n)]
        self.degree = [0 for i in range(n)]
        self.free_nbhrs = [F(n) for i in range(n)]
        self.free_v_heap = AVLTree()
        for i in range(n):
            self.free_v_heap.insert((0,i))
        self.num_edges = 0
        self.vertex_cover = []
        self.vc_pointers = [None for i in range(n)]

    def insert(self, u, v):
        self.neighbours[u].insert(v)
        self.neighbours[v].insert(u)
        self.degree[u] += 1
        self.degree[v] += 1
        self.num_edges += 1
        if self.is_free(u):
            self.free_v_heap.delete((self.degree[u]-1, u))
            self.free_v_heap.insert((self.degree[u], u))
            self.free_nbhrs[v].insert(u)
        if self.is_free(v):
            self.free_v_heap.delete((self.degree[v]-1, v))
            self.free_v_heap.insert((self.degree[v], v))
            self.free_nbhrs[u].insert(v)
        if self.is_free(u) and self.is_free(v):
            self.match(u, v)
        else:
            if self.is_free(u):
                self.handle_one_free(u, v)
            if self.is_free(v):
                self.handle_one_free(v, u)



    def handle_one_free(self, u, v):
        z = self.mate[v]
        self.free_nbhrs[z].delete(u)
        if self.free_nbhrs[z].has_free():
            self.delete_from_matching((min(v,z), max(v,z)))
            self.match(u, v)
            self.match(z, self.free_nbhrs[z].get_free())
            
        else:
            for w in self.free_nbhrs[u].nbhrs:
                self.free_nbhrs[w].insert(u)

    def delete(self, u, v):
        
        def match_loop(node):
            if self.free_nbhrs[node].has_free():
                self.match(node, self.free_nbhrs[node].get_free())
            else:
                if self.degree[node] > (2*self.num_edges)**0.5:
                    node = self.surrogate(node)
                    match_loop(node)
                else:
                    self.aug_path(node)

        self.neighbours[u].delete(v)
        self.neighbours[v].delete(u)
        self.degree[u] -= 1
        self.degree[v] -= 1
        self.num_edges -= 1
        if self.mate[u] != v:
            if self.is_free(u):
                self.free_nbhrs[v].delete(u)
            if self.is_free(v):
                self.free_nbhrs[u].delete(v)
        elif self.mate[u] == v:
            self.delete_from_matching((u, v) if u < v else (v, u))
            for node in [u,v]:
                match_loop(node)

        
    

    def match(self, u, v):
        self.matching.insert((u, v) if u < v else (v, u))
        for node in [u, v]:
            self.vertex_cover.append(node)
            self.vc_pointers[node] = len(self.vertex_cover) - 1
        self.free_v_heap.delete((self.degree[u], u))
        self.free_v_heap.delete((self.degree[u], v))
        for w in [u,v]:
            for x in self.neighbours[w].inOrder():
                self.free_nbhrs[x].delete(w)
        self.mate[u] = v
        self.mate[v] = u


    def surrogate(self, v):
        z = None
        for w in self.neighbours[v]:
            z = self.mate(w)
            if z != None and self.degree[z] <= (2*m)**0.5:
                break
        self.delete_from_matching((w, z))
        self.match(v, w)
        return z

    def is_free(self, v):
        return self.mate[v] == None

    def aug_path(self, v):
        x = None
        for w in self.neighbours[v].inOrder():
            z = self.mate[w]
            if z != None and self.free_nbhrs[z].has_free():
                x = self.free_nbhrs[w].get_free()
                break
        if x != None:
            self.delete_from_matching((min(w,z), max(w,z)))
            self.match(v, w)
            self.match(z, x)
            
        else:
            for w in self.neighbours[v].inOrder():
                self.free_nbhrs[w].insert(v)
                self.free_v_heap.insert((self.degree[v], v))
                self.mate[v] = None

    def delete_from_matching(self, edge):
        self.matching.delete(edge)
        for node in edge:
            pos = self.vc_pointers[node]
            if pos != len(self.vertex_cover) - 1:
                z = self.vertex_cover[-1]
                self.vertex_cover[pos] = z
                self.vc_pointers[z] = pos
            self.vertex_cover.pop()
            self.vc_pointers[node] = None
        

class F:
    def __init__(self, n):
        self.size = math.ceil(n**0.5)
        self.nbhrs = []
        self.pointers = [None for i in range(n)]
        self.free_nbhrs = [False for j in range(n)]
        self.counter = [0 for i in range(self.size)]
        self.num_nbhrs_free = 0

    def insert(self, v):
        self.free_nbhrs[v] = True
        #self.nbhrs.append(v)
        #self.pointers[v] = len(self.nbhrs) - 1
        pos = math.floor(v/self.size)
        self.counter[pos] += 1
        self.num_nbhrs_free += 1

    def delete(self, v):
        self.free_nbhrs[v] = False
        #if self.pointers[v] != len(self.nbhrs) - 1:
            #node = self.nbhrs[-1]
            #self.nbhrs[self.pointers[v]] = node
            #self.pointers[node] = self.pointers[v]
        #self.nbhrs.pop()
        #self.pointers[v] = None
        pos = math.floor(v/self.size)
        self.counter[pos] -= 1
        self.num_nbhrs_free -= 1

    def has_free(self):
        return self.num_nbhrs_free > 0

    def get_free(self):
        for i in range(len(self.counter)):
            if self.counter[i] > 0:
                for j in range(i*self.size, (i+1)*self.size):
                    if self.free_nbhrs[j] == True:
                        return j