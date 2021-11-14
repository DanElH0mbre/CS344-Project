from tkinter import *
import math

class Animator:
    def __init__(self, n):
        # n is the number of nodes in the input graph
        self.n = n

        # Setup for tkinter canvas and draws nodes on canvas.
        # Nodes are numbered from 0 to n-1.
        # We store the nodes and possible edges in arrays to enable constant time insertion and deletion.
        self.window = Tk()
        h = 700
        w = 900
        self.canvas = Canvas(self.window, bg = "white", height = h, width = w)
        self.centre = [h/2, w/2]
        self.graph_r = 300
        self.nodes = [None for i in range(n)]
        self.lines = [[None for i in range(n)] for j in range(n)]
        for node in range(n):
            x = self.node_pos_x(node)
            y = self.node_pos_y(node)
            r = 7
            self.nodes[node] = (self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black"), self.node_pos_x(node), self.node_pos_y(node))
            self.canvas.create_text(x+18*math.sin(2 * math.pi * (node / self.n)), y+18*math.cos(2 * math.pi * (node / self.n)), text=str(node), fill="black", font=("Calibri 12"))
        self.canvas.pack()

    def node_pos_x(self, node):
        return  self.centre[0] + self.graph_r * math.sin(2 * math.pi * (node / self.n))

    def node_pos_y(self, node):
        return  self.centre[0] + self.graph_r * math.cos(2 * math.pi * (node / self.n))

    #Draws the edge (u, v) on the graph.
    def insert(self, u, v):
        line = self.canvas.create_line(self.nodes[u][1], self.nodes[u][2], self.nodes[v][1], self.nodes[v][2], fill="black", width = 1)
        self.lines[u][v] = line
        self.lines[v][u] = line
        self.window.update_idletasks()
        self.window.update()

    #Remove the edge (u, v) from the graph.
    def delete(self, u, v):
        line = self.lines[u][v]
        self.canvas.delete(line)
        self.lines[u][v] = None
        self.lines[v][u] = None

    #Colours the set of nodes given green, which indicates the approximated minimum vertex cover.
    def highlight_vc(self, nodes):
        for node in nodes:
            self.canvas.itemconfig(self.nodes[node][0], fill="green")
